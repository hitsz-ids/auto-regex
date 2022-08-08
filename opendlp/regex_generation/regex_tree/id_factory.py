
class IDFactory:
    id = 0

    @classmethod
    def next_id(cls):
        cls.id += 1
        return cls.id
