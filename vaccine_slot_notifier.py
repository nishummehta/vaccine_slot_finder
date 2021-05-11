"""
Created by :- Nishant Mehta
Creation Time :-  02:32am 12 May 2021

This tool can be used to find tommorrow's available vaccine slot at your pincode

This tool may have some flaws or issue. Please feel free to report them at
nishummehta1997@gmail.com
"""

import requests
import time
import argparse
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError

SLEEP_INTERVAL = 10
SLOT_AVAILABILITY_ENDPOINT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"

# This function is used to send email alert when a slot is available
def send_email(slot_details, sender, recipients):

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = "URGENT || Vaccine Slot available"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Vaccine Slot Available. Details: \r\n" + slot_details)

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1> Vaccine Slot available. Details : </h1>
      <br><br><h3>{code}</h3><br>
      <p>Created by :- Nishant Mehta(9003667751) </p>
    </body>
    </html>
    """.format(code=slot_details)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': recipients,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# This function is used to hit api and return the response
def get_slot_response(pincode, slot_date):

    payload = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/39.0.2171.95 Safari/537.36'}

    params = {
        'pincode': pincode,
        'date': slot_date
    }

    response = requests.request("GET",
                                SLOT_AVAILABILITY_ENDPOINT,
                                headers=headers,
                                data=payload,
                                params=params,
                                verify=False)
    return response

def main(pincode, sender, recipients):

    print("Execution Started")

    slot_date = (datetime.now()+timedelta(hours=29)+timedelta(minutes=30)).date()
    date_arr = str(slot_date).split("-")
    slot_date = date_arr[2] + '-' + date_arr[1] + '-' + date_arr[0]

    iteration_count = 0

    while True:
        try:
            response = get_slot_response(pincode, slot_date)
        except Exception as e:
            print("Exception occured. Details : [%s]" % e)

        if len(response.json()['sessions']) > 0:
            print(str(response.json()))
            send_email(str(response.json()), sender, recipients)

        iteration_count +=1
        if iteration_count % 50 == 0:
            print("Checked slot for [%d] times." % iteration_count)

        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Covid Slot Finder')

    parser.add_argument('--pincode',
                        type=int,
                        default=127021,
                        help='Enter pincode to search for covid slot')
    parser.add_argument('--sender_email',
                        type=str,
                        help='Enter the sender email(Must be Amazon SES verified)')

    parser.add_argument('--receiver_emails_comma_seperated',
                        type=str,
                        help='Enter the receiver emails in comma seperated format'
                             '(All emails should be Amazon SES verified)')

    args = parser.parse_args()

    sender = args.sender_email
    recipients = str(args.receiver_emails_comma_seperated).split(',')
    main(args.pincode, sender, recipients)
