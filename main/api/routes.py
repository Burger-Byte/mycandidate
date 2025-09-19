from flask import jsonify
from . import api_bp
from main.database.models import db, Candidate, Ward


@api_bp.route('/wards/<int:ward_id>/candidates', methods=['GET'])
def get_ward_candidates(ward_id):
    """
    Get all candidates standing for election in a specific ward.
    
    Parameters:
    - ward_id (int): The ID of the ward
    
    Returns:
    - JSON array of candidates with their details
    - 404 if ward doesn't exist
    
    Sample Response:
    {
        "ward_id": 1,
        "ward_name": "Ward 1",
        "candidates": [
            {
                "id": 1,
                "name": "Someone Awesome",
                "party": "Party A",
                "age": 45,
                "occupation": "Developer"
            }
        ]
    }
    """
    ward = Ward.query.get(ward_id)
    if not ward:
        return jsonify({'error': 'Ward not found'}), 404
    
    candidates = Candidate.query.filter_by(ward_id=ward_id).all()
    
    response = {
        'ward_id': ward.id,
        'ward_name': ward.name,
        'candidates': []
    }
    
    for candidate in candidates:
        candidate_data = {
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party if hasattr(candidate, 'party') else None,
            'age': candidate.age if hasattr(candidate, 'age') else None,
            'occupation': candidate.occupation if hasattr(candidate, 'occupation') else None
        }
        response['candidates'].append(candidate_data)
    
    return jsonify(response), 200


@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500