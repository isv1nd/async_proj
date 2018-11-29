import factory


class UsersFactory(factory.DictFactory):
    full_name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('pystr', min_chars=6, max_chars=20)
