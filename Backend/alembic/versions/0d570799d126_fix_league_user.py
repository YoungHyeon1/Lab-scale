"""fix_league_user

Revision ID: 0d570799d126
Revises: a83bfc781081
Create Date: 2024-06-09 00:38:39.245042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d570799d126'
down_revision: Union[str, None] = 'a83bfc781081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('league', sa.Column('name', sa.String(length=255), nullable=True))
    op.drop_column('league', 'league_points')
    op.drop_column('league', 'veteran')
    op.drop_column('league', 'losses')
    op.drop_column('league', 'hot_streak')
    op.drop_column('league', 'fresh_blood')
    op.drop_column('league', 'inactive')
    op.drop_column('league', 'rank')
    op.drop_column('league', 'wins')
    op.add_column('user_leagues', sa.Column('league_points', sa.Integer(), nullable=True))
    op.add_column('user_leagues', sa.Column('rank', sa.String(length=10), nullable=True))
    op.add_column('user_leagues', sa.Column('wins', sa.Integer(), nullable=True))
    op.add_column('user_leagues', sa.Column('losses', sa.Integer(), nullable=True))
    op.add_column('user_leagues', sa.Column('veteran', sa.Boolean(), nullable=True))
    op.add_column('user_leagues', sa.Column('inactive', sa.Boolean(), nullable=True))
    op.add_column('user_leagues', sa.Column('fresh_blood', sa.Boolean(), nullable=True))
    op.add_column('user_leagues', sa.Column('hot_streak', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_leagues', 'hot_streak')
    op.drop_column('user_leagues', 'fresh_blood')
    op.drop_column('user_leagues', 'inactive')
    op.drop_column('user_leagues', 'veteran')
    op.drop_column('user_leagues', 'losses')
    op.drop_column('user_leagues', 'wins')
    op.drop_column('user_leagues', 'rank')
    op.drop_column('user_leagues', 'league_points')
    op.add_column('league', sa.Column('wins', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('rank', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('inactive', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('fresh_blood', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('hot_streak', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('losses', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('veteran', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('league', sa.Column('league_points', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('league', 'name')
    # ### end Alembic commands ###
