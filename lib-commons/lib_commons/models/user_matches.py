from .base import Model
import sqlalchemy as sa

user_matches = sa.Table('user_matches', Model.metadata,
    sa.Column('user_id', sa.ForeignKey('users.puuid'), primary_key=True),
    sa.Column('match_id', sa.ForeignKey('matches.match_id'), primary_key=True)
)

user_leagues = sa.Table('user_leagues', Model.metadata,
    sa.Column('summoner_id', sa.ForeignKey('users.summoner_id'), primary_key=True),
    sa.Column('league_id', sa.ForeignKey('league.league_id'), primary_key=True),
    sa.Column('league_points', sa.Integer),
    sa.Column('rank', sa.String(10)),
    sa.Column('wins', sa.Integer),
    sa.Column('losses', sa.Integer),
    sa.Column('veteran', sa.Boolean),
    sa.Column('inactive', sa.Boolean),
    sa.Column('fresh_blood', sa.Boolean),
    sa.Column('hot_streak', sa.Boolean)
)

class Matches(Model):
    __tablename__ = 'matches'

    match_id = sa.Column(sa.String(15), primary_key=True, nullable=False)
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
    users = sa.orm.relationship("Users", secondary=user_matches, back_populates="matches")


class Users(Model):
    __tablename__ = 'users'
    puuid = sa.Column(sa.String(78), nullable=False, primary_key=True)
    summoner_id = sa.Column(sa.String(78), index=True, nullable=False, unique=True)
    accountId= sa.Column(sa.String(78), index=True, nullable=True)
    profile_icon_id = sa.Column(sa.Integer(), nullable=True)
    revision_date = sa.Column(sa.DateTime, nullable=True)
    summoner_level = sa.Column(sa.Integer(), nullable=True)
    matches = sa.orm.relationship("Matches", secondary=user_matches, back_populates='users')
    league = sa.orm.relationship("League", secondary=user_leagues, back_populates='summoner')

class League(Model):
    __tablename__ = 'league'

    league_id = sa.Column(sa.String(78), primary_key=True, nullable=False)
    queue_type = sa.Column(sa.String(50), nullable=False)
    tier = sa.Column(sa.String(50), nullable=True)
    name = sa.Column(sa.String(255), nullable=True)
    summoner = sa.orm.relationship("Users", secondary=user_leagues, back_populates="league")
