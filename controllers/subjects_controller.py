# coding: utf-8
from flask_cors import cross_origin
from flask import jsonify
from . import routes

@routes.route("/disciplinas")
@cross_origin()
def get_rates():
  return jsonify({"ok": "true"})