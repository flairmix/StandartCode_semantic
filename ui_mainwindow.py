from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QTreeWidget, QTreeWidgetItem
from models import Property, ObjectEntity, Expression, ObjectSet
from ui_main import ExpressionDialog, ObjectDialog, PropertyDialog, SetDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop приложение")
        self.resize(500, 500)

        self.expressions = []
        self.object_map = {}

        self.main_layout = QVBoxLayout()

        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setFixedHeight(100)
        self.description_text.setPlainText("Добро пожаловать! Это простое приложение для работы с объектами и их свойствами.")
        self.main_layout.addWidget(QLabel("Описание интерфейса:"))
        self.main_layout.addWidget(self.description_text)

        btn_layout = QHBoxLayout()

        self.add_expr_button = QPushButton("Добавить выражение")
        self.add_expr_button.clicked.connect(self.add_expression)
        btn_layout.addWidget(self.add_expr_button)

        self.add_set_button = QPushButton("Добавить множество")
        self.add_set_button.clicked.connect(self.add_set)
        self.add_set_button.setEnabled(False)
        btn_layout.addWidget(self.add_set_button)

        self.add_object_button = QPushButton("Добавить объект")
        self.add_object_button.clicked.connect(self.add_object)
        self.add_object_button.setEnabled(False)
        btn_layout.addWidget(self.add_object_button)

        self.add_prop_button = QPushButton("Добавить свойство")
        self.add_prop_button.clicked.connect(self.add_property)
        self.add_prop_button.setEnabled(False)
        btn_layout.addWidget(self.add_prop_button)

        self.edit_button = QPushButton("Редактировать выбранное")
        self.edit_button.clicked.connect(self.edit_selected)
        self.edit_button.setEnabled(False)
        btn_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить выбранное")
        self.delete_button.clicked.connect(self.delete_selected)
        self.delete_button.setEnabled(False)
        btn_layout.addWidget(self.delete_button)

        self.add_relation_button = QPushButton("Добавить отношение")
        self.add_relation_button.setEnabled(False)
        btn_layout.addWidget(self.add_relation_button)

        self.main_layout.addLayout(btn_layout)

        self.object_tree = QTreeWidget()
        self.object_tree.setHeaderLabels(["Структура: выражения, множества, объекты и свойства"])
        self.object_tree.currentItemChanged.connect(self.on_object_selected)
        self.main_layout.addWidget(QLabel("Список объектов:"))
        self.main_layout.addWidget(self.object_tree)

        self.setLayout(self.main_layout)

    def add_expression(self):
        dialog = ExpressionDialog(self)
        if dialog.exec():
            expr_text = dialog.expr_text.text()
            if expr_text:
                expr = Expression(expr_text)
                self.expressions.append(expr)
                expr_item = QTreeWidgetItem([f"Выражение: {expr_text}"])
                expr_item.setData(0, 1, expr)
                self.object_tree.addTopLevelItem(expr_item)

    def add_set(self):
        current_item = self.object_tree.currentItem()
        if not current_item:
            return
        expr = current_item.data(0, 1)
        if not isinstance(expr, Expression):
            return
        dialog = SetDialog(self)
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

    def add_object(self):
        current_item = self.object_tree.currentItem()
        if not current_item:
            return
        obj_set = current_item.data(0, 1)
        if not isinstance(obj_set, ObjectSet):
            return
        dialog = ObjectDialog(self)
        if dialog.exec():
            obj_name = dialog.obj_name.text()
            obj_code = dialog.obj_code.text()
            obj_ksi = dialog.obj_ksi.text()
            if obj_name:
                new_object = ObjectEntity(obj_name, obj_code, obj_ksi)
                obj_set.add_object(new_object)
                self.object_map[obj_code] = new_object
                obj_item = QTreeWidgetItem([str(new_object)])
                obj_item.setData(0, 1, obj_code)
                current_item.addChild(obj_item)
                current_item.setExpanded(True)

    def add_property(self):
        current_item = self.object_tree.currentItem()
        if not current_item:
            return
        parent_item = current_item.parent()
        item_data = current_item.data(0, 1)
        if isinstance(item_data, ObjectSet):
            obj_set = item_data
            props_container = None
            for i in range(current_item.childCount()):
                child = current_item.child(i)
                if child.text(0) == "Свойства":
                    props_container = child
                    break
        elif isinstance(item_data, dict) and item_data.get("type") == "props":
            obj_set = item_data.get("parent")
            props_container = current_item
        else:
            return
        dialog = PropertyDialog(self)
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

    def delete_selected(self):
        current_item = self.object_tree.currentItem()
        if not current_item:
            return
        parent_item = current_item.parent()
        item_data = current_item.data(0, 1)
        if isinstance(item_data, Expression):
            index = self.object_tree.indexOfTopLevelItem(current_item)
            self.object_tree.takeTopLevelItem(index)
            return
        if isinstance(item_data, ObjectSet):
            if parent_item:
                parent_item.removeChild(current_item)
            return
        if isinstance(item_data, str) and parent_item:
            if item_data in self.object_map:
                del self.object_map[item_data]
            parent_item.removeChild(current_item)
            return
        if parent_item:
            grandparent = parent_item.parent()
            if grandparent:
                grand_data = grandparent.data(0, 1)
                if isinstance(grand_data, ObjectSet):
                    grand_data.remove_property_by_str(current_item.text(0))
                    parent_item.removeChild(current_item)

    def edit_selected(self):
        current_item = self.object_tree.currentItem()
        if not current_item:
            return
        item_data = current_item.data(0, 1)
        if isinstance(item_data, Expression):
            dialog = ExpressionDialog(self)
            dialog.expr_text.setText(item_data.text)
            if dialog.exec():
                item_data.text = dialog.expr_text.text()
                current_item.setText(0, f"Выражение: {item_data.text}")
        elif isinstance(item_data, ObjectSet):
            dialog = SetDialog(self)
            dialog.set_name.setText(item_data.name)
            if dialog.exec():
                item_data.name = dialog.set_name.text()
                current_item.setText(0, f"Множество: {item_data.name}")
        elif isinstance(item_data, str):
            obj = self.object_map.get(item_data)
            if obj:
                dialog = ObjectDialog(self, obj)
                if dialog.exec():
                    obj.name = dialog.obj_name.text()
                    obj.ksi = dialog.obj_ksi.text()
                    current_item.setText(0, str(obj))
        elif current_item.parent() and current_item.parent().text(0) == "Свойства":
            obj_set = current_item.parent().data(0, 1).get("parent")
            for prop in obj_set.properties:
                if str(prop) == current_item.text(0):
                    dialog = PropertyDialog(self, prop)
                    if dialog.exec():
                        prop.code = dialog.code.text()
                        prop.name = dialog.name.text()
                        prop.unit = dialog.unit.text()
                        prop.logic_relation = dialog.logic_relation.currentText()
                        prop.value = dialog.value.text()
                        current_item.setText(0, str(prop))
                    break

    def on_object_selected(self, current, previous):
        self.add_expr_button.setEnabled(True)
        self.add_set_button.setEnabled(False)
        self.add_object_button.setEnabled(False)
        self.add_prop_button.setEnabled(False)
        self.add_relation_button.setEnabled(False)
        self.edit_button.setEnabled(current is not None)
        self.delete_button.setEnabled(current is not None)
        if not current:
            return
        item_data = current.data(0, 1)
        if isinstance(item_data, Expression):
            self.add_set_button.setEnabled(True)
        elif isinstance(item_data, ObjectSet):
            self.add_object_button.setEnabled(True)
            self.add_prop_button.setEnabled(True)
        elif isinstance(item_data, dict) and item_data.get("type") == "props":
            self.add_prop_button.setEnabled(True)
    # если хочешь — перенесу их тоже
