from datetime import date
from pydantic import BaseModel


class Result(BaseModel):
    id: int
    date: date
    symbol: str
    task: str
    difficult: int
    like: int

    class Config:
        orm_mode = True