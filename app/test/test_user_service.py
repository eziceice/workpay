import json
from unittest import TestCase
from user_service import (
    create_user
)


class Test(TestCase):
    def test_create_user(self):
        with open("create_user_input.json") as f:
            data = json.loads(f.read())
            create_user(data, "")
