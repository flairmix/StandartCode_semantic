from PySide6.QtWidgets import QTreeWidgetItem
from models import Expression
from dialogs import ExpressionDialog


class ExpressionHandler:
    def __init__(self, window):
        self.window = window

    def add_expression(self):
        dialog = ExpressionDialog(self.window)
        if dialog.exec():
            expr_text = dialog.expr_text.text()
            if expr_text:
                expr = Expression(expr_text)
                self.window.expressions.append(expr)
                expr_item = QTreeWidgetItem([f"Выражение: {expr_text}"])
                expr_item.setData(0, 1, expr)
                self.window.object_tree.addTopLevelItem(expr_item)
