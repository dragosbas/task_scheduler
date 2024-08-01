import uuid


class BaseClass:
    def __init__(self):
        self.uuid = uuid.uuid4()

    def get_uuid(self) -> uuid:
        return self.uuid
