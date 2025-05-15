from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200
    pass

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
# @app.route("/picture", methods=["POST"])
# def create_picture():
#     pass


@app.route("/picture/<int:id>", methods=["POST"])
def create_picture():
    picture = request.get_json()
    
    # Check if the picture with the same id already exists
    if any(p['id'] == picture['id'] for p in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    data.append(picture)
    return jsonify(picture), 201


@app.route("/count", methods=["GET"])
def get_count():
    return jsonify({"length": len(data)}), 200
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    for i, p in enumerate(data):
        if p["id"] == id:
            data[i] = picture
            with open(json_url, "w") as json_file:
                json.dump(data, json_file)
            return jsonify(picture), 200
    return jsonify({"error": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i, p in enumerate(data):
        if p["id"] == id:
            del data[i]
            with open(json_url, "w") as json_file:
                json.dump(data, json_file)
            return jsonify({"message": "Picture deleted"}), 200
    return jsonify({"error": "Picture not found"}), 404