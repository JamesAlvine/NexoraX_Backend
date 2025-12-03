def send_sms(phone, message, provider='twilio'):
    if provider == 'twilio':
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(body=message, from_='+1234567890', to=phone)
    elif provider == 'africas_talking':
        # Africa's Talking API call
        pass