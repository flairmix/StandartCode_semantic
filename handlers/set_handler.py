from PySide6.QtWidgets import QTreeWidgetItem
from models import Expression, ObjectSet, Property
from dialogs import SetDialog, PropertyDialog


class SetHandler:
    def __init__(self, window):
        self.window = window

    def add_set(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return
        expr = current_item.data(0, 1)
        if not isinstance(expr, Expression):
            return
        dialog = SetDialog(self.window)
        if dialog.exec():
            set_name = dialog.set_name.text()
            if set_name:
                obj_set = ObjectSet(set_name)
                expr.add_set(obj_set)
                set_item = QTreeWidgetItem([f"Множество: {set_name}"])
                set_item.setData(0, 1, obj_set)
                props_item = QTreeWidgetItem(["Свойства"])
                props_item.setData(0, 1, {"type": "props", "parent": obj_set})
                set_item.addChild(props_item)
                current_item.addChild(set_item)
                current_item.setExpanded(True)

    def add_property(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return
        item_data = current_item.data(0, 1)

        if isinstance(item_data, ObjectSet):
            obj_set = item_data
            props_container = next((current_item.child(i)
                                     for i in range(current_item.childCount())
                                     if current_item.child(i).text(0) == "Свойства"), None)
        elif isinstance(item_data, dict) and item_data.get("type") == "props":
            obj_set = item_data.get("parent")
            props_container = current_item
        else:
            return

        dialog = PropertyDialog(self.window)
        if dialog.exec():
            new_prop = Property(
                dialog.code.text(),
                dialog.name.text(),
                dialog.unit.text(),
                dialog.logic_relation.currentText(),
                dialog.value.text()
            )
            obj_set.add_property(new_prop)
            prop_item = QTreeWidgetItem([str(new_prop)])
            props_container.addChild(prop_item)
            props_container.setExpanded(True)