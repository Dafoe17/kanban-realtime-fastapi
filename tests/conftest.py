from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.main import app
from src.repositories import UsersRepository
from src.services import AuthService

from .data import (
    generate_test_board,
    generate_test_card,
    generate_test_checklist,
    generate_test_checklist_item,
    generate_test_column,
    generate_test_comment,
    generate_test_tag,
    generate_test_user,
)


@pytest.fixture(autouse=True)
def mock_redis():
    with patch(
        "src.redis.tokens.RedisTools.ensure_initialized", new_callable=AsyncMock
    ) as mock:
        mock.return_value = AsyncMock()
        yield mock


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_headers(client):
    test_user_data = generate_test_user()
    password = test_user_data.password_hash
    db = next(get_db())
    try:
        user = await AuthService.sign_up(db=db, data=test_user_data)

        response = await client.post(
            "/auth/token-json",
            data={"username": test_user_data.email, "password": password},
        )
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        yield headers
    finally:
        if user:
            UsersRepository.delete_user(db=db, data=user)


@pytest.fixture
async def test_board(client, auth_headers):

    test_board_data = generate_test_board()

    response = await client.post(
        "/boards/create", headers=auth_headers, json={"title": test_board_data.title}
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_column(test_board, client, auth_headers):

    test_column_data = generate_test_column()

    response = await client.post(
        f"/columns/create/in-board={test_board["id"]}",
        headers=auth_headers,
        json={"title": test_column_data.title},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_columns(test_board, client, auth_headers):
    columns = []

    for _ in range(3):
        test_column_data = generate_test_column()

        res = await client.post(
            f"/columns/create/in-board={test_board["id"]}",
            headers=auth_headers,
            json={"title": test_column_data.title},
        )
        assert res.status_code == 200
        columns.append(res.json())

    return columns


@pytest.fixture
async def test_card(test_column, client, auth_headers):

    test_card_data = generate_test_card()

    response = await client.post(
        f"/cards/create/in-column={test_column["id"]}",
        headers=auth_headers,
        json={"title": test_card_data.title, "description": test_card_data.description},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_cards(test_column, client, auth_headers):
    cards = []

    for _ in range(3):
        test_card_data = generate_test_card()

        res = await client.post(
            f"/cards/create/in-column={test_column["id"]}",
            headers=auth_headers,
            json={
                "title": test_card_data.title,
                "description": test_card_data.description,
            },
        )
        assert res.status_code == 200
        cards.append(res.json())

    return cards


@pytest.fixture
async def test_comment(test_card, client, auth_headers):

    test_comment_data = generate_test_comment()

    response = await client.post(
        f"/{test_card["id"]}/comments/create",
        headers=auth_headers,
        json={"text": test_comment_data.text},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_tag(test_board, client, auth_headers):

    test_tag_data = generate_test_tag()

    response = await client.post(
        f"/{test_board["id"]}/tags/create",
        headers=auth_headers,
        json={"title": test_tag_data.title, "color": test_tag_data.color},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_checklist(test_card, client, auth_headers):

    test_checklist_data = generate_test_checklist()

    response = await client.post(
        f"/{test_card["id"]}/checklist/create",
        headers=auth_headers,
        json={"title": test_checklist_data.title},
    )

    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_checklist_item(test_checklist, client, auth_headers):

    test_checklist_item_data = generate_test_checklist_item()

    response = await client.post(
        f"/{test_checklist["card_id"]}/checklist/{test_checklist["id"]}/item/create",
        headers=auth_headers,
        json={"task": test_checklist_item_data.task},
    )

    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def test_invite(test_board, client, auth_headers):

    response = await client.post(
        f"/invites/boards/{test_board["id"]}/invite",
        headers=auth_headers,
    )

    assert response.status_code == 200
    return response.json()
