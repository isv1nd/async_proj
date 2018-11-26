import factory


class UsersFactory(factory.DictFactory):
    name = factory.Faker('name')
    birthday = factory.Faker('date')
