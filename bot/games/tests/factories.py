import factory


class GameFactory(factory.django.DjangoModelFactory):

    name = factory.Faker('bs')

    class Meta:
        model = 'games.Game'
