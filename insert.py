import os


with open('insert.txt', 'r') as f:
    lines = filter(None, (line.rstrip() for line in f))
    for line in lines:
        (key,value) = [s.strip() for s in line.split(',')]
        os.system('ls -l')