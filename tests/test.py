
from treewatcher import run_watch_files
from subprocess import Popen

def proc():
    proc = Popen(
        ['gcc', '-o', 'test.o', '-c', 'test.c'],
        cwd = '.'
    )
    
    proc.wait()

_, mods = run_watch_files(proc, '.')

print(mods)

