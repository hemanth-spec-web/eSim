import os, re
p = os.path.expanduser('~/.config/kicad/8.0/sym-lib-table')
bad = esim = 0
for line in open(p):
    m = re.search(r'\(name "([^"]+)"\)\(type "([^"]+)"\)\(uri "([^"]+)"\)', line)
    if not m: continue
    name, typ, uri = m.groups()
    path = re.sub(r'\$\{KICAD\d+_SYMBOL_DIR\}', '/usr/share/kicad/symbols', uri)
    if name.startswith('eSim'): esim += 1
    if '(disabled)' not in line and not os.path.exists(path):
        bad += 1; print('ENABLED+MISSING', name)
print('enabled-but-missing:', bad, ' eSim entries:', esim)
