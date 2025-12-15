from tests.data.cards import CARD_PREFIX


async def test_create_tag(test_tag):
    assert test_tag["title"].startswith(f"tag_title_for_{CARD_PREFIX}")


async def test_patch_tag(test_tag, client, auth_headers):
    assert test_tag["title"].startswith(f"tag_title_for_{CARD_PREFIX}")

    response = await client.patch(
        f"/{test_tag["board_id"]}/tags/{test_tag['id']}/update",
        headers=auth_headers,
        json={"title": "new_tag_title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "new_tag_title"


async def test_delete_tag(test_tag, client, auth_headers):
    assert test_tag["title"].startswith(f"tag_title_for_{CARD_PREFIX}")

    response = await client.delete(
        f"/{test_tag["board_id"]}/tags/{test_tag["id"]}/delete", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == test_tag["title"]


async def test_set_tag(test_tag, test_card, client, auth_headers):
    assert test_tag["title"].startswith(f"tag_title_for_{CARD_PREFIX}")
    assert test_card["title"].startswith(f"{CARD_PREFIX}")

    response = await client.patch(
        f"/{test_tag["board_id"]}/tags/{test_card["id"]}/set/{test_tag["id"]}",
        headers=auth_headers,
    )
    assert response.status_code == 200

    response = await client.get(
        f"/{test_tag["board_id"]}/tags/get/{test_card["id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert test_tag["id"] in response.json()["tags"][0]["id"]
