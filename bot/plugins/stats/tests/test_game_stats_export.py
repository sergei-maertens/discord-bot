from datetime import timedelta

from django.test import TestCase

from .factories import GameSessionFactory
from ..models import GameSession
from ..resources import GamesPlayedResource


class ExportTests(TestCase):

    def test_export_correctly(self):
        GameSessionFactory.create(game__name='Overwatch', duration=timedelta(hours=1))
        GameSessionFactory.create(game__name='Overwatch', duration=timedelta(minutes=30))
        GameSessionFactory.create(game__name='Battlefield 4', duration=timedelta(minutes=30))
        GameSessionFactory.create(game__name='Battlefield 4', duration=timedelta(minutes=30))
        GameSessionFactory.create(game__name='Battlefield 4', duration=timedelta(hours=1))

        queryset = GameSession.objects.get_game_durations()
        resource = GamesPlayedResource()

        dataset = resource.export(queryset)
        self.assertEqual(dataset.headers, ['game', 'time (hours)', 'num_players'])
        self.assertEqual(dataset[0], ('Battlefield 4', 2, 3))
        self.assertEqual(dataset[1], ('Overwatch', 1.5, 2))
