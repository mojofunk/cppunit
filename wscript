#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

import os
import subprocess
import sys
import re

from waflib import Logs

MAJOR_VERSION = '1'
MINOR_VERSION = '13'
MICRO_VERSION = '0'
# these are required by waf for waf dist
VERSION = MAJOR_VERSION + '.' + MINOR_VERSION + '.' + MICRO_VERSION
APPNAME = 'cppunit'

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = 'waf-build'


def options(opt):
    # options provided by the modules
    opt.load('compiler_c')
    opt.load('compiler_cxx')
    opt.load('gnu_dirs')
    opt.load('build_type')
    opt.load('library')


def display_config(conf):
    conf.msg('Host System', conf.env.DEST_OS)
    conf.msg('C compiler flags', conf.env.CFLAGS)
    conf.msg('C++ compiler flags', conf.env.CXXFLAGS)
    conf.msg('Linker flags', conf.env.LINKFLAGS)
    conf.msg('Enable shared', str(conf.env.ENABLE_SHARED))
    conf.msg('Enable static', str(conf.env.ENABLE_STATIC))


def configure(conf):
    conf.load('compiler_c')
    conf.load('compiler_cxx')
    conf.load('gnu_dirs')
    conf.load('build_type')
    conf.load('library')

    display_config(conf)


def build(bld):
    includes = bld.path.ant_glob('includes/*')

    windows_sources = '''
    src/cppunit/DllMain.cpp
    src/cppunit/Win32DynamicLibraryManager.cpp
    '''

    unix_sources = '''
    src/cppunit/UnixDynamicLibraryManager.cpp
    '''

    if bld.env.DEST_OS == 'win32':
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=unix_sources)
    else:
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=windows_sources)

    if bld.env.ENABLE_SHARED != False:
        bld.shlib(
            includes=['include'],
            source=sources,
            target='cppunit',
            name='CPPUNIT_SHARED',
            vnum='0.0.2'
        )

    if bld.env.ENABLE_STATIC != False:
        bld.stlib(
            includes=['include'],
            source=sources,
            target='cppunit',
            name='CPPUNIT_STATIC',
            vnum='0.0.2'
        )

    bld.install_files('${PREFIX}/include', includes)

    bld(
        features='subst',
        source='cppunit.pc.in',
        target='cppunit.pc',
        install_path='${PREFIX}/lib/pkgconfig',
    )
