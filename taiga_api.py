# taiga_api.py
import requests

TAIGA_API_URL = "http://localhost:9000/api/v1"
USERNAME = "admin@taiga.local"
PASSWORD = "123"

def get_auth_token():
    response = requests.post(f"{TAIGA_API_URL}/auth", json={
        "type": "normal",
        "username": USERNAME,
        "password": PASSWORD
    })

    if response.status_code == 200:
        return response.json()["auth_token"]
    else:
        raise Exception(f"Error al autenticar con Taiga: {response.text}")

def create_project(token, name, description=""):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": name,
        "description": description
    }

    response = requests.post(f"{TAIGA_API_URL}/projects", headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error al crear proyecto: {response.text}")
