from .base import Model
import sqlalchemy as sa
from .user_matches import user_matches

class Users(Model):
    __tablename__ = 'users'
    puuid = sa.Column(sa.String(78), nullable=False, primary_key=True)
    summoner_id = sa.Column(sa.String(78), index=True, nullable=False)
    league_id = sa.Column(sa.String(78), nullable=True, index=True)
    tier = sa.Column(sa.String(50), nullable=True)
    rank = sa.Column(sa.String(50), nullable=True)
    leaguePoints = sa.Column(sa.Integer, nullable=True)
    win= sa.Column(sa.Integer, nullable=True)
    losses = sa.Column(sa.Integer, nullable=True)
    veteran = sa.Column(sa.Boolean, nullable=True)
    incative = sa.Column(sa.Boolean, nullable=True)
    fresh_blood = sa.Column(sa.Boolean, nullable=True)
    hot_streak = sa.Column(sa.Boolean, nullable=True)
    matches = sa.orm.relationship("Matches", secondary=user_matches, back_populates='users')
