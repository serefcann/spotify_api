import os
from dotenv import load_dotenv
import dotenv
import base64
import requests

class Token:
    def __init__(self):
        self.dotenv_path = "C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env"
        load_dotenv(self.dotenv_path)
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

    def get_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        token_url = "https://accounts.spotify.com/api/token"
        headers = {
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        data = {
                "grant_type": "client_credentials"
            }
        response = requests.post(token_url, headers=headers, data=data)
        return response

    def embbed_token(self):
        response = self.get_token()
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(token,"\n")
            dotenv.set_key(self.dotenv_path, "TOKEN", token)

            load_dotenv(self.dotenv_path)
            print(f"Successfully updated in .env file: {os.getenv('TOKEN')}")
        else:
            print("Failed to get access token")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

token = Token()
token.get_token()
token.embbed_token()