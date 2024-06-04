from .base import Model
import sqlalchemy as sa

class Matches(Model):
    __tablename__ = 'matches'

    match_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    start_timestamp = sa.Column(sa.DateTime, nullable=False)
    game_mode = sa.Column(sa.String(50), nullable=False)
    duration = sa.Column(sa.Integer, nullable=False)
    game_version = sa.Column(sa.String(50), nullable=False)
    match_matches = sa.orm.relationship('MatchMatches', backref='matches')
