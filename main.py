import json
import os

from dotenv import load_dotenv
from pathlib import Path

from fastapi import FastAPI
from web3 import Web3

from api.api import router as api_router


app = FastAPI()

app.include_router(api_router, prefix="/api")

