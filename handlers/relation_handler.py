from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox
from models import Relation, Expression, ObjectSet
from dialogs import RelationDialog


class RelationHandler:
    def __init__(self, window):
        self.window = window

    def add_relation(self):
        current_item = self.window.object_tree.currentItem()
        if not current_item:
            return

        expr_item = current_item
        expr = None
        while expr_item:
            expr_data = expr_item.data(0, 1)
            if isinstance(expr_data, Expression):
                expr = expr_data
                break
            expr_item = expr_item.parent()

        if not expr:
            return

        object_names = [obj_set.name for obj_set in expr.sets]

        dialog = RelationDialog(self.window, object_names)
        if dialog.exec():
            subject_name, relation, object_name = dialog.get_values()

            if subject_name == object_name:
                QMessageBox.warning(self.window, "Ошибка", "Субъект и объект не могут совпадать")
                return

            subject = next((s for s in expr.sets if s.name == subject_name), None)
            obj = next((s for s in expr.sets if s.name == object_name), None)

            if subject and obj:
                relation_obj = Relation(subject, relation, obj)

                subject.relations.append(relation_obj)
                obj.relations.append(relation_obj)

                self.update_relation_in_tree(subject, relation_obj)
                self.update_relation_in_tree(obj, relation_obj)

    def update_relation_in_tree(self, obj, relation):
        relation_item = QTreeWidgetItem([f"Отношение: {relation.relation} {relation.subject.name} → {relation.obj.name}"])
        relation_item.setData(0, 1, relation)

        root = self.window.object_tree.invisibleRootItem()
        stack = [root.child(i) for i in range(root.childCount())]

        while stack:
            item = stack.pop()
            data = item.data(0, 1)
            if isinstance(data, ObjectSet) and data.name == obj.name:
                relations_container = None
                for i in range(item.childCount()):
                    if item.child(i).text(0) == "Отношения":
                        relations_container = item.child(i)
                        break
                if not relations_container:
                    relations_container = QTreeWidgetItem(["Отношения"])
                    relations_container.setData(0, 1, {"type": "relations"})
                    item.addChild(relations_container)
                relations_container.addChild(relation_item)
                relations_container.setExpanded(True)
                item.setExpanded(True)
                break
            for i in range(item.childCount()):
                stack.append(item.child(i))