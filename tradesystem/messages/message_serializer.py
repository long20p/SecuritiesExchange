from json import JSONEncoder

class MessageSerializer(JSONEncoder):
    
    def default(self, obj):
        return obj.__dict__