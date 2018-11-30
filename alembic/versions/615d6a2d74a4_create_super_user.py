"""create super user

Revision ID: 615d6a2d74a4
Revises: 269850db03df
Create Date: 2018-11-30 17:10:38.720373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615d6a2d74a4'
down_revision = '269850db03df'
branch_labels = None
depends_on = None

USER_EMAIL = "admin@admin.ru"
USER_PASSWORD_HASH = "$5$rounds=535000$CLy2KrHo3JXmV5vY$/H3L0CS3a6wUKbJTeC7t8ogiPDX6Td7E60Q5M9b13p."


def upgrade():
    user_table = sa.Table('users', sa.MetaData(bind=op.get_bind()),
                          autoload=True)
    op.get_bind().execute(
        user_table.insert().values(
            {"email": USER_EMAIL,
             "pwd_hash": USER_PASSWORD_HASH,
             "full_name": "Admin"}
        )
    )


def downgrade():
    user_table = sa.Table('users', sa.MetaData(bind=op.get_bind()),
                          autoload=True)
    op.get_bind().execute(user_table.delete().where(email=USER_EMAIL))
