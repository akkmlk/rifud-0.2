from flask import jsonify, Response

def success_response(message: str = "", data: dict = {}, res_code: int = 200) -> Response:
    return jsonify(
        {
            'data': data,
            'message': message,
            'status': "success",
        }
    ), res_code

def error_response(message: str = "", data: dict = {}, res_code: int = 400) -> Response:
    return jsonify(
        {
            'data': data,
            'message': message,
            'status': "error",
        }
    ), res_code