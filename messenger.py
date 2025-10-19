from twilio.rest import Client

def send_message(number, message):
    account_sid = 'AC2cf2999e6243491028eef6eede3d6fc1'
    auth_token = 'b2e582999c532269cd8310be6fd8f334'
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_='+16813223394',         # Your Twilio SMS-enabled number
            body=message,
            to=f'+91{number}'             # Customer's phone number with country code
        )
        return {f"message_id": message.sid,
                "status": "success"}

    except Exception as e:
        return {f"Failed to send message": str(e)}

