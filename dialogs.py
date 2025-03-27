from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox, QCompleter
from PySide6.QtCore import Qt


class ExpressionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выражение")
        layout = QFormLayout()

        self.expr_text = QLineEdit()
        layout.addRow("Текст выражения:", self.expr_text)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)


class SetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Множество")
        layout = QFormLayout()

        self.set_name = QLineEdit()
        layout.addRow("Название множества:", self.set_name)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)


class PropertyDialog(QDialog):
    def __init__(self, parent=None, prop=None):
        super().__init__(parent)
        self.setWindowTitle("Свойство")
        layout = QFormLayout()

        self.code = QLineEdit()
        self.name = QLineEdit()
        self.unit = QLineEdit()
        self.logic_relation = QComboBox()
        self.logic_relation.addItems(["==", ">=", "<=", ">", "<"])
        self.value = QLineEdit()

        layout.addRow("Name:", self.name)
        layout.addRow("Code:", self.code)
        layout.addRow("Unit:", self.unit)
        layout.addRow("LogicRelation:", self.logic_relation)
        layout.addRow("Value:", self.value)

        if prop:
            self.code.setText(prop.code)
            self.name.setText(prop.name)
            self.unit.setText(prop.unit)
            self.logic_relation.setCurrentText(prop.logic_relation)
            self.value.setText(prop.value)

        add_button = QPushButton("ОК")
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)

        self.setLayout(layout)


class ObjectDialog(QDialog):
    def __init__(self, parent=None, obj=None, searcher=None):
        super().__init__(parent)
        self.setWindowTitle("Объект")
        self.resize(400, self.height())

        layout = QFormLayout()
        
        self.searcher = searcher
        self.obj_name = QLineEdit()
        self.obj_name.textChanged.connect(self.update_suggestions)
        self.obj_name.textChanged.connect(self.update_ksi)

        self.obj_code = QLineEdit()
        self.obj_code.width = 200
        self.obj_code.setReadOnly(True)
        self.obj_ksi = QLineEdit()
        layout.addRow("Name:", self.obj_name)
        layout.addRow("Code:", self.obj_code)
        layout.addRow("KSI:", self.obj_ksi)

        if obj:
            self.obj_name.setText(obj.name)
            self.obj_code.setText(obj.code)
            self.obj_ksi.setText(obj.ksi)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)
    
    def update_suggestions(self, text):
        if not self.searcher or len(text) < 2:
            return
        results = self.searcher.search_nearest(text, top_k=10)
        suggestions = [res["Наименование"] for res in results]

        completer = QCompleter(suggestions)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        self.obj_name.setCompleter(completer)

    def update_ksi(self, text):
        if not self.searcher or len(text) < 2:
            return
        self.obj_ksi.setText(self.searcher.df[self.searcher.df["Наименование"] == text]["Подкласс 2"].values[0])


class RelationDialog(QDialog):
    def __init__(self, parent=None, object_names=None, current_subject=None, current_object=None, current_relation=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить отношение")
        layout = QFormLayout()

        self.subject_combo = QComboBox()
        self.subject_combo.addItems(object_names or [])
        if current_subject:
            self.subject_combo.setCurrentText(current_subject)

        self.relation_combo = QComboBox()
        self.relation_combo.addItems(["partOf", "serves", "distanceFrom", "insideOf", "aboveOf", "belowOf"])
        if current_relation:
            self.relation_combo.setCurrentText(current_relation)

        self.object_combo = QComboBox()
        self.object_combo.addItems(object_names or [])
        if current_object:
            self.object_combo.setCurrentText(current_object)

        layout.addRow("Субъект:", self.subject_combo)
        layout.addRow("Отношение:", self.relation_combo)
        layout.addRow("Объект:", self.object_combo)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_values(self):
        return (
            self.subject_combo.currentText(),
            self.relation_combo.currentText(),
            self.object_combo.currentText()
        )
