import factory


class MemberFactory(factory.django.DjangoModelFactory):

    discord_id = factory.Sequence(lambda n: n, type=str)
    name = factory.Faker('user_name')

    class Meta:
        model = 'users.Member'
