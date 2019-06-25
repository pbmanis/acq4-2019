#!/usr/bin/python
"""
Script for compiling Qt Designer .ui files to .py



"""
import os, sys, subprocess, tempfile
import argparse

pyqt4uic = 'pyuic4'
pysideuic = 'pyside2-uic'
pyqt5uic = 'pyuic5'
compilers = {'pyqt4': 'pyuic4', 'pyqt5': 'pyuic5', 'pyside': 'pyside2-uic'}
compilersext = {'pyqt4': '_pyqt4.py', 'pyqt5': '_pyqt5.py', 'pyside': 'pyside.py'}
usage = """Compile .ui files to .py for all supported pyqt/pyside versions.

  Usage: python rebuildUi.py pyversion, [--force] -d [.ui files|search paths]

  May specify a list of .ui files and/or directories to search recursively for .ui files.
"""
parser = argparse.ArgumentParser(description='Rebuild the UI files')
parser.add_argument('pyversion', type=str, default='pyqt5', choices=['pyqt4', 'pyqt5', 'pyside'],
                    help='Select pyside, pyqt4 or pyqt5 version')
parser.add_argument('-f', '--force', action='store_true',
                        help='Force')                    
parser.add_argument('-d', '--directory', type=str, default=None, nargs='*',
                        help='Starting directoyr')

args = parser.parse_args()


if args.force:
    force = True
else:
    force = False

    
uifiles = []
for arg in args.directory:
    if os.path.isfile(arg) and arg.endswith('.ui'):
        uifiles.append(arg)
    elif os.path.isdir(arg):
        # recursively search for ui files in this directory
        for path, sd, files in os.walk(arg):
            for f in files:
                if not f.endswith('.ui'):
                    continue
                uifiles.append(os.path.join(path, f))
    else:
        print('Argument "%s" is not a directory or .ui file.' % arg)
        sys.exit(-1)

print('uifiles: ', uifiles)



# rebuild all requested ui files
for ui in uifiles:
    base, _ = os.path.splitext(ui)
    compiler = args.pyversion
    ext = compilersext[compiler]
    print('compiler, ext: ', compiler, ext)
    # for compiler, ext in [(pyqt4uic, '_pyq4t.py'), (pysideuic, '_pyside.py'), (pyqt5uic, '_pyqt5.py')]:
    pylong = base + ext
    pyshort = base + '.py'
    if not force and os.path.exists(pylong) and os.stat(ui).st_mtime <= os.stat(pylong).st_mtime:
        pass
        # print("Skipping %s; already compiled." % py)
    else:
        cmd = '%s %s > %s' % (compilers[compiler], ui, pyshort)
        print(cmd)
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError:
            print('Failed to compile: ', pylong, pyshort)  # no support for that one
            # os.remove(pylong)
