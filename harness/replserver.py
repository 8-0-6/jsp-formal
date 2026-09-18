#!/usr/bin/env python3
"""Persistent Lean REPL daemon.

Holds a `repl` process with Mathlib loaded so that checking a snippet costs
milliseconds instead of ~10s. Environments are cached per import-set, so the
~27s Mathlib load is paid once per distinct set of imports, not once per check.

Protocol (unix socket, one JSON object per connection, newline-terminated):
  request : {"code": "<lean source>"}  or  {"file": "<path>"}  or  {"op": "ping"|"shutdown"|"stats"}
  response: {"ok": bool, "errors": [...], "warnings": [...], "sorries": [...],
             "ms": int, "env_cached": bool}
"""
import json, os, re, socket, subprocess, sys, threading, time, hashlib, signal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOCK = os.path.join(ROOT, ".harness", "repl.sock")
REPL_BIN = os.path.join(os.path.dirname(ROOT), "repl", ".lake", "build", "bin", "repl")
IMPORT_RE = re.compile(r'^\s*(import\s+\S+|/-.*?-/|--.*|)\s*$')

def missing_modules(imports):
    """Import names with no corresponding .lean file in the project or its deps.

    The REPL answers a bad import with a valid-looking empty environment and no
    error, so every later message becomes noise. We detect it up front.
    """
    roots = [ROOT] + [os.path.join(ROOT, ".lake", "packages", d)
                      for d in (os.listdir(os.path.join(ROOT, ".lake", "packages"))
                                if os.path.isdir(os.path.join(ROOT, ".lake", "packages")) else [])]
    missing = []
    for line in imports.split("\n"):
        m = re.match(r'\s*import\s+(\S+)', line)
        if not m:
            continue
        rel = m.group(1).replace(".", os.sep) + ".lean"
        if not any(os.path.isfile(os.path.join(r, rel)) for r in roots):
            missing.append(m.group(1))
    return missing


class Repl:
    def __init__(self):
        self.lock = threading.Lock()
        self.envs = {}          # imports-hash -> env id
        self.proc = None
        self.start()

    def start(self):
        env = dict(os.environ)
        env["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + env.get("PATH", "")
        self.proc = subprocess.Popen(
            ["lake", "env", REPL_BIN], cwd=ROOT, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.envs.clear()

    def _raw(self, obj, timeout=300):
        """Send one JSON object, read one JSON object back."""
        self.proc.stdin.write(json.dumps(obj) + "\n\n")
        self.proc.stdin.flush()
        buf, deadline = "", time.time() + timeout
        while True:
            if time.time() > deadline:
                raise TimeoutError("repl timed out")
            line = self.proc.stdout.readline()
            if line == "":
                raise RuntimeError("repl died")
            if line.strip() == "" and buf.strip():
                return json.loads(buf)
            buf += line

    @staticmethod
    def split(code):
        """Separate the leading header (imports, comments, blank lines) from the body.

        Returns (header, body, offset) where offset is the number of header
        lines, so reported positions map back to the real file. Handles
        multi-line `/- ... -/` block comments, which Lean files open with.
        """
        lines = code.split("\n")
        i, in_block = 0, False
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if in_block:
                if "-/" in line:
                    in_block = False
                i += 1
                continue
            if stripped.startswith("/-"):
                # a block comment closed on the same line stays a header line
                if "-/" not in stripped[2:]:
                    in_block = True
                i += 1
                continue
            if stripped == "" or stripped.startswith("--") or \
               re.match(r'import\s+\S+', stripped):
                i += 1
                continue
            break
        return "\n".join(lines[:i]), "\n".join(lines[i:]), i

    def check(self, code):
        with self.lock:
            imports, body, offset = self.split(code)
            key = hashlib.sha1(imports.encode()).hexdigest()
            cached = key in self.envs
            try:
                if not cached:
                    r = self._raw({"cmd": imports or "", "env": None})
                    # A failed import leaves a crippled environment in which every
                    # later error is noise. Surface it instead of proceeding.
                    imp_errs = [m for m in r.get("messages", [])
                                if m.get("severity") == "error"]
                    bad = missing_modules(imports)
                    probe_ok = False
                    if "env" in r and not imp_errs and not bad:
                        probe = self._raw({"cmd": "example : True := trivial",
                                           "env": r["env"]})
                        probe_ok = not [m for m in probe.get("messages", [])
                                        if m.get("severity") == "error"]
                    if not probe_ok:
                        if bad:
                            detail = "no such module: " + ", ".join(bad)
                        elif imp_errs:
                            detail = "; ".join(m.get("data", "")[:200] for m in imp_errs)
                        else:
                            detail = ("imports produced an unusable environment "
                                      "(check module names)")
                        return {"ok": False,
                                "errors": [{"data": f"IMPORT FAILED: {detail}",
                                            "pos": {"line": 1, "column": 0}}],
                                "warnings": [], "sorries": [], "env_cached": False}
                    self.envs[key] = r["env"]
                r = self._raw({"cmd": body, "env": self.envs[key]})
            except (RuntimeError, TimeoutError, BrokenPipeError) as e:
                try: self.proc.kill()
                except Exception: pass
                self.start()
                return {"ok": False, "errors": [{"data": f"repl restarted: {e}"}],
                        "warnings": [], "sorries": [], "env_cached": False}
            def shift(items):
                for it in items:
                    for k in ("pos", "endPos"):
                        if isinstance(it.get(k), dict) and "line" in it[k]:
                            it[k]["line"] += offset
                return items
            msgs = shift(r.get("messages", []))
            errs = [m for m in msgs if m.get("severity") == "error"]
            warns = [m for m in msgs if m.get("severity") == "warning"]
            sorries = shift(r.get("sorries", []))
            return {"ok": not errs and not sorries, "errors": errs, "warnings": warns,
                    "sorries": sorries, "env_cached": cached}

def serve():
    os.makedirs(os.path.dirname(SOCK), exist_ok=True)
    if os.path.exists(SOCK):
        os.unlink(SOCK)
    repl = Repl()
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(SOCK); srv.listen(16)
    sys.stderr.write("ready\n"); sys.stderr.flush()
    while True:
        conn, _ = srv.accept()
        try:
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(65536)
                if not chunk: break
                data += chunk
            req = json.loads(data.decode() or "{}")
            op = req.get("op")
            if op == "ping":
                resp = {"ok": True, "pid": os.getpid()}
            elif op == "stats":
                resp = {"ok": True, "cached_envs": len(repl.envs)}
            elif op == "shutdown":
                conn.sendall((json.dumps({"ok": True}) + "\n").encode()); conn.close()
                break
            else:
                code = req.get("code")
                if code is None:
                    code = open(req["file"], encoding="utf-8").read()
                t0 = time.time()
                resp = repl.check(code)
                resp["ms"] = int((time.time() - t0) * 1000)
            conn.sendall((json.dumps(resp) + "\n").encode())
        except Exception as e:
            try: conn.sendall((json.dumps({"ok": False, "errors": [{"data": str(e)}]}) + "\n").encode())
            except Exception: pass
        finally:
            conn.close()
    try: repl.proc.kill()
    except Exception: pass
    os.unlink(SOCK)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    serve()
