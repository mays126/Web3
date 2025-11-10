import asyncio
from typing import List

import aiohttp
from watchfiles import awatch
from web3.contract import Contract
from web3 import Web3
from api.service import validate_address, _get_balance, _get_top_holders, _get_last_transaction, _get_info
from api.schemas import ReturnBalance

async def get_balance(address: str, token_contract: Contract, web3: Web3, decimals):
    await validate_address(address, web3)
    balance = await _get_balance(address,token_contract,decimals)
    return ReturnBalance.model_validate(balance)


async def get_balance_batch(addresses: List[str], token_contract: Contract, web3: Web3, decimals):
    for address in addresses:
        await validate_address(address, web3)

    tasks = [_get_balance(addr, token_contract,decimals) for addr in addresses]
    balances = await asyncio.gather(*tasks)
    return balances


async def get_top(api_key: str,n: int, token_address: str):
    async with aiohttp.ClientSession() as session:
        holders = await _get_top_holders(session,api_key,n, token_address)
    return holders


async def get_top_with_transactions(api_key: str, n: int, token_address: str):
    async with aiohttp.ClientSession() as session:
        holders = await _get_top_holders(session, api_key, n, token_address)
        if not holders:
            return []

        addresses = [holder[0] for holder in holders]
        balances = {holder[0]: holder[1] for holder in holders}

        tasks = [_get_last_transaction(session, api_key, addr) for addr in addresses]

        last_tx_dates = await asyncio.gather(*tasks)

        result = []
        for i in range(len(addresses)):
            addr = addresses[i]
            balance = balances[addr]
            date = last_tx_dates[i]
            result.append((addr, float(balance), date))

        return result




async def get_info(address: str, web3: Web3,erc20_abi):
    token_contract = web3.eth.contract(
    address=Web3.to_checksum_address(address),
    abi=erc20_abi
    )

    return await _get_info(token_contract)