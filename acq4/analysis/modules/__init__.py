# -*- coding: utf-8 -*-
from __future__ import print_function
import os

def listModules():
    d = os.path.split(__file__)[0]
    files = []
    for f in os.listdir(d):
        if os.path.isdir(os.path.join(d, f)):
            files.append(f)
        elif f[-3:] == '.py' and f != '__init__.py' and f != '__pycache__':
            files.append(f[:-3])
    files.sort()
    return files
    
def getModuleClass(modName):
    mod = __import__('acq4.analysis.modules.'+modName, fromlist=['*'])
    try:
        modcls = getattr(mod, modName)
    except:
        modcls = None
    #print id(cls)
    return modcls

def load(modName, host):
    modcls = getModuleClass(modName)
    if modcls is not None:
        return modcls(host)
    else:
        return None