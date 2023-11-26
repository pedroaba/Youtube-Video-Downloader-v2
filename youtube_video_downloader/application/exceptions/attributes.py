class NonAssignableAttribute(Exception):
    def __init__(self, attribute_name: str):
        super(NonAssignableAttribute, self).__init__(f"Attrinute '{attribute_name}' is not assignable!")
