from flask import Blueprint, jsonify
from apiapp.model.mongodb import query_stats, query_account

account = Blueprint("account", __name__)

@account.route("/<apiid>/account", methods=["GET"])
def query_account_route(apiid):
    account_info = query_account(apiid)
    return jsonify(account_info)
    
@account.route("/<apiid>/stats", methods=["GET"])
def query_stats_route(apiid):
    account_stats = query_stats(apiid)
    return jsonify(account_stats)
