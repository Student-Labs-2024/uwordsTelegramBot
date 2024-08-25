import logging
from typing import Dict
import aiohttp

from src.config.instance import APP_URL, APP_TOKEN


logger = logging.getLogger("[SERVICES CLIENT]")
logging.basicConfig(level=logging.INFO)


async def check_code(code: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{APP_URL}/api/users/telegram/check_code",
                headers={
                    "Authorization": f"Bearer {APP_TOKEN}",
                },
                json={"code": code},
            ) as response:
                response.raise_for_status()

                res_json: Dict[str, str] = await response.json()
                uwords_uid: int = res_json.get("uwords_uid")
                return uwords_uid

    except Exception as e:
        logger.info(f"[CHECK CODE] Error: {e}")
        return None


async def send_text(uwords_uid: str, text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{APP_URL}/api/v1/user/bot_word",
                headers={"Authorization": f"Bearer {APP_TOKEN}"},
                json={"uwords_uid": uwords_uid, "text": text},
            ) as response:
                data = await response.text()

                if response.status != 200:
                    logger.info(f"[SEND TEXT] Error: {data}")
                    return False

                return True
    except Exception as e:
        logger.info(f"[SEND TEXT] Error: {e}")
        return False


async def send_audio(uwords_uid: str, file_path: str, filename: str, content_type: str):
    try:
        async with aiohttp.ClientSession() as session:

            form_data = aiohttp.FormData()
            form_data.add_field(
                "audio_file",
                open(file=file_path, mode="rb"),
                filename=filename,
                content_type=content_type,
            )

            async with session.post(
                url=f"{APP_URL}/api/v1/user/bot_audio?uwords_uid={uwords_uid}",
                headers={"Authorization": f"Bearer {APP_TOKEN}"},
                data=form_data,
            ) as response:
                data = await response.text()

                if response.status != 200:
                    logger.info(f"[SEND TEXT] Error: {data}")
                    return False

                return True
    except Exception as e:
        logger.info(f"[SEND AUDIO] Error: {e}")
        return False


async def send_promo(uwords_uid: str, promo: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{APP_URL}/api/v1/user/promo",
                headers={"Authorization": f"Bearer {APP_TOKEN}"},
                json={"uwords_uid": uwords_uid, "promo": promo},
            ) as response:
                data = await response.text()

                if response.status != 200:
                    logger.info(f"[SEND PROMO] Error: {data}")
                    return False

                return True
    except Exception as e:
        logger.info(f"[SEND PROMO] Error: {e}")
        return False
