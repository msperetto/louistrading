# Domain class
class Strategy:
    def __init__(self, id: int, name: str, enabled: bool, operation_type: str):
        self.id = id
        self.name = name
        self.enabled = enabled
        self.operation_type = operation_type 

    def __repr__(self):
        return f"Strategy(id={self.id}, name='{self.name}', enabled={self.enabled}, operation_type='{self.operation_type}')"