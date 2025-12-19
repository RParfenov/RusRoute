from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Float, func, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

SqlAlchemyBase = declarative_base()

class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    viewed_routes = relationship('UserViewedRoute', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Route(SqlAlchemyBase):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    city_from = Column(String(120), nullable=False, index=True)
    city_to = Column(String(120), nullable=False, index=True)
    date_start = Column(String(10), nullable=False, index=True)
    cost_image_path = Column(String(120), nullable=False)
    time_image_path = Column(String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint('city_from', 'city_to', 'date_start'),
    )

    viewers = relationship('UserViewedRoute', back_populates='route', cascade='all, delete-orphan')

class UserViewedRoute(SqlAlchemyBase):
    __tablename__ = 'user_viewed_routes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    route_id = Column(Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False, index=True)
    viewed_at = Column(DateTime, default=func.now())

    user = relationship('User', back_populates='viewed_routes')
    route = relationship('Route', back_populates='viewers')