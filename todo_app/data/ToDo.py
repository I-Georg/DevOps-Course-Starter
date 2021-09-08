class ToDo:
    def __init__(self, id, name, last_modified, status="To Do"):
        self.id = id
        self.name = name
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def from_mongo_db_entry(cls, entry):
        return cls(
            entry['_id'],
            entry['name'],
            entry['last_modified'],
            entry['status']
        )
