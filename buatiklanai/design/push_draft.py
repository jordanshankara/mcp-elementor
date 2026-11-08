import json, os, sys, random, subprocess, hashlib
pid = sys.argv[1]; src = sys.argv[2]
random.seed(7)
def ids(els):
    for e in els:
        e['id'] = '%07x' % random.getrandbits(28)
        if e['elType'] == 'widget': e.setdefault('elements', [])
        if 'settings' in e and '_element_id' in e['settings']: pass
        ids(e.get('elements', []))
data = json.load(open(src)); ids(data)
def wp(method, path, body=None):
    cmd = ['curl', '-sS', '-m', '90', '-u', 'adminbuatiklan:' + os.environ['WPPW'], '-X', method, '-H', 'Content-Type: application/json', 'https://buatiklanai.id/wp-json' + path]
    if body is not None: cmd += ['-d', json.dumps(body)]
    return json.loads(subprocess.check_output(cmd))
cur = wp('GET', f'/claude/v1/elementor/{pid}')
r = wp('POST', f'/claude/v1/elementor/{pid}', {'data': json.dumps(data, ensure_ascii=False), 'hash': cur['hash'], 'reason': 'Beranda baru (desain majalah)'})
print(r)
