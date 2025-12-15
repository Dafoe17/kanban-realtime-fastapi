from tests.data.cards import CARD_PREFIX


async def test_create_card(test_card):
    assert test_card["title"].startswith(CARD_PREFIX)


async def test_patch_card(test_card, client, auth_headers):
    assert test_card["title"].startswith(CARD_PREFIX)

    response = await client.patch(
        f"/cards/patch-card/{test_card["id"]}",
        headers=auth_headers,
        json={"title": "new_column_title", "description": "new_description"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "new_column_title"
    assert response.json()["description"] == "new_description"


async def test_move_card(test_cards, client, auth_headers):
    assert test_cards[0]["title"].startswith(CARD_PREFIX)
    assert test_cards[1]["title"].startswith(CARD_PREFIX)
    assert test_cards[2]["title"].startswith(CARD_PREFIX)

    response = await client.patch(
        f"/cards/move-card/{test_cards[0]["id"]}",
        headers=auth_headers,
        json={"position": 1},
    )
    assert response.status_code == 200
    assert response.json()["position"] == 1


async def test_delete_card(test_card, client, auth_headers):
    assert test_card["title"].startswith(CARD_PREFIX)

    response = await client.delete(
        f"/cards/delete-card/{test_card["id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == test_card["title"]

    response = await client.get(
        f"/cards/get-column-cards/{test_card["column_id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert int(response.json()["total"]) == 0
