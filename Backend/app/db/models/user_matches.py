from .base import Model
import sqlalchemy as sa

class UserMatches(Model):
    __tablename__ = 'user_matches'

    user_id = sa.Column(sa.String(78), sa.ForeignKey('users.sommoner_id'), nullable=False)
    match_id = sa.Column(sa.Integer, sa.ForeignKey('matches.match_id'), nullable=False)
