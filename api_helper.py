import os, json
from typing import List, Dict
from dotenv import load_dotenv

import requests


# Load the .env file
load_dotenv()


class APIRequestHelper:
    """
        A helper class for calling the external APIs
        Moved the api-calling code to this separate function to separate concerns
    """
    API_KEY = os.environ["RAPID_API_KEY"]

    def __make_request(
        self, url: str, headers: dict = None, params: dict = None, payload: dict = None
    ):
        if headers is None:
            headers = {
                "x-rapidapi-key": self.API_KEY, 
                "content-type": "application/json"
            }
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            
            print(f"\n request response #{response.text} \n")
            print(f"\n request response code #{response.status_code} \n")
        except Exception as e:
            error = f"erro: {e}"
            response = {"error": error}
            print(response)
        
        response = json.loads(response.content)
        return response[:5]

    def __get_linkedin_jobs(self, payload: dict) -> List[Dict]:
        __api_url = "https://linkedin-jobs-search.p.rapidapi.com/"
        linkedin_jobs = self.__make_request(url=__api_url, payload=payload)

        return linkedin_jobs


    def get_jobs(self, payload: dict) -> List[Dict]:
        jobs = self.__get_linkedin_jobs(payload=payload)
        
        return jobs


jobs_api: APIRequestHelper = APIRequestHelper()