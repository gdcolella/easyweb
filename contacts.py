import attr
import service_configs
import shortuuid

@attr.s()
class Contact(object):
    name = attr.ib()
    service_names = attr.ib()
    key = attr.ib()
    image = attr.ib(default='')

    def to_dict(self):
        return {
            'name': self.name,
            'image': self.image,
            'key': self.key
        }


UNKNOWN = Contact(name="Unknown", service_names={}, key=shortuuid.random())

class ContactProvider():
    def __init__(self):
        self.contacts = []
        people = service_configs.get_config("contacts")
        for person in people:
            self.contacts.append(Contact(
                name=person['name'],
                image=person.get('image', ''),
                key=shortuuid.random(),
                service_names={
                    service: names
                    for service, names in person['services'].items()
                },
            ))

    def find_contact(self, service, service_key):
        for contact in self.contacts:
            if service in contact.service_names:
                if service_key in contact.service_names[service]:
                    return contact
        print("Didn't find {}:{}".format(service_key, service))
        return UNKNOWN