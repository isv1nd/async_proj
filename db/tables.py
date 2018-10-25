import sqlalchemy as sa

metadata = sa.MetaData()


users = sa.Table('users', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('name', sa.String(255)),
                 sa.Column('birthday', sa.DateTime))

emails = sa.Table('emails', metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('user_id', None, sa.ForeignKey('users.id')),
                  sa.Column('email', sa.String(255), nullable=False),
                  sa.Column('private', sa.Boolean, nullable=False))
