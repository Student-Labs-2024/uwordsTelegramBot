import logging
import aiohttp

from src.config.instance import NODE, SECRET


logger = logging.getLogger("[SERVICES CLIENT]")
logging.basicConfig(level=logging.INFO)


async def check_code(code: str) -> int:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{NODE}/api/users/telegram/check_code", json={"code": code}
            ) as response:
                response.raise_for_status()

                res_json = await response.json()
                user_id: int = res_json.get("user_id")
                return user_id
    except Exception as e:
        logger.info(f"[CHECK CODE] Error: {e}")
        return None


async def send_text(app_id: int, text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{NODE}/api/v1/user/bot_word",
                json={
                    "secret": SECRET,
                    "user_id": app_id,
                    "text": text,
                },
            ) as response:
                response.raise_for_status()

                text = await response.text()

                return True
    except Exception as e:
        logger.info(f"[SEND TEXT] Error: {text}")
        return False
