#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017


def options(opt):
    opt.add_option(
        '--enable-shared',
        action='store_true',
        default=False,
        help='Build shared libraries')
    opt.add_option(
        '--enable-static',
        action='store_true',
        default=False,
        help='Build static libraries')


def configure(conf):
    conf.env.ENABLE_SHARED = conf.options.enable_shared
    conf.env.ENABLE_STATIC = conf.options.enable_static

    if not conf.env.ENABLE_SHARED and not conf.env.ENABLE_STATIC:
        # needed because of the weird waf options design
        conf.env.ENABLE_SHARED = True
