#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

import sys

from waflib.Configure import conf

import compiler_checks

@conf
def set_toolset_from_compiler_check(self):
    print('Setting Toolset from compiler check')
    if self.compiler_is_clang():
        set_toolset_clang(self)
    elif self.compiler_is_msvc():
        set_toolset_msvc(self)
    else:
        set_toolset_gcc(self)


@conf
def check_toolset_clang(self):
    if not self.compiler_is_clang():
        print ("Clang compiler not detected")
        sys.exit(1)


@conf
def check_toolset_msvc(self):
    if not self.compiler_is_msvc():
        print ("MSVC compiler not detected")
        sys.exit(1)


@conf
def check_toolset_mingw(self):
    if not self.compiler_is_mingw():
        print ("MingW compiler/toolset not detected")
        sys.exit(1)


@conf
def set_toolset_gcc(self):
    self.env.TOOLSET = 'gcc'
    self.env.TOOLSET_GCC = True
    self.env.TOOLSET_CLANG = False
    self.env.TOOLSET_MSVC = False


@conf
def set_toolset_clang(self):
    self.env.TOOLSET = 'clang'
    self.env.TOOLSET_GCC = False
    self.env.TOOLSET_CLANG = True
    self.env.TOOLSET_MSVC = False


@conf
def set_toolset_msvc(self):
    self.env.TOOLSET = 'msvc'
    self.env.TOOLSET_GCC = False
    self.env.TOOLSET_CLANG = False
    self.env.TOOLSET_MSVC = True


@conf
def load_toolset(self):
    if self.env.TOOLSET == 'gcc':
        self.load('gcc')
        self.load('g++')
        set_toolset_gcc(self)
    elif self.env.TOOLSET == 'clang':
        self.load('clang')
        self.load('clang++')
        set_toolset_clang(self)
        check_toolset_clang(self)
    elif self.env.TOOLSET == 'msvc':
        self.load('msvc')
        set_toolset_msvc(self)
        check_toolset_msvc(self)
    elif self.env.TOOLSET == 'auto':
        self.load('compiler_c')
        self.load('compiler_cxx')
        set_toolset_from_compiler_check(self)
    else:
        print ("Unsupported Toolset option")
        sys.exit(1)


def options(opt):
    opt.add_option(
        '--toolset',
        type='string',
        dest='toolset',
        default='auto',
        help='Compiler and Toolset options: auto, gcc, clang, mingw, msvc')


def configure(self):
    self.env.TOOLSET = self.options.toolset
    self.load_toolset()
