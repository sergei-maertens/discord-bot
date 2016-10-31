from unittest import TestCase, mock

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from ..plugin import Plugin


class PluginTests(TestCase):

    def test_parse_delta(self):
        plugin = Plugin(mock.MagicMock(), {})

        def expected(**kwargs):
            return (timezone.now() + relativedelta(**kwargs)).replace(microsecond=0)

        self.assertEqual(plugin.parse_delta('30m'), expected(minutes=30))
        self.assertEqual(plugin.parse_delta('30min'), expected(minutes=30))
        self.assertEqual(plugin.parse_delta('30minutes'), expected(minutes=30))
        self.assertEqual(plugin.parse_delta('1h'), expected(hours=1))
        self.assertEqual(plugin.parse_delta('1hour'), expected(hours=1))
        self.assertEqual(plugin.parse_delta('1hours'), expected(hours=1))
        self.assertEqual(plugin.parse_delta('2days 4h 30m'), expected(days=2, hours=4, minutes=30))
        self.assertEqual(plugin.parse_delta('5year 3months 2days 1hour'), expected(years=5, months=3, days=2, hours=1))
