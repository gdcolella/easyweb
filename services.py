import contacts
import messages


class MessagingSystem:
    def __init__(self, contacts, providers):
        self.providers = providers
        self.contacts = contacts
        self.services = {
            provider.service_name()
            for provider in self.providers
        }
        self.get_messages()

    def get_messages(self):
        streams = []
        for provider in self.providers:
            service = provider.service_name()
            messages_by_id = provider.get_messages()
            for service_key, service_messages in messages_by_id.items():
                contact = self.contacts.find_contact(service, service_key)
                stream = messages.MessageStream(contact=contact, messages=service_messages)
                streams.append(stream)

        # Recombine the streams of contacts.
        knit_streams = []
        for stream in streams:
            this_stream = [s for s in knit_streams if s.contact == stream.contact]
            if this_stream:
                this_stream = this_stream[0]
                this_stream.messages = (this_stream.messages + stream.messages)
            else:
                this_stream = messages.MessageStream(contact=stream.contact, messages=stream.messages[::])
                knit_streams.append(this_stream)

        for knit_stream in knit_streams:
            knit_stream.messages = sorted(knit_stream.messages, key = lambda msg: msg.timestamp, reverse= True)

        self.saved_streams = knit_streams
        return knit_streams

    def get_messages_with(self, contact_key):
        for message_stream in self.get_messages():
            if message_stream.contact.key == contact_key:
                return message_stream
        return None






