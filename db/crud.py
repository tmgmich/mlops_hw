import sqlalchemy.orm as orm
from .models import DataFrame, Model
from .dataframes_obj import DataFrameCreate, ModelCreate

def get_dataframe(db: orm.Session, dataframe_id: int) -> DataFrame:
    return db.query(DataFrame).filter(DataFrame.id == dataframe_id).first()

def get_dataframes(db: orm.Session, skip: int = 0, limit: int = 100) -> list[DataFrame]:
    return db.query(DataFrame).offset(skip).limit(limit).all()

def delete_dataframe(db: orm.Session, dataframe_id: int):
    db.query(DataFrame).filter(DataFrame.id == dataframe_id).delete()
    db.commit()

def create_dataframe(db: orm.Session, dataframe: DataFrameCreate) -> DataFrame:
    dataframe_og = DataFrame(**dataframe.model_dump())
    db.add(dataframe_og)
    db.commit()
    db.refresh(dataframe_og)
    return dataframe_og

def get_model(db: orm.Session, model_id: int) -> Model:
    return db.query(Model).filter(Model.id == model_id).first()

def get_models(db: orm.Session, skip: int = 0, limit: int = 100) -> list[Model]:
    return db.query(Model).offset(skip).limit(limit).all()

def create_model(db: orm.Session, model: ModelCreate) -> Model:
    model_og = Model(**model.model_dump())
    db.add(model_og)
    db.commit()
    db.refresh(model_og)
    return model_og

def delete_model(db: orm.Session, model_id: int):
    db.query(Model).filter(Model.id == model_id).delete()
    db.commit()
