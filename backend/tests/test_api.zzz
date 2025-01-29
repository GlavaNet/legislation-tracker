# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.main import app
from app.database import Base, get_db
from app.models import Legislation, LegislationType

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

@pytest.fixture
def sample_legislation(test_db):
    legislation_data = [
        {
            "id": "federal_1",
            "type": LegislationType.FEDERAL,
            "title": "Test Federal Bill",
            "summary": "Test Summary",
            "status": "active",
            "introduced_date": datetime.now(),
            "source_url": "http://example.com",
            "metadata": {"bill_number": "HR1"}
        },
        {
            "id": "state_1",
            "type": LegislationType.STATE,
            "title": "Test State Bill",
            "summary": "Test Summary",
            "status": "active",
            "introduced_date": datetime.now(),
            "source_url": "http://example.com",
            "metadata": {"state": "CA"}
        },
        {
            "id": "executive_1",
            "type": LegislationType.EXECUTIVE,
            "title": "Test Executive Order",
            "summary": "Test Summary",
            "status": "signed",
            "introduced_date": datetime.now(),
            "source_url": "http://example.com",
            "metadata": {"order_number": "12345"}
        }
    ]
    
    db = TestingSessionLocal()
    for data in legislation_data:
        legislation = Legislation(**data)
        db.add(legislation)
    db.commit()
    db.close()

def test_read_federal_legislation(client, sample_legislation):
    response = client.get("/api/v1/federal/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["type"] == "federal"

def test_read_state_legislation(client, sample_legislation):
    response = client.get("/api/v1/state/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["type"] == "state"

def test_read_executive_orders(client, sample_legislation):
    response = client.get("/api/v1/executive/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["type"] == "executive"

def test_read_single_legislation(client, sample_legislation):
    response = client.get("/api/v1/federal/federal_1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "federal_1"
    assert data["title"] == "Test Federal Bill"

def test_read_nonexistent_legislation(client):
    response = client.get("/api/v1/federal/nonexistent")
    assert response.status_code == 404

def test_pagination(client, sample_legislation):
    response = client.get("/api/v1/federal/?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data

def test_search_legislation(client, sample_legislation):
    response = client.get("/api/v1/federal/?search=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
    assert "Test" in data["data"][0]["title"]

def test_filter_by_status(client, sample_legislation):
    response = client.get("/api/v1/federal/?status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
    assert data["data"][0]["status"] == "active"

def test_date_range_filter(client, sample_legislation):
    today = datetime.now().strftime("%Y-%m-%d")
    response = client.get(f"/api/v1/federal/?start_date={today}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0

# Tests for error handling
def test_invalid_page_number(client):
    response = client.get("/api/v1/federal/?page=0")
    assert response.status_code == 400

def test_invalid_limit(client):
    response = client.get("/api/v1/federal/?limit=1000")
    assert response.status_code == 400

def test_invalid_date_format(client):
    response = client.get("/api/v1/federal/?start_date=invalid-date")
    assert response.status_code == 422

# Tests for scrapers
@pytest.mark.integration
def test_congress_scraper():
    from app.scrapers.scrapers import CongressScraper
    
    scraper = CongressScraper()
    data = scraper.scrape()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]
        assert "type" in data[0]
        assert data[0]["type"] == LegislationType.FEDERAL

@pytest.mark.integration
def test_federal_register_scraper():
    from app.scrapers.scrapers import FederalRegisterScraper
    
    scraper = FederalRegisterScraper()
    data = scraper.scrape()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]
        assert "type" in data[0]
        assert data[0]["type"] == LegislationType.EXECUTIVE
