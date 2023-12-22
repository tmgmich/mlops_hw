from datetime import datetime
from enum import Enum
import sqlalchemy as sa
import sqlalchemy.orm as orm
from .sa_db import Base
from .dataframes_obj import ChooseUrModel

class DataFrame(Base):
    __tablename__ = "dataframe"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    description = sa.Column(sa.String)
    target = sa.Column(sa.String, default="target", nullable=False)
    created_date = sa.Column(sa.DateTime, default = datetime.utcnow)
    model = orm.relationship("Model", back_populates = "dataframe")

class Model(Base):
    __tablename__ = "model"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    dataframe_id = sa.Column(sa.Integer, sa.ForeignKey("dataframe.id"))
    description = sa.Column(sa.String)
    type = sa.Column(sa.Enum(ChooseUrModel), nullable=False)
    created_date = sa.Column(sa.DateTime, default = datetime.utcnow)
    dataframe = orm.relationship("DataFrame", back_populates="model")