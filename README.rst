
Treewatcher
===========

``treewatcher`` is a python module for watching which files are accessed and
modified while performing an operation. The target use is tracking dependencies
in an incremental build.

Installation
------------

::

    sudo python setup.py install

Dependencies
------------

``treewatcher`` uses `pyinotify <https://github.com/seb-m/pyinotify>`_ to watch
files. This means:

1. ``treewatcher`` will only run on Linux
   
2. ``treewatcher`` will only run on those versions of Linux on which
   ``pyinotify`` will run.

Using
-----

``treewatcher`` uses one function: ``run_watch_files``. Pass it the command to
run and the directory to watch. As an example::

    from treewatcher import run_watch_files
    from subprocess import Popen

    def proc():
        proc = Popen(
            ['touch', 'foo'],
            cwd = '.'
        )
        proc.wait()

    _, mods = run_watch_files(proc, '.')

    print(mods)

Also see the docstring for the function ``run_watch_files``.

