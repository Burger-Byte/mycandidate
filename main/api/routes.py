from flask import jsonify
from . import api_bp

@api_bp.route('/candidates', methods=['GET'])
def get_all_candidates():
    """
    Get all candidates from the database.
    
    Returns:
    - JSON array of all candidates
    """
    from main.database.models import db
    from sqlalchemy import text
    
    try:
        query = text("SELECT * FROM candidates WHERE candidate_type IS NOT NULL")
        candidates_result = db.session.execute(query).fetchall()
        
        candidates = []
        for row in candidates_result:
            candidate_data = dict(row)
            candidates.append(candidate_data)
        
        return jsonify({
            'total_candidates': len(candidates),
            'candidates': candidates
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@api_bp.route('/candidates/type/<candidate_type>', methods=['GET'])
def get_candidates_by_type(candidate_type):
    """
    Get candidates by type (provincial, national, national_regional).
    
    Parameters:
    - candidate_type (string): The type of candidates to retrieve
    
    Returns:
    - JSON array of candidates of the specified type
    """
    from main.database.models import db
    from sqlalchemy import text
    
    try:
        query = text("SELECT * FROM candidates WHERE candidate_type = :candidate_type")
        candidates_result = db.session.execute(query, {'candidate_type': candidate_type}).fetchall()
        
        if not candidates_result:
            return jsonify({'error': f'No candidates found for type: {candidate_type}'}), 404
        
        candidates = []
        for row in candidates_result:
            candidate_data = dict(row)
            candidates.append(candidate_data)
        
        return jsonify({
            'candidate_type': candidate_type,
            'total_candidates': len(candidates),
            'candidates': candidates
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@api_bp.route('/candidates/types', methods=['GET'])
def get_candidate_types():
    """
    Get all available candidate types.
    
    Returns:
    - JSON array of available candidate types
    """
    from main.database.models import db
    from sqlalchemy import text
    
    try:
        query = text("SELECT DISTINCT candidate_type, COUNT(*) as count FROM candidates GROUP BY candidate_type")
        types_result = db.session.execute(query).fetchall()
        
        types = []
        for row in types_result:
            types.append({
                'type': dict(row)['candidate_type'],
                'count': dict(row)['count']
            })
        
        return jsonify({
            'available_types': types
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@api_bp.route('/wards/<ward_id>/candidates', methods=['GET'])
def get_ward_candidates(ward_id):
    """
    Legacy endpoint: Since this database doesn't use ward structure, 
    this redirects to show candidates by type instead.
    
    Parameters:
    - ward_id: Interpreted as candidate_type if it matches available types
    
    Returns:
    - Suggestions for proper endpoints to use
    """
    from main.database.models import db
    from sqlalchemy import text
    
    try:
        valid_types = ['provincial', 'national', 'national_regional']
        
        if ward_id.lower() in valid_types:
            query = text("SELECT * FROM candidates WHERE candidate_type = :candidate_type LIMIT 10")
            candidates_result = db.session.execute(query, {'candidate_type': ward_id.lower()}).fetchall()
            
            candidates = []
            for row in candidates_result:
                candidate_data = dict(row)
                candidates.append(candidate_data)
            
            return jsonify({
                'message': f'No ward structure found. Showing candidates of type: {ward_id}',
                'suggestion': 'Use /api/v1/candidates/type/<type> for better results',
                'available_endpoints': [
                    '/api/v1/candidates',
                    '/api/v1/candidates/types',
                    '/api/v1/candidates/type/provincial',
                    '/api/v1/candidates/type/national',
                    '/api/v1/candidates/type/national_regional'
                ],
                'candidates': candidates
            }), 200
        else:
            return jsonify({
                'error': 'Ward structure not supported in this database',
                'suggestion': 'This database organizes candidates by type, not wards',
                'available_endpoints': [
                    '/api/v1/candidates - Get all candidates',
                    '/api/v1/candidates/types - Get available types',
                    '/api/v1/candidates/type/provincial - Get provincial candidates',
                    '/api/v1/candidates/type/national - Get national candidates',
                    '/api/v1/candidates/type/national_regional - Get regional candidates'
                ],
                'available_types': ['provincial', 'national', 'national_regional']
            }), 400
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500