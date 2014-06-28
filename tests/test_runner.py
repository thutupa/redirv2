#!/usr/bin/python
import optparse
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
    print 'test_path = ', test_path
    suite = unittest.loader.TestLoader().discover(test_path, pattern='*_test.py')
    print 'suite = ', suite
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    import os
    SDK_PATH = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine'
    TEST_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    main(SDK_PATH, TEST_PATH)
