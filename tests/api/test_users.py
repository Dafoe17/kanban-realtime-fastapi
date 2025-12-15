import pytest


async def test_get_me(client, auth_headers):
    response = await client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"]
    assert "@test.com" in response.json()["email"]


async def test_get_users(client, auth_headers):
    response = await client.get("/users/get-all?order=ASC", headers=auth_headers)
    assert response.status_code == 200
    assert int(response.json()["total"]) > 0


async def test_patch_user(client, auth_headers):
    response = await client.patch(
        "/users/patch-user?username=new_name&email=new_emai@test.com",
        headers=auth_headers,
    )
    assert response.status_code == 200
    response = response.json()
    assert response["username"] == "new_name"
    assert response["email"] == "new_emai@test.com"


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/docs")
    assert response.status_code == 200
