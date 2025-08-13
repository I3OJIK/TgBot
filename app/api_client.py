import aiohttp
from config import API_URL, API_EMAIL, API_PASSWORD

async def get_access_token():
    """Авторизация в Laravel API и получение access_token"""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/auth/login", data={
            "email": API_EMAIL,
            "password": API_PASSWORD
        }) as resp:
            data = await resp.json()
            return data.get("access_token")


async def get_cart(token):
    """Запрос корзины"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/cart", headers={
            "Authorization": f"Bearer {token}"
        }) as resp:
            return await resp.json()
        
async def change_product_quantity(product_id: int, delta: int):
    """Запрос корзины"""
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/cart/{product_id}", headers={
            "Authorization": f"Bearer {await get_access_token()}"
        },data={
            "delta": {delta}
        }) as resp:
            return await resp.json()