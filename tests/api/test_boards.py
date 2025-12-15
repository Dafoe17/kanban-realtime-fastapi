from tests.data.boards import BOARD_PREFIX


async def test_create_board(test_board):
    assert test_board["title"].startswith(BOARD_PREFIX)


async def test_get_my_boards(test_board, client, auth_headers):
    assert test_board["title"].startswith(BOARD_PREFIX)

    response = await client.get("/boards/my-boards", headers=auth_headers)
    assert response.status_code == 200
    assert int(response.json()["total"]) == 1


async def test_patch_board(test_board, client, auth_headers):
    assert test_board["title"].startswith(BOARD_PREFIX)

    response = await client.patch(
        f"/boards/patch/{test_board["id"]}",
        headers=auth_headers,
        json={"title": "new_table_title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "new_table_title"


async def test_delete_board(test_board, client, auth_headers):
    assert test_board["title"].startswith(BOARD_PREFIX)

    response = await client.delete(
        f"/boards/delete/{test_board["id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == test_board["title"]

    response = await client.get("/boards/my-boards", headers=auth_headers)
    assert response.status_code == 200
    assert int(response.json()["total"]) == 0
