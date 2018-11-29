import factory


class UsersFactory(factory.DictFactory):
    full_name = factory.Faker('name')
    email = factory.Faker('email')
