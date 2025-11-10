import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter
from web3 import Web3

from api.controller import get_balance, get_balance_batch, get_top, get_top_with_transactions, get_info
from api.schemas import ReturnBalance,GetBalanceBatch

router = APIRouter()

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
POLYGON_RPC = os.getenv("POLYGON_RPC", "https://polygon-rpc.com")
API_KEY = os.getenv("API_KEY")


abi_path = Path("erc20_abi.json")
with open(abi_path, "r") as f:
    erc20_abi = json.load(f)

web3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
if not web3.is_connected():
    raise ConnectionError("Не удалось подключиться к Polygon RPC")

token_contract = web3.eth.contract(
    address=Web3.to_checksum_address(TOKEN_ADDRESS),
    abi=erc20_abi
)

try:
    DECIMALS = token_contract.functions.decimals().call()
except Exception as e:
    raise RuntimeError(f"Ошибка получения decimals: {str(e)}")





@router.get("/get_balance",response_model=ReturnBalance)
async def get_token_balance(address: str):
    return await get_balance(address, token_contract, web3, DECIMALS)

@router.post("/get_balance_batch")
async def get_tokens_balance(addresses: GetBalanceBatch):
    return await get_balance_batch(addresses.batch, token_contract, web3, DECIMALS)


@router.get("/get_top")
async def get_top_holders(n: int):
    return await get_top(API_KEY,n, TOKEN_ADDRESS)


@router.get("/get_top_with_transactions")
async def get_top_with_transactions_token(n: int):
    return await get_top_with_transactions(API_KEY, n, TOKEN_ADDRESS)


@router.get("/get_token_info")
async def get_token_info(address: str):
    return await get_info(address, web3,erc20_abi)