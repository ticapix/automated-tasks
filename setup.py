#!/usr/bin/env python3
import os
import glob
import pip
import sys

rootpath = os.path.abspath(os.path.dirname(__file__))

def install_requirements(rootpath):
    for requirements in glob.glob(os.path.join(rootpath, '*', 'requirements.txt')):
        print(requirements)
        with open(requirements) as fd:
            for line in fd:
                line = line.strip('\n\r')
                print('installing', line)
                ans = pip.main(['install', line])
                if ans != 0:
                    return ans

if __name__ == '__main__':
    if install_requirements(rootpath) != 0:
        sys.exit(1)
