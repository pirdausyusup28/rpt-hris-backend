class Model:
    def __init__(self):
        self.data = []
        
    def add_item(self, item):
        self.data.append(item)
        
    def get_items(self):
        return self.data
