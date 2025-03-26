# handlers/__init__.py — агрегатор





# from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
# from models import Expression, ObjectSet, ObjectEntity, Property, Relation
# from dialogs import ExpressionDialog, RelationDialog, SetDialog, ObjectDialog, PropertyDialog


# class ExpressionHandler:
#     def __init__(self, window):
#         self.window = window

#     def add_expression(self):
#         dialog = ExpressionDialog(self.window)
#         if dialog.exec():
#             expr_text = dialog.expr_text.text()
#             if expr_text:
#                 expr = Expression(expr_text)
#                 self.window.expressions.append(expr)
#                 expr_item = QTreeWidgetItem([f"Выражение: {expr_text}"])
#                 expr_item.setData(0, 1, expr)
#                 self.window.object_tree.addTopLevelItem(expr_item)


# class ObjectTreeHandler:
#     def __init__(self, window):
#         self.window = window

#     def add_set(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return
#         expr = current_item.data(0, 1)
#         if not isinstance(expr, Expression):
#             return
#         dialog = SetDialog(self.window)
#         if dialog.exec():
#             set_name = dialog.set_name.text()
#             if set_name:
#                 obj_set = ObjectSet(set_name)
#                 expr.add_set(obj_set)
#                 set_item = QTreeWidgetItem([f"Множество: {set_name}"])
#                 set_item.setData(0, 1, obj_set)
#                 props_item = QTreeWidgetItem(["Свойства"])
#                 props_item.setData(0, 1, {"type": "props", "parent": obj_set})
#                 set_item.addChild(props_item)
#                 current_item.addChild(set_item)
#                 current_item.setExpanded(True)

#     def add_object(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return
#         obj_set = current_item.data(0, 1)
#         if not isinstance(obj_set, ObjectSet):
#             return
#         dialog = ObjectDialog(self.window)
#         if dialog.exec():
#             obj_name = dialog.obj_name.text()
#             obj_code = dialog.obj_code.text()
#             obj_ksi = dialog.obj_ksi.text()
#             if obj_name:
#                 new_object = ObjectEntity(obj_name, obj_code, obj_ksi)
#                 obj_set.add_object(new_object)
#                 self.window.object_map[obj_code] = new_object
#                 obj_item = QTreeWidgetItem([str(new_object)])
#                 obj_item.setData(0, 1, obj_code)
#                 current_item.addChild(obj_item)

#                 # Добавляем отношения объекта (если есть)
#                 if new_object.relations:
#                     relations_container = QTreeWidgetItem(["Отношения"])
#                     relations_container.setData(0, 1, {"type": "relations"})
#                     for rel in new_object.relations:
#                         rel_item = QTreeWidgetItem([str(rel)])
#                         rel_item.setData(0, 1, rel)
#                         relations_container.addChild(rel_item)
#                     obj_item.addChild(relations_container)

#                 current_item.setExpanded(True)
#                 new_object = ObjectEntity(obj_name, obj_code, obj_ksi)
#                 obj_set.add_object(new_object)
#                 self.window.object_map[obj_code] = new_object
#                 obj_item = QTreeWidgetItem([str(new_object)])
#                 obj_item.setData(0, 1, obj_code)
#                 current_item.addChild(obj_item)
#                 current_item.setExpanded(True)

#     def add_property(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return
#         parent_item = current_item.parent()
#         item_data = current_item.data(0, 1)
#         if isinstance(item_data, ObjectSet):
#             obj_set = item_data
#             props_container = None
#             for i in range(current_item.childCount()):
#                 child = current_item.child(i)
#                 if child.text(0) == "Свойства":
#                     props_container = child
#                     break
#         elif isinstance(item_data, dict) and item_data.get("type") == "props":
#             obj_set = item_data.get("parent")
#             props_container = current_item
#         else:
#             return
#         dialog = PropertyDialog(self.window)
#         if dialog.exec():
#             new_prop = Property(
#                 dialog.code.text(),
#                 dialog.name.text(),
#                 dialog.unit.text(),
#                 dialog.logic_relation.currentText(),
#                 dialog.value.text()
#             )
#             obj_set.add_property(new_prop)
#             prop_item = QTreeWidgetItem([str(new_prop)])
#             props_container.addChild(prop_item)
#             props_container.setExpanded(True)

