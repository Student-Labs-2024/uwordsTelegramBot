import pytest
import aioresponses
from src.config.instance import NODE
from src.services.client_service import check_code, send_text


class TestClientService:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "code, expected_user_id, status_code, response_json",
        [
            ("valid_code", 123, 200, {"user_id": 123}),
            ("invalid_code", None, 404, {"error": "Code not found"}),
            ("error_code", None, 500, {"error": "Internal server error"}),
        ],
    )
    async def test_check_code(self, code, expected_user_id, status_code, response_json):
        with aioresponses.aioresponses() as m:
            m.post(
                f"{NODE}/api/users/telegram/check_code",
                status=status_code,
                payload=response_json,
            )

            user_id = await check_code(code)

            assert user_id == expected_user_id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app_id, text, status_code, expected_result",
        [
            (123, "valid_text", 200, True),
            (456, "invalid_text", 404, False),
            (789, "error_text", 500, False),
        ],
    )
    async def test_send_text(self, app_id, text, status_code, expected_result):
        with aioresponses.aioresponses() as m:
            m.post(f"{NODE}/api/v1/user/bot_word", status=status_code, payload={})

            result = await send_text(app_id, text)

            assert result == expected_result
