import aiohttp
from fastapi import HTTPException
from web3 import Web3
from web3.contract import Contract


async def validate_address(address: str ,web3: Web3):
    if not web3.is_address(address):
        raise HTTPException(status_code=400, detail="Некорректный адрес")


async def _get_balance(address: str, token_contract: Contract, decimals):
    try:
        balance = token_contract.functions.balanceOf(address).call()
        return {"balance": balance / (10 ** decimals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения баланса: {str(e)}")


async def _get_top_holders(session: aiohttp.ClientSession,api_key: str,n: int, token_address: str):
    url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address.strip()}/owners"  # Убираем лишние пробелы
    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }
    params = {
        "chain": "polygon",
        "limit": n,
        "order": "DESC"
    }

    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()
        result = []
        for record in data.get("result", []):
            result.append((record["owner_address"], record["balance_formatted"]))
        return result

async def _get_last_transaction(session: aiohttp.ClientSession, api_key: str, address: str):

    url = f"https://deep-index.moralis.io/api/v2.2/{address.strip()}/erc20/transfers"

    headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    params = {
        "chain":"polygon",
        "limit": 1,
        "order": "DESC"
    }

    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()
        txs = data.get("result", [])
        if txs:
            last_tx = txs[0]
            return last_tx.get("block_timestamp", "N/A")
        else:
            return "N/A"




async def _get_info(token_contract: Contract):
    return {"symbol": token_contract.functions.symbol().call(), "name": token_contract.functions.name().call(), "totalSupply": token_contract.functions.totalSupply().call()}
