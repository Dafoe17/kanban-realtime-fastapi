async def test_create_invite(test_invite):
    assert test_invite


async def test_delete_invite(test_invite, client, auth_headers):
    assert test_invite

    response = await client.delete(
        f"/invites/delete/{test_invite["id"]}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_invite["id"]

    response = await client.get(
        f"/invites/info/{test_invite["id"]}", headers=auth_headers
    )
    assert response.status_code == 404
