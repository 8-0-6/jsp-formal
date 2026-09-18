import json,os,re,time,urllib.request,html,sys
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
OUT='erdos_db.json'
db=json.load(open(OUT)) if os.path.exists(OUT) else {}
def text(h):
    h=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',h)
    t=html.unescape(re.sub(r'(?s)<[^>]+>','\n',h))
    return [l.strip() for l in t.split('\n') if l.strip()]
STATUS=re.compile(r'^(OPEN|SOLVED|PROVED|DISPROVED)(\s*\(LEAN\))?$')
ok=fail=0
for n in range(1,1250):
    k=str(n)
    if k in db: continue
    try:
        req=urllib.request.Request(f"https://www.erdosproblems.com/{n}",headers=UA)
        h=urllib.request.urlopen(req,timeout=20).read().decode('utf-8','replace')
        L=text(h)
        st=next((l for l in L[:80] if STATUS.match(l)), None)
        if st is None: db[k]={'status':None}; fail+=1
        else:
            i=L.index(st)
            body=" ".join(L[i+1:i+14])
            prize=next((l for l in L[i:i+6] if re.match(r'^-?\s*\$[\d,]+',l)), None)
            tags=[l for l in L[i:i+40] if l in ('number theory','graph theory','combinatorics',
                  'additive combinatorics','geometry','analysis','set theory','probability')]
            db[k]={'status':st,'blurb':body[:600],'prize':prize,'tags':tags}
            ok+=1
    except Exception as ex:
        db[k]={'status':None,'err':str(ex)[:80]}; fail+=1
    if n%50==0:
        json.dump(db,open(OUT,'w')); print(f"{n}/1249 ok={ok} fail={fail}",flush=True)
    time.sleep(0.25)
json.dump(db,open(OUT,'w'))
print(f"DONE ok={ok} fail={fail} total={len(db)}",flush=True)
