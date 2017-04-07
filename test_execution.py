
import messages
import contacts
import texting_service

import services

texts = texting_service.TwilioService()
contacts = contacts.ContactProvider()


service = services.MessagingSystem(contacts, [texts])

for stream in service.get_messages():
    print("{}: {}".format(stream.contact.name, len(stream.messages)))
    print("\t\tConversation: ")
    for message in stream.messages:
        print("\t\t"+message.text)