"""Save settings for political and rule levels

Revision ID: 8fe786843072
Revises: 3517ac55b471
Create Date: 2019-04-16 14:00:41.259237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe786843072'
down_revision = '3517ac55b471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_settings', sa.Column('politics_levels', sa.ARRAY(sa.Integer()), nullable=True))
    op.add_column('users_rules', sa.Column('levels', sa.ARRAY(sa.Integer()), nullable=True))
    op.drop_column('users_rules', 'level')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_rules', sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('users_rules', 'levels')
    op.drop_column('user_settings', 'politics_levels')
    # ### end Alembic commands ###