from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from db import dataframes_obj, crud
from db.sa_db import SessionLocal
from models import LinearModel, TreeModel, DataFrame, Model
import db
from typing import Optional 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/dataframes/", response_model = dataframes_obj.DataFrame, tags=["DataFrames"]
)

def create_dataframe(
    dataframe: dataframes_obj.DataFrameCreate,
    dataframe_dict: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    dataframe_og = crud.create_dataframe(db=db, dataframe=dataframe)
    DataFrame.save(dataframe_og.id, dataframe_dict)
    return dataframe_og

@app.get(
    "/dataframes/", response_model=list[dataframes_obj.DataFrame], tags=["DataFrames"]
)

def read_dataframes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_dataframes(db=db, skip=skip, limit=limit)

@app.get(
    "/dataframes/{dataframe_id}/", response_model = dataframes_obj.DataFrame, tags=["DataFrames"]
)

def read_dataframe(dataframe_id: int, db: Session = Depends(get_db)):
    dataframe_og = crud.get_dataframe(db=db, dataframe_id=dataframe_id)
    if dataframe_og is None:
        raise HTTPException(status_code=404, detail="DataFrame doesn't exist")
    return dataframe_og

@app.delete(
    "/dataframes/{dataframe_id}/", tags=["DataFrames"]
)

def delete_dataframe(dataframe_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_dataframe(db=db, dataframe_id=dataframe_id)
        DataFrame.delete(dataframe_id)
    except IntegrityError:
        raise HTTPException(
            status_code=403,
            detail="Dataframe still used in models, firstly delete model",
        )
    return {"message": "Dataframe deleted"}

@app.post(
    "/models/", response_model=dataframes_obj.Model, tags=["Models"]
)

def create_model(
    model: dataframes_obj.ModelCreate,
    hyperparams: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    model_og = crud.create_model(db=db, model=model)
    model_learner = LinearModel
    if model_og.type == dataframes_obj.ChooseUrModel.Tree:
        model_learner = TreeModel
    model_learner.fit(model_og.id, model_og.dataframe_id, hyperparams)
    return model_og

@app.post(
    "/models/validation/", response_model=dataframes_obj.Model, tags=["Models"]
)

def create_model_with_validation(
    model: dataframes_obj.ModelCreate,
    hyperparams_grid: dict = None,
    db: Session = Depends(get_db),
):
    model_og = crud.create_model(db=db, model=model)
    model_learner = LinearModel
    if model_og.type == dataframes_obj.ChooseUrModel.Tree:
        model_learner = TreeModel
    model_learner.fit_with_validation(
        model_og.id, model_og.dataframe_id, hyperparams_grid
    )
    return model_og

@app.get(
    "/models/", response_model=list[dataframes_obj.Model], tags=["Models"]
)

def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_models(db=db, skip=skip, limit=limit)


@app.get(
    "/models/available/", response_model=dataframes_obj.AvailableModels, tags=["Models"]
)

def read_available_models():
    return dataframes_obj.AvailableModels()

@app.post(
    "/models/predict/", response_model=dataframes_obj.PredictResult, tags=["Models"]
)

def predict(
    model_info: dataframes_obj.Predict, dataframe: dict, db: Session = Depends(get_db)
):
    model_og = crud.get_model(db=db, model_id=model_info.model_id)
    if model_og is None:
        raise HTTPException(status_code=404, detail="Model not found")
    result = Model.predict(model_info.model_id, dataframe)
    return dataframes_obj.PredictResult(result=result)

@app.get(
    "/models/{model_id}/", response_model=dataframes_obj.Model, tags=["Models"]
)

def read_model(model_id: int, db: Session = Depends(get_db)):
    model_og = crud.get_model(db=db, model_id=model_id)
    if model_og is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return model_og

@app.delete(
    "/models/{model_id}/", tags=["Models"]
)

def delete_model(model_id: int, db: Session = Depends(get_db)):
    Model.delete_model(model_id)
    crud.delete_model(db=db, model_id=model_id)
    return {"message": "Model has been deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)