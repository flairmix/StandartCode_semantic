# import sys, uuid
# from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
#                                QHBoxLayout, QPushButton, QLineEdit,
#                                QDialog, QFormLayout, QTreeWidget, QTreeWidgetItem, QComboBox, QMessageBox, QTextEdit)

# class Property:
#     def __init__(self, code, name, unit, logic_relation, value):
#         self.code = code
#         self.name = name
#         self.unit = unit
#         self.logic_relation = logic_relation
#         self.value = value

#     def __str__(self):
#         return f"Code: {self.code}, Name: {self.name}, Unit: {self.unit}, Logic: {self.logic_relation}, Value: {self.value}"

# class ObjectEntity:
#     def __init__(self, name, code, ksi):
#         self.name = name
#         self.code = code
#         self.ksi = ksi
#         self.properties = []

#     def add_property(self, prop):
#         self.properties.append(prop)

#     def remove_property_by_str(self, prop_str):
#         self.properties = [p for p in self.properties if str(p) != prop_str]

# class Expression:
#     def __init__(self, text):
#         self.text = text
#         self.objects = []

#     def add_object(self, obj):
#         self.objects.append(obj)

# class ExpressionDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Выражение")
#         layout = QFormLayout()

#         self.expr_text = QLineEdit()
#         layout.addRow("Текст выражения:", self.expr_text)

#         ok_button = QPushButton("ОК")
#         ok_button.clicked.connect(self.accept)
#         layout.addWidget(ok_button)

#         self.setLayout(layout)

# class PropertyDialog(QDialog):
#     def __init__(self, parent=None, prop=None):
#         super().__init__(parent)
#         self.setWindowTitle("Свойство")
#         layout = QFormLayout()

#         self.code = QLineEdit()
#         self.name = QLineEdit()
#         self.unit = QLineEdit()
#         self.logic_relation = QComboBox()
#         self.logic_relation.addItems(["==", ">=", "<=", ">", "<"])
#         self.value = QLineEdit()

#         layout.addRow("Name:", self.name)
#         layout.addRow("Code:", self.code)
#         layout.addRow("Unit:", self.unit)
#         layout.addRow("LogicRelation:", self.logic_relation)
#         layout.addRow("Value:", self.value)

#         if prop:
#             self.code.setText(prop.code)
#             self.name.setText(prop.name)
#             self.unit.setText(prop.unit)
#             self.logic_relation.setCurrentText(prop.logic_relation)
#             self.value.setText(prop.value)

#         add_button = QPushButton("ОК")
#         add_button.clicked.connect(self.accept)
#         layout.addWidget(add_button)

#         self.setLayout(layout)

# class ObjectDialog(QDialog):
#     def __init__(self, parent=None, obj=None):
#         super().__init__(parent)
#         self.setWindowTitle("Объект")
#         layout = QFormLayout()

#         self.obj_name = QLineEdit()
#         self.obj_code = QLineEdit(str(uuid.uuid4())[:8])
#         self.obj_code.setReadOnly(True)
#         self.obj_ksi = QLineEdit()
#         layout.addRow("Name:", self.obj_name)
#         layout.addRow("Code:", self.obj_code)
#         layout.addRow("KSI:", self.obj_ksi)

#         if obj:
#             self.obj_name.setText(obj.name)
#             self.obj_code.setText(obj.code)
#             self.obj_ksi.setText(obj.ksi)

#         ok_button = QPushButton("ОК")
#         ok_button.clicked.connect(self.accept)
#         layout.addWidget(ok_button)

#         self.setLayout(layout)

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Desktop приложение")
#         self.resize(500, 500)

#         self.expressions = []
#         self.object_map = {}

#         self.main_layout = QVBoxLayout()

#         self.description_text = QTextEdit()
#         self.description_text.setReadOnly(True)
#         self.description_text.setPlainText("Добро пожаловать! Это простое приложение для работы с объектами и их свойствами.")
#         self.main_layout.addWidget(QLabel("Описание интерфейса:"))
#         self.main_layout.addWidget(self.description_text)

#         btn_layout = QHBoxLayout()

#         self.add_expr_button = QPushButton("Добавить выражение")
#         self.add_expr_button.clicked.connect(self.add_expression)
#         btn_layout.addWidget(self.add_expr_button)

#         self.add_object_button = QPushButton("Добавить объект")
#         self.add_object_button.clicked.connect(self.add_object)
#         btn_layout.addWidget(self.add_object_button)

#         self.add_prop_button = QPushButton("Добавить свойство")
#         self.add_prop_button.clicked.connect(self.add_property)
#         self.add_prop_button.setEnabled(False)
#         btn_layout.addWidget(self.add_prop_button)

#         self.edit_button = QPushButton("Редактировать выбранное")
#         self.edit_button.clicked.connect(self.edit_selected)
#         self.edit_button.setEnabled(False)
#         btn_layout.addWidget(self.edit_button)

#         self.delete_button = QPushButton("Удалить выбранное")
#         self.delete_button.clicked.connect(self.delete_selected)
#         self.delete_button.setEnabled(False)
#         btn_layout.addWidget(self.delete_button)

