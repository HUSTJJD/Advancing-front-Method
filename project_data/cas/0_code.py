import os
path = './in-100-out-50-front'
filenames = []
for  a, b,files in os.walk('../dat/'):
    for filename in files:
        if os.path.splitext(filename)[1] == '.dat':
            filenames.append(os.path.splitext(filename)[0])
print(filenames)
os.chdir(path)
for filename in filenames[1:-1]:
    os.mkdir(filename)