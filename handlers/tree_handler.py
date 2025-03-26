from .set_handler import SetHandler
from .object_handler import ObjectHandler
from .relation_handler import RelationHandler


class ObjectTreeHandler:
    def __init__(self, window):
        self.window = window
        self.set_handler = SetHandler(window)
        self.object_handler = ObjectHandler(window)
        self.relation_handler = RelationHandler(window)

    def add_set(self):
        self.set_handler.add_set()

    def add_object(self):
        self.object_handler.add_object()

    def add_property(self):
        self.set_handler.add_property()

    def delete_selected(self):
        self.object_handler.delete_selected()

    def edit_selected(self):
        self.object_handler.edit_selected()

    def add_relation(self):
        self.relation_handler.add_relation()

    def on_object_selected(self, current, previous):
        self.object_handler.on_object_selected(current, previous)
