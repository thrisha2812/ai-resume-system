# Utility functions for Python AI service

def format_response(success, data=None, error=None):
    """Format API response"""
    response = {"success": success}
    if data:
        response.update(data)
    if error:
        response["error"] = error
    return response

def validate_input(text, min_length=1, max_length=10000):
    """Validate text input"""
    if not text or len(text) < min_length:
        return False, "Input text too short"
    if len(text) > max_length:
        return False, "Input text too long"
    return True, "Valid"
