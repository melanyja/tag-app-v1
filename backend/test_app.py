import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"
USER_EMAIL = "user1@email.com"
USER_PASSWORD = "user1"

@pytest.mark.asyncio
async def get_token():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/jwt/login",
            data={"username": USER_EMAIL, "password": USER_PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        return response.json()["access_token"]

@pytest.mark.asyncio
async def test_get_tags_unauthorized():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/tags/me")
    assert response.status_code == 401  

@pytest.mark.asyncio
async def test_get_my_tags():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/tags/me", headers=headers)

    print("Tags:", response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_tag():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "AUTOTEST_TAG",
        "value": "This is a test value",
        "description": "Tag for automated testing"
    }

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/tags/", headers=headers, json=payload)

    print("Create:", response.json())
    assert response.status_code in [200, 400]  
    if response.status_code == 200:
        assert response.json()["tag"]["name"] == "AUTOTEST_TAG"

@pytest.mark.asyncio
async def test_create_duplicate_tag():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "AUTOTEST_TAG",
        "value": "Duplicate value",
        "description": "Should fail"
    }

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/tags/", headers=headers, json=payload)

    print("Duplicate:", response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Tag name already exists"

@pytest.mark.asyncio
async def test_update_tag():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(base_url=BASE_URL) as ac:
        tag_res = await ac.get("/tags/me", headers=headers)
    tags = tag_res.json()
    tag_id = next((tag["id"] for tag in tags if tag["name"] == "AUTOTEST_TAG"), None)
    assert tag_id is not None, "Test tag not found for update"

    update_payload = {
        "name": "AUTOTEST_TAG_UPDATED",
        "value": "Updated value",
        "description": "Updated via test"
    }

    async with AsyncClient(base_url=BASE_URL) as ac:
        update_res = await ac.put(f"/tags/{tag_id}", headers=headers, json=update_payload)

    print("Update:", update_res.json())
    assert update_res.status_code == 200
    assert update_res.json()["tag"]["name"] == "AUTOTEST_TAG_UPDATED"

@pytest.mark.asyncio
async def test_update_tag_unauthorized():
   
    fake_id = 999999
    update_payload = {
        "name": "SHOULD_FAIL",
        "value": "no auth",
        "description": "unauthorized"
    }

    async with AsyncClient(base_url=BASE_URL) as ac:
        res = await ac.put(f"/tags/{fake_id}", json=update_payload)
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_delete_nonexistent_tag():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    invalid_tag_id = 999999999

    async with AsyncClient(base_url=BASE_URL) as ac:
        res = await ac.delete(f"/tags/{invalid_tag_id}", headers=headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Tag not found or unauthorized"

@pytest.mark.asyncio
async def test_delete_tag():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(base_url=BASE_URL) as ac:
        tag_res = await ac.get("/tags/me", headers=headers)
    tags = tag_res.json()
    tag_id = next((tag["id"] for tag in tags if tag["name"] == "AUTOTEST_TAG_UPDATED"), None)
    assert tag_id is not None, "Test tag not found for delete"

    async with AsyncClient(base_url=BASE_URL) as ac:
        delete_res = await ac.delete(f"/tags/{tag_id}", headers=headers)

    print("Delete:", delete_res.json())
    assert delete_res.status_code == 200
    assert f"{tag_id}" in delete_res.json()["message"]

@pytest.mark.asyncio
async def test_generate_content():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"prompt": "Give me a motivational quote"}

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/tags/generate-content", headers=headers, json=payload)

    print("AI Response:", response.json())
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_generate_content_invalid_prompt():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"prompt": ""}

    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/tags/generate-content", headers=headers, json=payload)

    print("AI Error:", response.text)
    
    assert response.status_code in [200, 422]

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
