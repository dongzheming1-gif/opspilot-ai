import json, re, sys

def norm(s):
    s = re.sub(r'^\s*\d+\.\s*\([^)]*\)\s*', '', s or '')
    s = s.replace('\u00a0', ' ')
    s = re.sub(r'\s+', '', s)
    return s

old = json.load(open(sys.argv[1], encoding='utf-8'))['questions']
new = json.load(open(sys.argv[2], encoding='utf-8'))['questions']
ans = json.load(open(sys.argv[3], encoding='utf-8'))

old_by_num = {q['num']: q for q in old}
new_by_stem = {}
for q in new:
    new_by_stem.setdefault(norm(q['stem']), q)

out = {'_comment': '由 %s 按题干+选项文本重映射到新账号（%s）' % (sys.argv[3], sys.argv[2]),
       'single': {}, 'multi': {}, 'tf': {}, 'sort': {}, 'fill': {}}
miss = []
for key in ('single', 'multi', 'tf', 'sort', 'fill'):
    for num, val in (ans.get(key) or {}).items():
        oq = old_by_num.get(int(num))
        if not oq:
            miss.append((key, num, 'old num missing')); continue
        nq = new_by_stem.get(norm(oq['stem']))
        if not nq:
            miss.append((key, num, 'stem not found: ' + oq['stem'][:40])); continue
        if key in ('single', 'sort'):
            # 按选项文本找新字母
            want_text = next((o['text'] for o in oq['opts'] if o['key'] == val), None)
            got = next((o['key'] for o in nq['opts'] if o['text'] == want_text), None)
            if got is None:
                miss.append((key, num, 'option text not found')); continue
            out[key][str(nq['num'])] = got
        elif key == 'multi':
            letters = []
            for L in val:
                want_text = next((o['text'] for o in oq['opts'] if o['key'] == L), None)
                got = next((o['key'] for o in nq['opts'] if o['text'] == want_text), None)
                if got is None:
                    miss.append((key, num, 'multi opt missing: ' + str(want_text)[:30])); letters = None; break
                letters.append(got)
            if letters:
                out[key][str(nq['num'])] = letters
        elif key == 'tf':
            out[key][str(nq['num'])] = val
        elif key == 'fill':
            out[key][str(nq['num'])] = val

json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
counts = {k: len(v) for k, v in out.items() if k != '_comment'}
print('mapped:', counts)
print('misses:', len(miss))
for m in miss[:15]: print('  MISS', m)