#     def delete_selected(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return
#         parent_item = current_item.parent()
#         item_data = current_item.data(0, 1)
#         if isinstance(item_data, Expression):
#             index = self.window.object_tree.indexOfTopLevelItem(current_item)
#             self.window.object_tree.takeTopLevelItem(index)
#             return
#         if isinstance(item_data, ObjectSet):
#             if parent_item:
#                 parent_item.removeChild(current_item)
#             return
#         if isinstance(item_data, str) and parent_item:
#             if item_data in self.window.object_map:
#                 del self.window.object_map[item_data]
#             parent_item.removeChild(current_item)
#             return
#         if parent_item:
#             grandparent = parent_item.parent()
#             if grandparent:
#                 grand_data = grandparent.data(0, 1)
#                 if isinstance(grand_data, ObjectSet):
#                     grand_data.remove_property_by_str(current_item.text(0))
#                     parent_item.removeChild(current_item)

#     def edit_selected(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return
#         item_data = current_item.data(0, 1)
#         if isinstance(item_data, Expression):
#             dialog = ExpressionDialog(self.window)
#             dialog.expr_text.setText(item_data.text)
#             if dialog.exec():
#                 item_data.text = dialog.expr_text.text()
#                 current_item.setText(0, f"Выражение: {item_data.text}")
#         elif isinstance(item_data, ObjectSet):
#             dialog = SetDialog(self.window)
#             dialog.set_name.setText(item_data.name)
#             if dialog.exec():
#                 item_data.name = dialog.set_name.text()
#                 current_item.setText(0, f"Множество: {item_data.name}")
#         elif isinstance(item_data, str):
#             obj = self.window.object_map.get(item_data)
#             if obj:
#                 dialog = ObjectDialog(self.window, obj)
#                 if dialog.exec():
#                     obj.name = dialog.obj_name.text()
#                     obj.ksi = dialog.obj_ksi.text()
#                     current_item.setText(0, str(obj))
#         elif current_item.parent() and current_item.parent().text(0) == "Свойства":
#             obj_set = current_item.parent().data(0, 1).get("parent")
#             for prop in obj_set.properties:
#                 if str(prop) == current_item.text(0):
#                     dialog = PropertyDialog(self.window, prop)
#                     if dialog.exec():
#                         prop.code = dialog.code.text()
#                         prop.name = dialog.name.text()
#                         prop.unit = dialog.unit.text()
#                         prop.logic_relation = dialog.logic_relation.currentText()
#                         prop.value = dialog.value.text()
#                         current_item.setText(0, str(prop))
#                     break

#     def on_object_selected(self, current, previous):
#         self.window.add_expr_button.setEnabled(True)
#         self.window.add_set_button.setEnabled(False)
#         self.window.add_object_button.setEnabled(False)
#         self.window.add_prop_button.setEnabled(False)
#         self.window.add_relation_button.setEnabled(False)
#         self.window.edit_button.setEnabled(current is not None)
#         self.window.delete_button.setEnabled(current is not None)
#         if not current:
#             return
#         item_data = current.data(0, 1)

#         if isinstance(item_data, Expression):
#             self.window.add_set_button.setEnabled(True)
#             sets = item_data.sets
#             if len(sets) >= 2:
#                 self.window.add_relation_button.setEnabled(True)
#         elif isinstance(item_data, ObjectSet):
#             self.window.add_object_button.setEnabled(True)
#             self.window.add_prop_button.setEnabled(True)
#         elif isinstance(item_data, dict) and item_data.get("type") == "props":
#             self.window.add_prop_button.setEnabled(True)

