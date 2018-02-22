#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

import os
import subprocess
import sys
import re

from waflib import Logs

CPPUNIT_MAJOR_VERSION = '1'
CPPUNIT_MINOR_VERSION = '13'
CPPUNIT_MICRO_VERSION = '0'
CPPUNIT_VERSION = '%s.%s.%s' % (CPPUNIT_MAJOR_VERSION, CPPUNIT_MINOR_VERSION, CPPUNIT_MICRO_VERSION)

# these are required by waf for waf dist
VERSION = CPPUNIT_VERSION
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

    conf.check(header_name='dlfcn.h', define='CPPUNIT_HAVE_DLFCN_H', mandatory=False)

    if conf.check_cxx(header_name='sstream'):
        conf.define("CPPUNIT_HAVE_SSTREAM", 1)


    conf.define("CPPUNIT_HAVE_NAMESPACES", 1)
    conf.define("CPPUNIT_PACKAGE", "cppunit")

    display_config(conf)

    conf.write_config_header('include/cppunit/config-auto.h')

def build(bld):
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


    if bld.env.ENABLE_SHARED != False:
        bld(features='cxx cxxshlib',
            includes=['include'],
            source=sources,
            target='cppunit',
            defines=defines,
            name='CPPUNIT_SHARED',
            vnum=CPPUNIT_VERSION
        )

    staticlib_name = 'cppunit'

    if bld.env.ENABLE_SHARED and bld.env.ENABLE_STATIC:
        if bld.env.CC_NAME == 'msvc':
            # Can't build shared and static with same name to due to
            # conflict with cppunit.lib(import library) and
            # cppunit.lib(static library), so use a different name
            staticlib_name = 'cppunit-static'

    if bld.env.ENABLE_STATIC != False:
        bld(features='cxx cxxstlib',
            includes=['include'],
            source=sources,
            target=staticlib_name,
            name='CPPUNIT_STATIC',
            vnum=CPPUNIT_VERSION
        )

    # There is an assumption in the name of the includedir here
    includes = bld.path.ant_glob('include/cppunit/**/*.h')
    bld.install_files('${PREFIX}', includes, relative_trick=True)

    bld.install_files('${PREFIX}/include/cppunit', ['include/cppunit/config-auto.h'])

    bld.env.CPPUNIT_VERSION = CPPUNIT_VERSION
    bld(
        features='subst',
        source='cppunit.pc.in',
        target='cppunit.pc',
        install_path='${LIBDIR}/pkgconfig',
    )
