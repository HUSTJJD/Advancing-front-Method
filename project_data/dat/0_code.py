from pathlib import Path
p = Path('./')
files = list(p.glob('*.dat'))
for file in files:
    with open(file) as fi:
        lines = fi.readlines()
        lines[0] = str(len(lines)-1) + '\n'
        lines[len(lines)-1] = lines[1].replace('\n', '') + ' 0.0\n'
        for i in range(1, len(lines)-1):
            lines[i] = lines[i].replace('\n', '') + ' 0.0\n'
        with open(file, 'w+') as fo:
            fo.writelines(lines)
            fo.close()
        print(file)
        fi.close()
