from twilio.rest import Client

def send_message(number,message):
    account_sid = 'AC2cf2999e6243491028eef6eede3d6fc1'
    auth_token = '1ad2bafc53427f06fb1325eb794cf5dc'
    client = Client(account_sid, auth_token)


    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:+91{number}'
        )

    except Exception as e:
        print(f"Failed to send message : {e}")


