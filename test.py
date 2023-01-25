import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from dotenv import load_dotenv


# Load the .env file
load_dotenv()


class TwilioHelper:
    FROM_EMAIL = 'nyior@84codes.com'
    
    
    def __Send_email(self, message: Mail):
        """ Send an email to the provided email addresses"""

        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response Code: {code} ")
            print(f"Response Body: {body} ")
            print(f"Response Headers: {headers} ")
            print("Email Sent!")
        except Exception as e:
            print("Error: {0}".format(e))
        return str(response.status_code)

    def email_job_listing(self, to_email: str):
        TO_EMAILS = [
            To(
                email=to_email,
                substitutions={
                    "-job_url-": "random job",
                    "-company_name-": "random company",
                    "-job_location-": "random location",
                    "-date_posted-": "random date posted"
                }
            )
        ]

        html_content=(
            "<strong>Hello there from GetMeHired! We've got new job posting for you :) " 
            "Job URL: -job_url-"
            "Company Name: -company_name-"
            "Job Location: -job_location-"
            "Date Posted: -date_posted-"
        )

        message = Mail(
            from_email=self.FROM_EMAIL,
            to_emails=TO_EMAILS,
            subject="New Job Posting HTML Content - GetMeHired",
            html_content=html_content
        )

        self.__Send_email(message)


twilio_api: TwilioHelper = TwilioHelper()
twilio_api.email_job_listing("cnyior27@gmail.com")