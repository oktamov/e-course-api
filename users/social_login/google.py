import json

import requests
from google.oauth2 import id_token  # noqa


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            url = f"https://openidconnect.googleapis.com/v1/userinfo?access_token={auth_token}"
            response = requests.request("GET", url)
            return json.loads(response.text)
        except Exception:  # noqa
            return "The token is either invalid or has expired"
