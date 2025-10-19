from twilio.rest import Client

def send_message(number,message):
    account_sid = 'AC2cf2999e6243491028eef6eede3d6fc1'
    auth_token = '4296fc6b8dd850cbf3a7dbbbdf26f866'
    client = Client(account_sid, auth_token)


    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:+91{number}'
        )
        return {f"message_id":message.sid,
                "status":"success"}

    except Exception as e:
        return {f"Failed to send message : {e}"}


print(send_message(8177809890,"test"))