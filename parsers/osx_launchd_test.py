#!/usr/bin/env python
# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for grr.parsers.osx_launchd."""



from grr.lib import flags
from grr.lib import test_lib
from grr.parsers import osx_launchd
from grr.test_data import osx_launchd as testdata


class OSXLaunchdJobDictTest(test_lib.GRRBaseTest):

  def setUp(self):
    super(OSXLaunchdJobDictTest, self).setUp()
    self.jobdict = testdata.JOBS
    self.parser = osx_launchd.OSXLaunchdJobDict(self.jobdict)

  def testParseRegex(self):
    filtered = 0
    unfiltered = 0
    for job in self.jobdict:
      if self.parser.FilterItem(job):
        filtered += 1
        self.assertTrue(job['Label'].startswith('0x'), job['Label'])
      else:
        unfiltered += 1
        self.assertFalse(job['Label'].startswith('0x'), job['Label'])
        self.assertFalse('anonymous' in job['Label'], job['Label'])
        self.assertFalse('mach_init.crash_inspector' in job['Label'],
                         job['Label'])

    self.assertEqual(filtered, testdata.FILTERED_COUNT)
    self.assertEqual(unfiltered, len(testdata.JOBS) - testdata.FILTERED_COUNT)


def main(argv):
  test_lib.main(argv)


if __name__ == '__main__':
  flags.StartMain(main)
