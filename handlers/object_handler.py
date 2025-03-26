from PySide6.QtWidgets import QTreeWidgetItem
from models import ObjectEntity, ObjectSet, Expression
from dialogs import ObjectDialog, SetDialog, ExpressionDialog, PropertyDialog


class ObjectHandler:
    def __init__(self, window):
        self.window = window

    def add_object(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return
        obj_set = current_item.data(0, 1)
        if not isinstance(obj_set, ObjectSet):
            return
        dialog = ObjectDialog(self.window, searcher=self.window.searcher)
        if dialog.exec():
            obj_name = dialog.obj_name.text()
            obj_code = dialog.obj_code.text()
            obj_ksi = dialog.obj_ksi.text()
            if obj_name:
                new_object = ObjectEntity(obj_name, obj_code, obj_ksi)
                obj_set.add_object(new_object)
                self.window.object_map[obj_code] = new_object
                obj_item = QTreeWidgetItem([str(new_object)])
                obj_item.setData(0, 1, obj_code)
                current_item.addChild(obj_item)
                current_item.setExpanded(True)

    def delete_selected(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return
        parent_item = current_item.parent()
        item_data = current_item.data(0, 1)

        if isinstance(item_data, Expression):
            index = self.window.object_tree.indexOfTopLevelItem(current_item)
            self.window.object_tree.takeTopLevelItem(index)
        elif isinstance(item_data, ObjectSet):
            if parent_item:
                parent_item.removeChild(current_item)
        elif isinstance(item_data, str):
            if parent_item:
                if item_data in self.window.object_map:
                    del self.window.object_map[item_data]
                parent_item.removeChild(current_item)
        elif parent_item:
            grandparent = parent_item.parent()
            if grandparent:
                grand_data = grandparent.data(0, 1)
                if isinstance(grand_data, ObjectSet):
                    grand_data.remove_property_by_str(current_item.text(0))
                    parent_item.removeChild(current_item)

    def edit_selected(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return
        item_data = current_item.data(0, 1)

        if isinstance(item_data, Expression):
            dialog = ExpressionDialog(self.window)
            dialog.expr_text.setText(item_data.text)
            if dialog.exec():
                item_data.text = dialog.expr_text.text()
                current_item.setText(0, f"Выражение: {item_data.text}")

        elif isinstance(item_data, ObjectSet):
            dialog = SetDialog(self.window)
            dialog.set_name.setText(item_data.name)
            if dialog.exec():
                item_data.name = dialog.set_name.text()
                current_item.setText(0, f"Множество: {item_data.name}")

        elif isinstance(item_data, str):
            obj = self.window.object_map.get(item_data)
            if obj:
                dialog = ObjectDialog(self.window, obj)
                if dialog.exec():
                    obj.name = dialog.obj_name.text()
                    obj.ksi = dialog.obj_ksi.text()
                    current_item.setText(0, str(obj))

        elif current_item.parent() and current_item.parent().text(0) == "Свойства":
            obj_set = current_item.parent().data(0, 1).get("parent")
            for prop in obj_set.properties:
                if str(prop) == current_item.text(0):
                    dialog = PropertyDialog(self.window, prop)
                    if dialog.exec():
                        prop.code = dialog.code.text()
                        prop.name = dialog.name.text()
                        prop.unit = dialog.unit.text()
                        prop.logic_relation = dialog.logic_relation.currentText()
                        prop.value = dialog.value.text()
                        current_item.setText(0, str(prop))
                    break

    def on_object_selected(self, current, previous):
        self.window.add_expr_button.setEnabled(True)
        self.window.add_set_button.setEnabled(False)
        self.window.add_object_button.setEnabled(False)
        self.window.add_prop_button.setEnabled(False)
        self.window.add_relation_button.setEnabled(False)
        self.window.edit_button.setEnabled(current is not None)
        self.window.delete_button.setEnabled(current is not None)

        if not current:
            return

        item_data = current.data(0, 1)

        if isinstance(item_data, Expression):
            self.window.add_set_button.setEnabled(True)
            if len(item_data.sets) >= 2:
                self.window.add_relation_button.setEnabled(True)

        elif isinstance(item_data, ObjectSet):
            self.window.add_object_button.setEnabled(True)
            self.window.add_prop_button.setEnabled(True)

        elif isinstance(item_data, dict) and item_data.get("type") == "props":
            self.window.add_prop_button.setEnabled(True)