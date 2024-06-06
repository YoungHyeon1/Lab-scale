from .base import Model
import sqlalchemy as sa

class Matches(Model):
    __tablename__ = 'matches'

    match_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    create_timestamp = sa.Column(sa.DateTime, nullable=False, index=True)
    start_timestamp = sa.Column(sa.DateTime, nullable=False, index=True)
    end_timestamp = sa.Column(sa.DateTime, nullable=False)
    game_name = sa.Column(sa.String(255), nullable=False)
    game_mode = sa.Column(sa.String(50), nullable=False, index=True)
    game_type = sa.Column(sa.String(50), nullable=False)
    map_id = sa.Column(sa.Integer(), nullable=False)
    duration = sa.Column(sa.Integer, nullable=False)
    game_version = sa.Column(sa.String(50), nullable=False)
    participants = sa.Column(sa.JSON, nullable=False)
    match_matches = sa.orm.relationship('MatchMatches', backref='matches')
