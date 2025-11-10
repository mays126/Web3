from typing import List
from pydantic import BaseModel


class GetBalance(BaseModel):
    address: str

class ReturnBalance(BaseModel):
    balance: float


class GetBalanceBatch(BaseModel):
    batch: List[str]

class ReturnBalanceBatch(BaseModel):
    batch: List[float]