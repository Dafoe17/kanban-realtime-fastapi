from tests.data.cards import CARD_PREFIX


async def test_create_comment(test_comment):
    assert test_comment["text"].startswith(f"comm_text_for_{CARD_PREFIX}")


async def test_patch_comment(test_comment, client, auth_headers):
    assert test_comment["text"].startswith(f"comm_text_for_{CARD_PREFIX}")

    response = await client.patch(
        f"/{test_comment["card_id"]}/comments/update?comment_id={test_comment["id"]}",
        headers=auth_headers,
        json={"text": "new_comment_text"},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "new_comment_text"


async def test_delete_comment(test_comment, client, auth_headers):
    assert test_comment["text"].startswith(f"comm_text_for_{CARD_PREFIX}")

    response = await client.delete(
        f"/{test_comment["card_id"]}/comments/delete?comment_id={test_comment["id"]}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["text"] == test_comment["text"]

    response = await client.get(
        f"/cards/get-card/{test_comment["card_id"]}", headers=auth_headers
    )
    assert response.status_code == 200