#         self.add_relation_button = QPushButton("Добавить отношение")
#         self.add_relation_button.setEnabled(False)
#         btn_layout.addWidget(self.add_relation_button)

#         self.main_layout.addLayout(btn_layout)

#         self.object_tree = QTreeWidget()
#         self.object_tree.setHeaderLabels(["Структура: выражения, объекты и свойства"])
#         self.object_tree.currentItemChanged.connect(self.on_object_selected)
#         self.main_layout.addWidget(QLabel("Список объектов:"))
#         self.main_layout.addWidget(self.object_tree)

#         self.setLayout(self.main_layout)

#     def add_expression(self):
#         dialog = ExpressionDialog(self)
#         if dialog.exec():
#             expr_text = dialog.expr_text.text()
#             if expr_text:
#                 expr = Expression(expr_text)
#                 self.expressions.append(expr)
#                 expr_item = QTreeWidgetItem([f"Выражение: {expr_text}"])
#                 expr_item.setData(0, 1, expr)
#                 self.object_tree.addTopLevelItem(expr_item)

#     def add_object(self):
#         current_item = self.object_tree.currentItem()
#         if not current_item:
#             return

#         expr = current_item.data(0, 1)
#         if not isinstance(expr, Expression):
#             return

#         dialog = ObjectDialog(self)
#         if dialog.exec():
#             obj_name = dialog.obj_name.text()
#             obj_code = dialog.obj_code.text()
#             obj_ksi = dialog.obj_ksi.text()
#             if obj_name:
#                 new_object = ObjectEntity(obj_name, obj_code, obj_ksi)
#                 expr.add_object(new_object)
#                 self.object_map[obj_code] = new_object
#                 obj_item = QTreeWidgetItem([f"{obj_name} (ID: {obj_code}) | KSI: {obj_ksi}"])
#                 obj_item.setData(0, 1, obj_code)
#                 current_item.addChild(obj_item)
#                 current_item.setExpanded(True)

#     def on_object_selected(self, current, previous):
#         self.add_prop_button.setEnabled(current and current.parent() is not None and current.parent().data(0, 1))
#         self.add_relation_button.setEnabled(current and current.parent() is not None)
#         self.edit_button.setEnabled(current is not None)
#         self.delete_button.setEnabled(current is not None)

#     def add_property(self):
#         current_item = self.object_tree.currentItem()
#         if current_item and current_item.parent():
#             obj_code = current_item.data(0, 1)
#             dialog = PropertyDialog(self)
#             if dialog.exec():
#                 new_prop = Property(
#                     dialog.code.text(),
#                     dialog.name.text(),
#                     dialog.unit.text(),
#                     dialog.logic_relation.currentText(),
#                     dialog.value.text()
#                 )
#                 if obj_code in self.object_map:
#                     obj = self.object_map[obj_code]
#                     obj.add_property(new_prop)
#                     prop_item = QTreeWidgetItem([str(new_prop)])
#                     current_item.addChild(prop_item)
#                     current_item.setExpanded(True)

#     def delete_selected(self):
#         current_item = self.object_tree.currentItem()
#         if not current_item:
#             return

#         parent_item = current_item.parent()

#         if parent_item is None:
#             index = self.object_tree.indexOfTopLevelItem(current_item)
#             self.object_tree.takeTopLevelItem(index)
#         elif parent_item and parent_item.parent() is None:
#             obj_code = current_item.data(0, 1)
#             if obj_code in self.object_map:
#                 self.object_map.pop(obj_code)
#             parent_item.removeChild(current_item)
#         else:
#             obj_code = parent_item.data(0, 1)
#             prop_str = current_item.text(0)
#             obj = self.object_map.get(obj_code)
#             if obj:
#                 obj.remove_property_by_str(prop_str)
#             parent_item.removeChild(current_item)

#     def edit_selected(self):
#         current_item = self.object_tree.currentItem()
#         if not current_item:
#             return

#         parent_item = current_item.parent()

#         if parent_item and parent_item.parent() is None:
#             obj_code = current_item.data(0, 1)
#             obj = self.object_map.get(obj_code)
#             if obj:
#                 dialog = ObjectDialog(self, obj)
#                 if dialog.exec():
#                     obj.name = dialog.obj_name.text()
#                     obj.ksi = dialog.obj_ksi.text()
#                     current_item.setText(0, f"{obj.name} (ID: {obj.code}) | KSI: {obj.ksi}")
#         elif parent_item and parent_item.parent():
#             obj_code = parent_item.data(0, 1)
#             obj = self.object_map.get(obj_code)
#             prop_str = current_item.text(0)
#             for p in obj.properties:
#                 if str(p) == prop_str:
#                     dialog = PropertyDialog(self, p)
#                     if dialog.exec():
#                         p.code = dialog.code.text()
#                         p.name = dialog.name.text()
#                         p.unit = dialog.unit.text()
#                         p.logic_relation = dialog.logic_relation.currentText()
#                         p.value = dialog.value.text()
#                         current_item.setText(0, str(p))
#                     break

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


import sys
from PySide6.QtWidgets import QApplication
from ui_mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
