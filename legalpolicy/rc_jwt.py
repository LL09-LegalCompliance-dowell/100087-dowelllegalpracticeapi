# pip install pyjwt
import os
import jwt

JSON_WEB_TOKEN_SECRET = os.environ.get(
    "JSON_WEB_TOKEN_SECRET",
    "IwillChangeJsonWebTokenSoonForLegalPolicy"
    )


def encode(payload: dict):
    return jwt.encode(
        payload=payload,
        key=JSON_WEB_TOKEN_SECRET,
        algorithm="HS256"
        )

def decode(encoded_jwt: str):
    return jwt.decode(
        jwt=encoded_jwt,
        key=JSON_WEB_TOKEN_SECRET,
        algorithms=["HS256"]
        )
