from flask import jsonify


def item_not_found(error):
    response_data = {"message": str(error.description)}
    return jsonify(response_data), 404


def bad_request(error):
    response_data = {"message": str(error.description)}
    return jsonify(response_data), 400


def access_forbidden(error):
    response_data = {"message": str(error.description)}
    return jsonify(response_data), 403


def internal_server_error(error):
    response_data = {"message": str(error.description)}
    return jsonify(response_data), 500
