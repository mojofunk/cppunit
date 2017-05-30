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
    opt.load('toolset')
    opt.load('compiler_flags')
    opt.load('library')
    opt.load('tests')


def display_config(conf):
    Logs.info('Host System              : %s' % conf.env.HOST_SYSTEM)
    Logs.info('Toolset                  : %s' % conf.env.TOOLSET)
    Logs.info('C compiler flags         : %s' % conf.env.CFLAGS)
    Logs.info('C++ compiler flags       : %s' % conf.env.CXXFLAGS)
    Logs.info('Linker flags             : %s' % conf.env.LINKFLAGS)
    Logs.info('Enable shared            : %s' % conf.env.ENABLE_SHARED)
    Logs.info('Enable static            : %s' % conf.env.ENABLE_STATIC)
    Logs.info('Build tests              : %s' % conf.env.WITH_TESTS)
    Logs.info('Run tests                : %s' % conf.env.RUN_TESTS)


def configure(conf):
    conf.load('gnu_dirs')
    conf.load('toolset')
    conf.load('host_system')
    conf.load('compiler_flags')
    conf.load('library')
    conf.load('tests')
    conf.load('pkgconfig')

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

    if bld.env.HOST_SYSTEM_WINDOWS:
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=unix_sources)
    else:
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=windows_sources)

    if bld.env.ENABLE_SHARED:
        bld.shlib(
            includes=['include'],
            source=sources,
            target='cppunit',
            name='CPPUNIT_SHARED',
            vnum='0.0.2'
        )

    if bld.env.ENABLE_STATIC:
        bld.stlib(
            includes=['include'],
            source=sources,
            target='cppunit-static',
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

    if bld.env.RUN_TESTS:
        bld.add_post_fun(test)


def test(bld):
    pass
