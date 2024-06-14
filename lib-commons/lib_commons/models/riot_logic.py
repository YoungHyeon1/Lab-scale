import sqlalchemy as sa
from .base import Model


class APIKeyUsage(Model):
    __tablename__ = 'api_key_usage'
    create_date = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    api_key = sa.Column(sa.String(78), primary_key=True, nullable=False)
    services = sa.Column(sa.String(255), nullable=False)
    last_update = sa.Column(sa.DateTime, nullable=False)
    count = sa.Column(sa.Integer, nullable=False, default=0)
