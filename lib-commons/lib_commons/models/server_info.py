import sqlalchemy as sa
from .base import Model

class Requests(Model):
    __tablename__ = 'requests'
    create_date = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    request_id = sa.Column(sa.String(78), primary_key=True, nullable=False)
    services = sa.Column(sa.String(255), nullable=False)
    ip = sa.Column(sa.String(255), nullable=False)
    status = sa.Column(sa.String(50), nullable=False)
    is_task = sa.Column(sa.Boolean, nullable=False, default=False)
    task = sa.orm.relationship("Task", back_populates="requests")


class Task(Model):
    __tablename__ = 'task'
    task_id = sa.Column(sa.String(78), primary_key=True, nullable=False)
    create_date = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    request_id = sa.Column(sa.String(78), sa.ForeignKey('requests.request_id'), nullable=False)
    status = sa.Column(sa.String(50), nullable=False)
    is_complete = sa.Column(sa.Boolean, nullable=False, default=False)
    requests = sa.orm.relationship("Requests", back_populates ="task")


