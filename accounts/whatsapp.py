from twilio.rest import Client
from django.conf import settings


def send_whatsapp_pdf(phone_number, pdf_url, message):
    """
    phone_number: 'whatsapp:+91XXXXXXXXXX'
    pdf_url: public https url of PDF
    """

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=phone_number,
        body=message,
        media_url=[pdf_url]
    )
