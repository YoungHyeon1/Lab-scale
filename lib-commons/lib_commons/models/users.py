from .base import Model
import sqlalchemy as sa

class Users(Model):
    __tablename__ = 'users'
    puuid = sa.Column(sa.String(78), nullable=False, primary_key=True)
    sommoner_id = sa.Column(sa.String(78), index=True, nullable=False)
    league_id = sa.Column(sa.String(78), nullable=False, index=True)
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