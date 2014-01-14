"""Tests for time_parser module."""

import datetime
import unittest

import time_parser


class TimeParserTest(unittest.TestCase):

  def setUp(self):
    pass

  def testIsAvailable(self):
    friday_3pm = datetime.datetime(2014, 1, 10, 15, 0)
    self.assertTrue(
        time_parser.IsAvailable(friday_3pm, 'every fri'))
    self.assertTrue(
        time_parser.IsAvailable(friday_3pm, 'every fri time: 8:00 AM-5:00 PM'))
    self.assertTrue(
        time_parser.IsAvailable(
            friday_3pm, 'every fri date: 10/1/2014 time: 8:00 AM-5:00 PM'))
    self.assertTrue(
        time_parser.IsAvailable(
            friday_3pm, 'date: 1/1/2014-15/1/2014 time: 8:00 AM-5:00 PM'))
    self.assertFalse(
        time_parser.IsAvailable(friday_3pm, 'every weekend'))
    self.assertFalse(
        time_parser.IsAvailable(friday_3pm, 'every day time: 8:00 AM-1:00 PM'))
    self.assertRaises(
        time_parser.ParseError,
        time_parser.IsAvailable, friday_3pm, 'every day time: 8:00 AM-15:00 PM')


if __name__ == '__main__':
  unittest.main()
