class SimpleLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleLocation):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)