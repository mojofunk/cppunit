#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

from waflib.Configure import conf

@conf
def compiler_is_clang(self):
    clang_check_source = '''
#ifndef __clang__
#error
#endif
int main() { return 0; }'''

    return self.check_cxx(fragment=clang_check_source,
                          features='cxx',
                          mandatory=False,
                          execute=False,
                          msg='Checking for clang compiler')


@conf
def compiler_is_msvc(self):
    msvc_check_source = '''
#ifndef _MSC_VER
#error
#endif
int main() { return 0; }'''

    return self.check_cxx(fragment=msvc_check_source,
                          features='cxx',
                          mandatory=False,
                          execute=False,
                          msg='Checking for msvc compiler')


@conf
def compiler_is_mingw(self):
    mingw_check_source = '''
#ifndef __MINGW32__
#error
#endif
int main() { return 0; }'''

    return self.check_cxx(fragment=mingw_check_source,
                          features='cxx',
                          mandatory=False,
                          execute=False,
                          msg='Checking for mingw compiler')


