from typing import Dict
import pytest
import aioresponses
from src.config.instance import APP_URL
from src.services.client_service import check_code, send_text


class TestClientService:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "code, expected_uwords_uid, status_code, response_json",
        [
            ("valid_code", "123", 200, {"uwords_uid": "123"}),
            ("invalid_code", None, 404, {"error": "Code not found"}),
            ("error_code", None, 500, {"error": "Internal server error"}),
        ],
    )
    async def test_check_code(self, code: str, expected_uwords_uid: str, status_code: int, response_json: Dict[str, str]):
        with aioresponses.aioresponses() as m:
            m.post(
                url=f"{APP_URL}/api/users/telegram/check_code",
                status=status_code,
                payload=response_json,
            )

            uwords_uid = await check_code(code=code)

            assert uwords_uid == expected_uwords_uid

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "uwords_uid, text, status_code, expected_result",
        [
            ("123", "valid_text", 200, True),
            ("456", "invalid_text", 404, False),
            ("789", "error_text", 500, False),
        ],
    )
    async def test_send_text(self, uwords_uid: str, text: str, status_code: int, expected_result: bool):
        with aioresponses.aioresponses() as m:
            m.post(url=f"{APP_URL}/api/v1/user/bot_word", status=status_code, payload={})

            result = await send_text(uwords_uid=uwords_uid, text=text)

            assert result == expected_result
