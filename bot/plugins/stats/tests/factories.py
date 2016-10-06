from datetime import timedelta

from django.utils import timezone

import factory
import factory.fuzzy


class GameSessionFactory(factory.django.DjangoModelFactory):

    member = factory.SubFactory('bot.users.tests.factories.MemberFactory')
    game = factory.SubFactory('bot.games.tests.factories.GameFactory')

    start = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - timedelta(hours=1),
        end_dt=timezone.now() - timedelta(minutes=30)
    )
    stop = factory.fuzzy.FuzzyDateTime(start_dt=timezone.now() - timedelta(minutes=30))
    duration = factory.LazyAttribute(lambda o: o.stop - o.start)

    class Meta:
        model = 'stats.GameSession'
