import messages

from twilio.rest import Client
import service_configs

class TwilioService:
    def __init__(self):
        conf = service_configs.get_config('twilio')
        self.account_sid = conf['account_sid']
        self.auth_token = conf['auth_token']

        self.twilio_client = Client(self.account_sid, self.auth_token)

    def service_name(self):
        return "sms"

    def _image_url(self, media_object):
        root = "https://{}:{}@api.twilio.com".format(self.account_sid, self.auth_token)
        url = root + media_object.uri.replace('.json','')
        return url

    def get_messages(self):
        messages_by_sender = {}
        for message in self.twilio_client.messages.list():
            contact_key = message.from_ if message.direction == 'inbound' else message.to

            messages_by_sender.setdefault(contact_key, []).append(
                messages.Message(
                    text=message.body,
                    incoming=message.direction=='inbound',
                    unique_key=message.sid,
                    timestamp=message.date_sent,
                    service_name=self.service_name(),
                    images=[self._image_url(media) for media in message.media.list()] if int(message.num_media) > 0 else [],
                )
            )
        return messages_by_sender




