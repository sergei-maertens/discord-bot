from datetime import datetime
from unittest import TestCase, mock

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from ..plugin import Plugin


class PluginTests(TestCase):

    def test_parse_time(self):
        plugin = Plugin(mock.MagicMock(), {})

        def expected(**kwargs):
            return (timezone.now() + relativedelta(**kwargs)).replace(microsecond=0)

        self.assertEqual(plugin.parse_time('30m'), expected(minutes=30))
        self.assertEqual(plugin.parse_time('30min'), expected(minutes=30))
        self.assertEqual(plugin.parse_time('30minutes'), expected(minutes=30))
        self.assertEqual(plugin.parse_time('1h'), expected(hours=1))
        self.assertEqual(plugin.parse_time('1hour'), expected(hours=1))
        self.assertEqual(plugin.parse_time('1hours'), expected(hours=1))
        self.assertEqual(plugin.parse_time('2days 4h 30m'), expected(days=2, hours=4, minutes=30))
        self.assertEqual(plugin.parse_time('5year 3months 2days 1hour'), expected(years=5, months=3, days=2, hours=1))

    def test_parse_absolute(self):
        plugin = Plugin(mock.MagicMock(), {})

        now = timezone.now()

        self.assertEqual(
            plugin.parse_time('21:00'),
            datetime(now.year, now.month, now.day, 21, 0).replace(tzinfo=timezone.utc)
        )
        self.assertEqual(
            plugin.parse_time('2016-11-01'),
            datetime(2016, 11, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
        )
        self.assertEqual(
            plugin.parse_time('2016-11-01 21:00'),
            datetime(2016, 11, 1, 21, 0).replace(tzinfo=timezone.utc)
        )

    def test_argument_regex_relative(self):
        """
        Test that the command can take both absolute and relative inputs.
        """
        plugin = Plugin(mock.MagicMock(), {})
        pattern = plugin.remindme._command.regex

        match = pattern.match('3days a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '3days')
        self.assertEqual(match.group('message'), 'a message')

        match = pattern.match('2hours 30min a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '2hours 30min')
        self.assertEqual(match.group('message'), 'a message')

        match = pattern.match('2h30m a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '2h30m')
        self.assertEqual(match.group('message'), 'a message')

    def test_argument_regex_absolute(self):
        """
        Test that the command can take both absolute and relative inputs.
        """
        plugin = Plugin(mock.MagicMock(), {})
        pattern = plugin.remindme._command.regex

        match = pattern.match('21:00 a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '21:00')
        self.assertEqual(match.group('message'), 'a message')

        match = pattern.match('2016-11-01 a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '2016-11-01')
        self.assertEqual(match.group('message'), 'a message')

        match = pattern.match('2016-11-01 21:00 a message')
        self.assertIsNotNone(match)
        self.assertEqual(match.group('time'), '2016-11-01 21:00')
        self.assertEqual(match.group('message'), 'a message')
