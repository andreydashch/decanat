import json
import sqlite3

from flask import redirect, request, url_for
from flask_login import login_user

from oauthlib.oauth2 import WebApplicationClient
import requests

from auth.googleuser import GoogleUser

from auth.db import init_db_command
import resourse

GOOGLE_CLIENT_ID = resourse.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = resourse.GOOGLE_CLIENT_SECRET
GOOGLE_DISCOVERY_URL = (
    resourse.GOOGLE_DISCOVERY_URL
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def login_callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = GoogleUser(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    if not GoogleUser.get(unique_id):
        GoogleUser.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect(url_for("index"))


def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)
