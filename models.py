class Property:
    def __init__(self, code, name, unit, logic_relation, value):
        self.code = code
        self.name = name
        self.unit = unit
        self.logic_relation = logic_relation
        self.value = value

    def __str__(self):
        return f"Code: {self.code}, Name: {self.name}, Unit: {self.unit}, Logic: {self.logic_relation}, Value: {self.value}"


class ObjectEntity:
    def __init__(self, name, code, ksi):
        self.name = name
        self.code = code
        self.ksi = ksi

    def __str__(self):
        return f"{self.name} (ID: {self.code}) | KSI: {self.ksi}"


class ObjectSet:
    def __init__(self, name):
        self.name = name
        self.objects = []
        self.properties = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_property(self, prop):
        self.properties.append(prop)

    def remove_property_by_str(self, prop_str):
        self.properties = [p for p in self.properties if str(p) != prop_str]


class Expression:
    def __init__(self, text):
        self.text = text
        self.sets = []

    def add_set(self, obj_set):
        self.sets.append(obj_set)
