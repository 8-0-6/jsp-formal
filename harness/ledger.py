#!/usr/bin/env python3
"""Ledger: the single source of truth for one problem's state.

One JSON file per problem at problems/<ID>/ledger.json. Every stage reads and
writes it, so progress survives context loss, session restarts, and agent
handoff. `bin/status` renders it; docs/PROGRESS.md is generated from it.
"""
import json, os, datetime

STAGES = ["scout", "statement", "skeleton", "proving", "verified", "submitted", "abandoned"]
GOAL_STATUS = ["stub", "proving", "proved", "failed", "decomposed"]

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def blank(pid, slug, title, catalog_url=""):
    return {
        "id": pid, "slug": slug, "title": title, "catalog_url": catalog_url,
        "stage": "scout",
        "budget": {"hours": 40, "usd": 300},
        "spent": {"hours": 0.0, "usd": 0.0},
        "statement": {"locked": False, "locked_at": None, "lean_name": None,
                      "source_ref": None, "fidelity_signed_off": False},
        "goals": [],
        "log": [{"ts": now(), "event": "created"}],
    }

def path(root, pid):
    return os.path.join(root, "problems", pid, "ledger.json")

def load(root, pid):
    with open(path(root, pid), encoding="utf-8") as f:
        return json.load(f)

def save(root, led):
    p = path(root, led["id"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(led, f, indent=2, ensure_ascii=False)
        f.write("\n")

def log(led, event):
    led.setdefault("log", []).append({"ts": now(), "event": event})

def counts(led):
    c = {s: 0 for s in GOAL_STATUS}
    for g in led.get("goals", []):
        c[g.get("status", "stub")] = c.get(g.get("status", "stub"), 0) + 1
    return c

def all_ledgers(root):
    base = os.path.join(root, "problems")
    if not os.path.isdir(base):
        return []
    out = []
    for d in sorted(os.listdir(base)):
        f = os.path.join(base, d, "ledger.json")
        if os.path.isfile(f):
            with open(f, encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out
