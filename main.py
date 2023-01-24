from fastapi import FastAPI
from cloudamqp_helper import cloudamqp
from api_helper import jobs_api
import json


app = FastAPI()


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    """ The logic for grabbing jobs and sending an email
        will be invoked here
    """

    body = json.loads(body.decode('utf-8'))
    search_term = body.get("search_term")
    location = body.get("location")
    email = body.get("email")

    payload = {
        "search_terms": search_term,
        "location": location
    }
    jobs = jobs_api.get_jobs(payload=payload)
    print(f"\n ALL JOBS: #{jobs} \n")


def main():
    cloudamqp.consume_message(callback=callback)


@app.on_event("startup")
def startup_event():
    """ Code to run during startup """
    main()


@app.on_event("shutdown")
def shutdown_event():
    """ Code to run during shutdown """
    pass