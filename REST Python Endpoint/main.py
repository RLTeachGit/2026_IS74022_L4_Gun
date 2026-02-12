from flask import jsonify, request
from google.cloud import bigquery
from datetime import datetime
import uuid
import base64
import os

BASIC_USER = os.environ["BASIC_USER"]
BASIC_PASS = os.environ["BASIC_PASS"]


def unauthorized():
    return (
        jsonify({"error": "Unauthorized"}),
        401,
        {"WWW-Authenticate": 'Basic realm="Restricted"'}
    )

def ingest(request):

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return unauthorized()

    try:
        encoded = auth_header.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return unauthorized()

    if username != BASIC_USER or password != BASIC_PASS:
        return unauthorized()


    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    client = bigquery.Client()
    table_id = "ue5test-486811.UE5Analytics.Event_log"

    row = {
        "user_id": data.get("user_id"),
        "session_id": data.get("session_id"),
        "created_at": data.get("created_at"),
        "event_type": data.get("event_type"),
        "event_data": data.get("event_data"),
        "event_number": data.get("event_number")
    }

    errors = client.insert_rows_json(table_id, [row])
    if errors:
        return jsonify({"errors": errors}), 500

    return jsonify({"status": "ok"}), 200