from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QTreeWidget, QTreeWidgetItem
)
from models import Property, ObjectEntity, Expression, ObjectSet
from dialogs import ExpressionDialog, ObjectDialog, PropertyDialog, SetDialog
from handlers import ExpressionHandler, ObjectTreeHandler


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop приложение")
        self.resize(500, 500)

        self.expressions = []
        self.object_map = {}

        self.expression_handler = ExpressionHandler(self)
        self.tree_handler = ObjectTreeHandler(self)

        self._init_ui()

    def _init_ui(self):
        self.main_layout = QVBoxLayout()

        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setFixedHeight(100)
        self.description_text.setPlainText("Добро пожаловать! Это простое приложение для работы с объектами и их свойствами.")
        self.main_layout.addWidget(QLabel("Описание интерфейса:"))
        self.main_layout.addWidget(self.description_text)

        self._init_buttons()
        self._init_tree()

        self.setLayout(self.main_layout)

    def _init_buttons(self):
        btn_layout = QHBoxLayout()

        self.add_expr_button = QPushButton("Добавить выражение")
        self.add_expr_button.clicked.connect(self.expression_handler.add_expression)
        btn_layout.addWidget(self.add_expr_button)

        self.add_set_button = QPushButton("Добавить множество")
        self.add_set_button.clicked.connect(self.tree_handler.add_set)
        self.add_set_button.setEnabled(False)
        btn_layout.addWidget(self.add_set_button)

        self.add_object_button = QPushButton("Добавить объект")
        self.add_object_button.clicked.connect(self.tree_handler.add_object)
        self.add_object_button.setEnabled(False)
        btn_layout.addWidget(self.add_object_button)

        self.add_prop_button = QPushButton("Добавить свойство")
        self.add_prop_button.clicked.connect(self.tree_handler.add_property)
        self.add_prop_button.setEnabled(False)
        btn_layout.addWidget(self.add_prop_button)

        self.edit_button = QPushButton("Редактировать выбранное")
        self.edit_button.clicked.connect(self.tree_handler.edit_selected)
        self.edit_button.setEnabled(False)
        btn_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить выбранное")
        self.delete_button.clicked.connect(self.tree_handler.delete_selected)
        self.delete_button.setEnabled(False)
        btn_layout.addWidget(self.delete_button)

        self.add_relation_button = QPushButton("Добавить отношение")
        self.add_relation_button.setEnabled(False)
        btn_layout.addWidget(self.add_relation_button)

        self.main_layout.addLayout(btn_layout)

    def _init_tree(self):
        self.object_tree = QTreeWidget()
        self.object_tree.setHeaderLabels(["Структура: выражения, множества, объекты и свойства"])
        self.object_tree.currentItemChanged.connect(self.tree_handler.on_object_selected)
        self.main_layout.addWidget(QLabel("Список объектов:"))
        self.main_layout.addWidget(self.object_tree)
