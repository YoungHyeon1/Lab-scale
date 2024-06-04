from .base import Model
import sqlalchemy as sa

class Users(Model):
    sommoner_id = sa.Column(sa.String(78),primary_key=True, nullable=False)
    league_id = sa.Column(sa.String(78), nullable=False)
    tier = sa.Column(sa.String(50), nullable=False)
    rank = sa.Column(sa.String(50), nullable=False)
    leaguePoints = sa.Column(sa.Integer, nullable=False)
    win= sa.Column(sa.Integer, nullable=False)
    losses = sa.Column(sa.Integer, nullable=False)
    veteran = sa.Column(sa.Boolean, nullable=False)
    incative = sa.Column(sa.Boolean, nullable=False)
    fresh_blood = sa.Column(sa.Boolean, nullable=False)
    hot_streak = sa.Column(sa.Boolean, nullable=False)
    user_matches = sa.orm.relationship('UserMatches', backref='users')