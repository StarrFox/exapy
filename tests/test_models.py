import pydantic
import pytest

from exapy import models

# TODO: add tests for other models

def test_account():
    normal_data = {
        "name": "example",
        "email": "example@exaroton.com",
        "verified": True,
        "credits": 42
    }

    bad_type = {
        "name": 123,
        "email": "a",
        "verified": False,
        "credits": 100,
    }

    models.Account(**normal_data)

    with pytest.raises(pydantic.ValidationError):
        models.Account(**bad_type)


def test_server():
    normal_data = {
        "id": "EwYiY9IAMtQBTb6U",
        "name": "example",
        "address": "example.exaroton.me",
        "motd": "Welcome to the server of example!",
        "status": 0,
        "host": None,
        "port": None,
        "players": {
            "max": 20,
            "count": 0,
            "list": []
        },
        "software": {
            "id": "kb4p09ABvLjxzedx",
            "name": "Vanilla",
            "version": "1.16.5"
        },
        "shared": False,
    }


    models.Server(**normal_data)
