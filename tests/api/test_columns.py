from tests.data.columns import COLUMN_PREFIX


async def test_create_column(test_column):
    assert test_column["title"].startswith(COLUMN_PREFIX)


async def test_patch_column(test_column, client, auth_headers):
    assert test_column["title"].startswith(COLUMN_PREFIX)

    response = await client.patch(
        f"/columns/patch-column/{test_column["id"]}",
        headers=auth_headers,
        json={"title": "new_column_title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "new_column_title"


async def test_move_column(test_columns, client, auth_headers):
    assert test_columns[0]["title"].startswith(COLUMN_PREFIX)
    assert test_columns[1]["title"].startswith(COLUMN_PREFIX)
    assert test_columns[2]["title"].startswith(COLUMN_PREFIX)

    response = await client.patch(
        f"/columns/move-column/{test_columns[0]["id"]}",
        headers=auth_headers,
        json={"position": 1},
    )
    assert response.status_code == 200
    assert response.json()["position"] == 1


async def test_delete_column(test_column, client, auth_headers):
    assert test_column["title"].startswith(COLUMN_PREFIX)

    response = await client.delete(
        f"/columns/delete/{test_column["id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == test_column["title"]

    response = await client.get(
        f"/columns/get-board-columns/{test_column["board_id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert int(response.json()["total"]) == 0
