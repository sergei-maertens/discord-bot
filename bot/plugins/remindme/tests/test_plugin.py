from unittest import TestCase, mock

from dateutil.relativedelta import relativedelta

from ..plugin import Plugin


class PluginTests(TestCase):

    def test_parse_delta(self):
        plugin = Plugin(mock.MagicMock(), {})

        self.assertEqual(plugin.parse_delta('30m'), relativedelta(minutes=30))
        self.assertEqual(plugin.parse_delta('1h'), relativedelta(hours=1))
        self.assertEqual(plugin.parse_delta('2days4h30m'), relativedelta(days=2, hours=4, minutes=30))
        self.assertEqual(
            plugin.parse_delta('5year3months2days1hour'),
            relativedelta(years=5, months=3, days=2, hours=2)
        )
