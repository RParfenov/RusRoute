import sqlalchemy as sa
import sqlalchemy.orm as orm

SqlAlchemyBase = orm.declarative_base()

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    cached_routes = orm.relationship('Route', back_populates='user', cascade='all, delete-orphan')

class RouteCache(SqlAlchemyBase):
    __tablename__ = 'route_cache'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True)

    city_from = sa.Column(sa.String(120), nullable=False, index=True)
    city_to = sa.Column(sa.String(120), nullable=False, index=True)
    date_start = sa.Column(sa.Date, nullable=False, index=True)

    transport = sa.Column(sa.String(120), nullable=False)
    cost = sa.Column(sa.Integer, nullable=False)
    time_hours = sa.Column(sa.Float, nullable=False)
    finish_date = sa.Column(sa.Date, nullable=False)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())

    user = sa.orm.relationship('User', back_populates='cached_routes')