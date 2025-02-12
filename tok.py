import os
from dotenv import load_dotenv
import dotenv
import base64
import requests
import time


class Token:
    def __init__(self,auth_code):
        self.dotenv_path = "C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env"
        load_dotenv(self.dotenv_path)
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.auth_code = auth_code
        self.redirect_uri = "http://localhost:8888/callback"
        
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
                "grant_type": "authorization_code",
                "code":self.auth_code,
                "redirect_uri":self.redirect_uri,
                "client_id":self.client_id,
                "client_secret":self.client_secret
            }
        response = requests.post(token_url, headers=headers, data=data)
        return response

    def embbed_token(self):
        response = self.get_token()
        if response.status_code == 200:
            token = response.json().get("access_token")
            refresh_token = response.json().get("refresh_token")
            print(refresh_token)
            
            dotenv.set_key(self.dotenv_path, "TOKEN", token)
            dotenv.set_key(self.dotenv_path,"REFRESH_TOKEN",refresh_token)

            load_dotenv(self.dotenv_path,override=True)
            print(f"Successfully updated in .env file: {os.getenv('TOKEN')}")
            print("refresh token: ",os.getenv("REFRESH_TOKEN"))
        else:
            print("Failed to get access token")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            
    def refresh_access_token(self):
        if not os.getenv("REFRESH_TOKEN"):
            print("No refresh token found. Get a new authorization code manually.")
            return

        token_url = "https://accounts.spotify.com/api/token"
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": os.getenv("REFRESH_TOKEN"),
            "expires_at": time.time() + 3600
        }

        response = requests.post(token_url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json.get("access_token")

            dotenv.set_key(self.dotenv_path, "TOKEN", access_token)

            print("Successfully refreshed access token!")
            print(f"New Token: {access_token}")
        else:
            print("Failed to refresh access token!")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

        return response

if __name__ == "__main__":
    token = Token("")
    token.embbed_token()
    token.refresh_access_token()


