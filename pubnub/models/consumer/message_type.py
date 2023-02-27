class PNMessageType:
    pn_message_type: str = None
    message_type: str = None
    _type_mapping = {
        'None': 'message',
        '0': 'message',
        '1': 'signal',
        '2': 'object',
        '3': 'message_action',
        '4': 'file',
    }

    def __init__(self, message_type: str = None) -> None:
        self.message_type = message_type

    def set_pn_message_type(self, pn_message_type: str):
        self.pn_message_type = self._type_mapping[str(pn_message_type)]
        return self

    def from_response(message_type: str = None, pn_message_type: str = None):
        return PNMessageType(message_type).set_pn_message_type(pn_message_type)

    def __str__(self) -> str:
        return self.message_type if self.message_type is not None else str(self.pn_message_type)

    def toJSON(self) -> str:
        return str(self)