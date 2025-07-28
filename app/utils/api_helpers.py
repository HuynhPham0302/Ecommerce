from datetime import datetime

from flask import jsonify


class APIResponse:
    """Standardized API response format"""
    
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        """Return a successful API response"""
        response = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="An error occurred", status_code=400, error_code=None):
        """Return an error API response"""
        response = {
            "success": False,
            "message": message,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat()
        }
        return jsonify(response), status_code