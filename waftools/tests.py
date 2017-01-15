#! /usr/bin/env python
# encoding: utf-8
# Tim Mayberry, 2017

def options(opt):
    opt.add_option(
        '--with-tests',
        action='store_true',
        default=False,
        help='Enable Testsuite')
    opt.add_option(
        '--run-tests',
        action='store_true',
        default=False,
        help='Run testsuite after build')


def configure(conf):
    conf.env.WITH_TESTS = conf.options.with_tests
    conf.env.RUN_TESTS = conf.options.run_tests
