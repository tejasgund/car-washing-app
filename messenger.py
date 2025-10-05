from twilio.rest import Client
import os

def send_message(number,message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:+91{number}'
        )

    except Exception as e:
        print(f"Failed to send message : {e}")


