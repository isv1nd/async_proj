import sqlalchemy as sa

metadata = sa.MetaData()


users = sa.Table(
    'users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String(255), nullable=False, unique=True),
    sa.Column('full_name', sa.String(255), nullable=True),
    sa.Column('pwd_hash', sa.String(511), nullable=True),
    sa.Column('is_active', sa.Boolean, nullable=False, server_default='TRUE')
)

