import json
import os
from uuid import UUID

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from httpx import Response

from src.app.db.database import Base
from src.app.dependencies import get_db
from src.app.routers import metadata
from .db.test_dependencies import get_test_db, test_engine
from .db.test_database import DB_PATH

@pytest.fixture(scope='session', autouse=True)
def db_client():
    app = FastAPI(
        title="Metadata-test-API",
        description="Metadata internal API to interact with metadata files",
        dependencies=[Depends(get_test_db)],
        docs_url="/",
        redoc_url=None
    )

    app.include_router(metadata.router)
    app.dependency_overrides[get_db] = get_test_db

    client = TestClient(app)

    yield client

    try:
        os.remove(DB_PATH)
    except:
        print(f"DB file could not be deleted. It may not exist or path is not correct {DB_PATH}")

    test_engine.dispose()

@pytest.fixture(autouse=True)
def init_db():
    try:
        Base.metadata.drop_all(bind=test_engine)
    except:
        pass

    Base.metadata.create_all(bind=test_engine)

    #Execute the test
    yield

    pass

def create_test_metadata(db_client: TestClient, name: str = "first_metadata", payload: dict = {"sourceName": "my-flights", "jobCluster": { "min_workers": 1 }, "partitioning": "--partitioning=logic=partitionByEventTimestamp"}) -> Response:
    json_payload = json.dumps(payload)
    return db_client.post("/metadata", json={"name": name, "payload": json_payload})

def test_should_return_metadata_list(db_client: TestClient):
    # Given
    create_test_metadata(db_client)
    create_test_metadata(db_client)

    # When
    response: Response = db_client.get("/metadata")

    # Then
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response) == 2
    assert json_response[0]['id'] != json_response[1]['id']

def test_should_return_specific_metadata(db_client: TestClient):
    # Given
    created_metadata_response: Response = create_test_metadata(db_client)
    metadata_id = created_metadata_response.json()['id']

    # When
    response = db_client.get(f"/metadata/{metadata_id}")

    # Then
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['id'] == metadata_id

def test_should_create_new_metadata(db_client: TestClient):
    # Given
    name = "test"
    json_payload = {
        "sourceName": "my-flights",
        "jobCluster": {
            "min_workers": 1
        },
        "partitioning": "--partitioning=logic=partitionByEventTimestamp"
    }

    # When
    response: Response = create_test_metadata(db_client, name, json_payload)

    # Then
    assert response.status_code == 200

    data = response.json()

    #Assert UUID is correct
    assert "id" in data
    try:
        UUID(data["id"])
    except ValueError:
        assert False

    assert "name" in data
    assert data["name"] == name
    assert json.loads(data["payload"]) == json_payload

def test_should_delete_metadata(db_client: TestClient):
    # Given
    created_metadata_response: Response = create_test_metadata(db_client)
    metadata_id = created_metadata_response.json()['id']

    # When
    response = db_client.delete(f"/metadata/{metadata_id}")

    # Then
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['deleted'] == 1

def test_should_not_delete_when_not_found(db_client: TestClient):
    # Given
    # When
    response = db_client.delete(f"/metadata/123456789abcdef")

    # Then
    assert response.status_code == 404

def test_should_return_404_if_metadata_not_found(db_client: TestClient):
    # Given
    # When
    response = db_client.get(f"/metadata/123456789abcdef")

    # Then
    assert response.status_code == 404

def test_should_return_500_when_an_exception_occurs(db_client: TestClient):
    pass