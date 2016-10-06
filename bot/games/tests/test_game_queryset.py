from django.test import TestCase

from ..models import Game


class QuerySetTests(TestCase):

    def test_get_by_name(self):

        gta_v = Game.objects.create(name='GTA V')
        Game.objects.create(name='Grand Theft Auto V', alias_for=gta_v)

        game = Game.objects.get_by_name('gta V')
        self.assertEqual(game, gta_v)

        game2 = Game.objects.get_by_name('Grand Theft Auto V')
        self.assertEqual(game2, gta_v)

        # non-existing game should be created
        overwatch = Game.objects.get_by_name('Overwatch')
        self.assertIsNotNone(overwatch.pk)
