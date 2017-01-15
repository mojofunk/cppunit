#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

from waflib.Configure import conf


@conf
def pkgconfig_check_required_deps(self, deps):
    for pkg, version in deps.items():
        self.check_cfg(package=pkg, atleast_version=version, mandatory=1)
        self.check_cfg(package=pkg, args='--cflags --libs')


@conf
def pkgconfig_check_optional_deps(self, deps):
    for pkg, version in deps.items():
        self.check_cfg(package=pkg, atleast_version=version, mandatory=0)
        self.check_cfg(package=pkg, args='--cflags --libs')
