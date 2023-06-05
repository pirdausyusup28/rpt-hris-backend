class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def add_item(self, item):
        self.model.add_item(item)
        
    def show_items(self):
        items = self.model.get_items()
        self.view.show_items(items)
