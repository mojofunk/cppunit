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

    conf.check(header_name='dlfcn.h', define='CPPUNIT_HAVE_DLFCN_H')

    conf.define("CPPUNIT_HAVE_NAMESPACES", 1)

    display_config(conf)

    conf.write_config_header('config-auto.h')

def build(bld):
    includes = bld.path.ant_glob('include/cppunit/*')

    windows_sources = '''
    src/cppunit/DllMain.cpp
    src/cppunit/Win32DynamicLibraryManager.cpp
    '''

    unix_sources = '''
    src/cppunit/UnixDynamicLibraryManager.cpp
    '''

    defines = []

    if bld.env.DEST_OS == 'win32':
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=unix_sources)
        defines = ['WIN32', 'CPPUNIT_BUILD_DLL']
    else:
        sources = bld.path.ant_glob('src/cppunit/*.cpp', excl=windows_sources)
        bld.env.CXXFLAGS += ['-fPIC']


    if bld.env.ENABLE_SHARED != False:
        bld(features='c cxxshlib',
            includes=['include'],
            source=sources,
            target='cppunit',
            defines=defines,
            name='CPPUNIT_SHARED',
            vnum=VERSION
        )

    staticlib_name = 'cppunit'

    if bld.env.ENABLE_SHARED and bld.env.ENABLE_STATIC:
        if bld.env.CC_NAME == 'msvc':
            # Can't build shared and static with same name to due to
            # conflict with cppunit.lib(import library) and
            # cppunit.lib(static library), so use a different name
            staticlib_name = 'cppunit-static'

    if bld.env.ENABLE_STATIC != False:
        bld(features='c cxxstlib',
            includes=['include'],
            source=sources,
            target=staticlib_name,
            name='CPPUNIT_STATIC',
            vnum=VERSION
        )

    bld.install_files('${PREFIX}/include/cppunit', includes)
    bld.install_files('${PREFIX}/include/cppunit', ['config-auto.h'])

    bld(
        features='subst',
        source='cppunit.pc.in',
        target='cppunit.pc',
        install_path='${LIBDIR}/pkgconfig',
    )
