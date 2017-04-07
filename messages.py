import attr


@attr.s()
class Message:
    text = attr.ib()
    incoming = attr.ib()
    unique_key = attr.ib()
    timestamp = attr.ib()
    service_name = attr.ib()
    images = attr.ib(default=[])

    def to_json(self):
        return {
            'text': self.text,
            'service': self.service_name,
            'incoming': self.incoming,
            'images': self.images
        }


@attr.s()
class MessageStream:
    contact  = attr.ib()
    messages = attr.ib()