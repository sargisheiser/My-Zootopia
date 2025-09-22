import requests
import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals"


def fetch_data(animalName):
   """ Fetches animal data from the API."""


   headers = {"X-Api-Key": API_KEY}
   response = requests.get(API_URL, params = {"name": animalName}, headers=headers)
   response.raise_for_status()
   return response.json()
