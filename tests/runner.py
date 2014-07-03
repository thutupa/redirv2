#!/usr/bin/python
import optparse
import os
import sys
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path, pattern='*_test.py')
    unittest.TextTestRunner(verbosity=2).run(suite)


def DiscoverSDKPath():
    BINARY = 'dev_appserver.py'
    for pathdir in os.environ['PATH'].split(':'):
        if not pathdir:
            pathdir = os.getcwd()
        binary_path = os.path.join(pathdir, BINARY)
        if os.path.exists(binary_path):
            binary_path = os.path.realpath(binary_path)
            return os.path.dirname(binary_path)
    raise Exception('Could not discover SDK Path')

if __name__ == '__main__':
    SDK_PATH = DiscoverSDKPath()
    TEST_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    main(SDK_PATH, TEST_PATH)
