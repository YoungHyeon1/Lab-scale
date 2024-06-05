from .base import Model
import sqlalchemy as sa

user_matches = sa.Table('user_matches', Model.metadata,
    sa.Column('user_id', sa.ForeignKey('users.puuid'), primary_key=True),
    sa.Column('match_id', sa.ForeignKey('matches.match_id'), primary_key=True)
)
