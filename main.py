"""Function called by PubSub trigger to execute cron job tasks."""
import logging
from operator import index
from string import Template
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pandas import to_datetime


def sendEmail(mail_content):
    sender_address = 'example@example.ca'
    sender_pass = 'Mkj56rfGtf7^5'
    receiver_address = ['example@example.ca', 'example@example.ca']
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('mail.example.ca', 587) #use email with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def main(dataa, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        data (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    try:
        sheet_id = "1beHkJSxGJWwDmbD0PauVF7SMehmTdIrQUrJK8"
        sheet_name = "Page1"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        data = pd.read_csv(url)
        # Creating new index to start from 2 and ignore header
        data["Index No."] = range(2, len(data)+2)
        # Change object to datetime
        data["Closeing Date"] = to_datetime(data["Closeing Date"]) 
        # Create dataframe of all data with "Closing date" coming within four days
        dueData = data[(data["Closeing Date"]+ pd.DateOffset(days=-4))== pd.to_datetime("today").strftime("%m/%d/%Y")]
        closingDue = dueData[dueData["Employee In Charge "].notnull()]
        if closingDue.empty == False:
            emailContent = f"This is an automatic reminder that the following contract(s) are closing within four days:\
                \n{closingDue[['Index No.','Title', 'Contract Number', 'Employee In Charge ']].to_string(index=False)}"
            sendEmail(emailContent)
        # print(emailContent)

    except Exception as error:
        log_message = Template('$error').substitute(error=error)
        logging.error(log_message)

# gcloud functions deploy "SEND_EMAIL" --entry-point main --runtime python37 --trigger-resource "SEND_EMAIL_EVENT" --trigger-event google.pubsub.topic.publish --timeout 540s --project projectName