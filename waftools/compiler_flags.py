#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

from waflib.Configure import conf

import compiler_checks
import toolset


def options(opt):
    opt.add_option(
        '--optimize',
        action='store_true',
        default=False,
        help='Enable Optimization')

@conf
def set_gcc_compiler_flags(self):
    cxx_flags = []
    self.check_cxx(cxxflags=["-std=c++11"])
    cxx_flags.append('-std=c++11')

    self.env.append_value('CXXFLAGS', cxx_flags)

    if self.options.optimize:
        self.env.append_value('CFLAGS', '-DNDEBUG')
        self.env.append_value('CXXFLAGS', '-DNDEBUG')
    else:
        self.env.append_value('CFLAGS', '-g')
        self.env.append_value('CXXFLAGS', '-g')


@conf
def set_msvc_compiler_flags(self):
    # much more to do here
    cxx_debug_flags = ['/DEBUG', '/Od', '/MD', '/Zi', '/EHsc']
    link_flags = ['/DEBUG']
    # enable exceptions
    self.env.append_value('CXXFLAGS', cxx_debug_flags)
    self.env.append_value('LINKFLAGS', link_flags)


@conf
def set_compiler_flags(self):
    if self.env.TOOLSET_GCC:
        set_gcc_compiler_flags(self)
    if self.env.TOOLSET_CLANG:
        set_gcc_compiler_flags(self)
    elif self.env.TOOLSET_MSVC:
        set_msvc_compiler_flags(self)


def configure(self):
    self.set_compiler_flags()
