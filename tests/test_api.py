import pytest
import json
from main.app import app
from main.database.models import db, Ward, Candidate


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def sample_data():
    """Create sample ward and candidate data for testing."""
    ward = Ward(id=1, name='Test Ward')
    db.session.add(ward)
    candidate1 = Candidate(
        id=1,
        name='Someone AwesomeSmith',
        ward_id=1,
        party='Test Party A',
        age=45,
        occupation='Developer'
    )
    candidate2 = Candidate(
        id=2,
        name='Someone Better',
        ward_id=1,
        party='Test Party B',
        age=38,
        occupation='Engineer'
    )
    
    db.session.add(candidate1)
    db.session.add(candidate2)
    db.session.commit()


def test_get_ward_candidates_success(client, sample_data):
    """Test successful retrieval of ward candidates."""
    response = client.get('/api/v1/wards/1/candidates')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['ward_id'] == 1
    assert data['ward_name'] == 'Test Ward'
    assert len(data['candidates']) == 2
    
    candidate = data['candidates'][0]
    assert candidate['name'] == 'John Smith'
    assert candidate['party'] == 'Test Party A'
    assert candidate['age'] == 45
    assert candidate['occupation'] == 'Teacher'


def test_get_ward_candidates_not_found(client):
    """Test 404 response for non-existent ward."""
    response = client.get('/api/v1/wards/999/candidates')
    
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Ward not found'


def test_get_ward_candidates_empty(client):
    """Test response for ward with no candidates."""
    ward = Ward(id=2, name='Empty Ward')
    db.session.add(ward)
    db.session.commit()
    
    response = client.get('/api/v1/wards/2/candidates')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['ward_id'] == 2
    assert data['ward_name'] == 'Empty Ward'
    assert len(data['candidates']) == 0