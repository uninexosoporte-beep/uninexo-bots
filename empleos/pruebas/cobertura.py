import re
import sys
import collections

sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')
import reglas

ts = open(r'D:\uninexo\src\data\convocatoriasRegiones.ts', encoding='utf-8').read()
cargos = [m.replace("\\'", "'") for m in re.findall(r"cargo: '((?:[^'\\]|\\.)*)'", ts)]
print('cargos:', len(cargos))
cont = collections.Counter()
sin, muchas = [], []
for c in cargos:
    ca = reglas.carreras_de(c)
    for x in ca:
        cont[x] += 1
    if not ca:
        sin.append(c)
    if len(ca) >= 4:
        muchas.append((c, ca))
print('con alguna carrera:', len(cargos) - len(sin), '| sin ninguna:', len(sin))
for k, v in cont.most_common():
    print(f'  {v:3d}  {k}')
print('--- SIN carrera (muestra):')
for c in sorted(set(sin))[:45]:
    print('  ', c)
print('--- con 4 o más carreras (muestra):')
for c, ca in muchas[:14]:
    print('  ', c, '->', ca)
