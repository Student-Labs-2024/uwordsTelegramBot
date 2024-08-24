import pytest
from unittest.mock import AsyncMock, patch
from src.database.models import User
from src.services.user_service import create_user, get_user


class TestUserService:

    @pytest.mark.asyncio
    @pytest.mark.parametrize("telegram_id, uwords_uid", [(123456, "789"), (987654, "321")])
    async def test_create_user(self, telegram_id, uwords_uid):
        with patch(
            "src.services.user_service.async_session_maker"
        ) as mock_session_maker:
            mock_session = AsyncMock()
            mock_session_maker.return_value.__aenter__.return_value = mock_session

            result = await create_user(telegram_id=telegram_id, uwords_uid=uwords_uid)

            assert result is True

            mock_session.execute.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("telegram_id", [123456, 987654])
    async def test_get_user(self, telegram_id):
        with patch(
            "src.services.user_service.async_session_maker"
        ) as mock_session_maker:
            mock_session = AsyncMock()
            mock_session_maker.return_value.__aenter__.return_value = mock_session

            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = User(
                tg_user_id=telegram_id, uwords_uid="123"
            )
            mock_session.execute.return_value = mock_result

            result = await get_user(telegram_id=telegram_id)

            assert result is not None

            mock_session.execute.assert_called_once()
