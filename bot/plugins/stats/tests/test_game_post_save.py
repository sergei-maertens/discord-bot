from django.test import TestCase

from bot.games.tests.factories import GameFactory

from .factories import GameSessionFactory


class GamePostSaveTests(TestCase):

    def test_game_session_updated_if_game_is_alias(self):
        gta_v = GameFactory.create(name='Grand Theft Auto V')
        gta_v2 = GameFactory.create(name='GTA V')

        session = GameSessionFactory.create(game=gta_v)
        self.assertEqual(session.game.name, 'Grand Theft Auto V')

        session2 = GameSessionFactory.create(game=gta_v2)
        self.assertEqual(session2.game.name, 'GTA V')

        gta_v2.alias_for = gta_v
        gta_v2.save()

        session2.refresh_from_db()
        self.assertEqual(session2.game, gta_v)
