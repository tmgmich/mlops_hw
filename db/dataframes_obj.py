from datetime import datetime
from typing import Iterable, Optional 
from pydantic import BaseModel 
import enum 

class ChooseUrModel(str, enum.Enum):    
    Regression = "Regression" 
    Tree = "Tree" 

class DataFrameCreate(BaseModel): 
    description: Optional[str] = None    
    target: str = "target" 

class DataFrame(BaseModel):    
    id: int 
    created_date: datetime
    description: Optional[str] = None    
    target: str = "target"
    
    class Config: 
        orm_mode = True 

class ModelCreate(BaseModel): 
    dataframe_id: int    
    description: Optional[str] = None 
    type: ChooseUrModel 

    class Config:        
        use_enum_values = True 

class Model(BaseModel):    
    id: int 
    dataframe_id: int    
    description: Optional[str] = None 
    type: ChooseUrModel 

    class Config:        
        use_enum_values = True 
        orm_mode = True 

class AvailableModels(BaseModel): 
    models: list[str] = [m.value for m in ChooseUrModel] 

class Predict(BaseModel): 
    model_id: int 

class PredictResult(BaseModel): 
    result: Iterable[float]