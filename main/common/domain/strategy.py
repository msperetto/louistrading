# Domain class
class Strategy:
    def __init__(self, id: int, name: str, enabled: bool):
        self.id = id
        self.name = name
        self.enabled = enabled

    def __repr__(self):
        return f"Strategy(id={self.id}, name='{self.name}', enabled={self.enabled})"