#     def add_relation(self):
#         current_item = self.window.object_tree.currentItem()
#         if not current_item:
#             return

#         # Найти ближайшее выражение
#         expr_item = current_item
#         expr = None
#         while expr_item:
#             expr_data = expr_item.data(0, 1)
#             if isinstance(expr_data, Expression):
#                 expr = expr_data
#                 break
#             expr_item = expr_item.parent()

#         if not expr:
#             return

#         # Получить все объекты из всех множеств выражения
#         object_names = [obj_set.name for obj_set in expr.sets]

#         dialog = RelationDialog(self.window, object_names, current_subject=None, current_object=None, current_relation=None)
#         if dialog.exec():
#             subject_name, relation, object_name = dialog.get_values()

#             # Запрет на выбор одного и того же множества
#             if subject_name == object_name:
#                 QMessageBox.warning(self.window, "Ошибка", "Субъект и объект не могут совпадать")
#                 return

#             subject = next((obj for obj in self.window.object_map.values() if obj.name == subject_name), None)
#             obj = next((obj for obj in self.window.object_map.values() if obj.name == object_name), None)

#             if subject and obj:
#                 relation_obj = Relation(subject, relation, obj)

#                 subject.relations.append(relation_obj)
#                 obj.relations.append(relation_obj)

#                 self.update_relation_in_tree(subject, relation_obj, current_item)
#                 self.update_relation_in_tree(obj, relation_obj, current_item)

#                 # Обновим представление у объектов в дереве
#                 self.refresh_object_relations_in_tree(subject)
#                 self.refresh_object_relations_in_tree(obj)

#     def update_relation_in_tree(self, obj, relation, parent_item):
#         relation_item = QTreeWidgetItem([f"Отношение: {relation.relation} {relation.subject.name} → {relation.obj.name}"])
#         relation_item.setData(0, 1, relation)

#         # Поиск узла множества, чтобы отобразить там отношение
#         root = self.window.object_tree.invisibleRootItem()
#         stack = [root.child(i) for i in range(root.childCount())]

#         while stack:
#             item = stack.pop()
#             data = item.data(0, 1)
#             if isinstance(data, ObjectSet) and (data.name == obj.name or data.name == relation.subject.name):
#                 # Найти или создать контейнер для отношений
#                 relations_container = None
#                 for i in range(item.childCount()):
#                     if item.child(i).text(0) == "Отношения":
#                         relations_container = item.child(i)
#                         break
#                 if not relations_container:
#                     relations_container = QTreeWidgetItem(["Отношения"])
#                     relations_container.setData(0, 1, {"type": "relations"})
#                     item.addChild(relations_container)
#                 relations_container.addChild(relation_item)
#                 relations_container.setExpanded(True)
#                 item.setExpanded(True)
#                 break
#             for i in range(item.childCount()):
#                 stack.append(item.child(i))
        

#     def refresh_object_relations_in_tree(self, obj):
#         root = self.window.object_tree.invisibleRootItem()
#         stack = [root.child(i) for i in range(root.childCount())]

#         while stack:
#             item = stack.pop()
#             data = item.data(0, 1)
#             if isinstance(data, str) and data == obj.code:
#                 # Удаляем старый контейнер "Отношения"
#                 for i in range(item.childCount()):
#                     if item.child(i).text(0) == "Отношения":
#                         item.removeChild(item.child(i))
#                         break

#                 # Создаем новый
#                 if obj.relations:
#                     container = QTreeWidgetItem(["Отношения"])
#                     container.setData(0, 1, {"type": "relations"})
#                     for rel in obj.relations:
#                         rel_item = QTreeWidgetItem([str(rel)])
#                         rel_item.setData(0, 1, rel)
#                         container.addChild(rel_item)
#                     item.addChild(container)
#                     container.setExpanded(True)
#                 break
#             for i in range(item.childCount()):
#                 stack.append(item.child(i))
