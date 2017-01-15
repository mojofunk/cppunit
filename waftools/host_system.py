#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

import sys

from waflib.Configure import conf

import compiler_checks

@conf
def set_host_system(self):
    print('Setting host system from compiler check')
    if self.compiler_is_mingw() or self.compiler_is_msvc():
        self.env.HOST_SYSTEM = 'Windows'
        self.env.HOST_SYSTEM_WINDOWS = True
        self.env.HOST_SYSTEM_LINUX = False
    else:
        self.env.HOST_SYSTEM = 'Linux'
        self.env.HOST_SYSTEM_WINDOWS = False
        self.env.HOST_SYSTEM_LINUX = True


def configure(self):
    self.set_host_system()
