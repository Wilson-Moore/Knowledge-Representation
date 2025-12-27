from PyQt5.QtCore import Qt

class Funcs:
    def __init__(self, patient_data):
        self.patient_data = patient_data

    def update_selected_symptoms(self, symptoms_dropdown, symptoms_model, method_dropdown, next_btn):
        selected = []
        for i in range(symptoms_model.rowCount()):
            item = symptoms_model.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())

        self.patient_data["symptoms"] = selected

        if selected:
            symptoms_dropdown.setEditText(", ".join(selected))
        else:
            symptoms_dropdown.setEditText("Select symptoms")

        self.validate_form(symptoms_model, method_dropdown, next_btn)

    def get_selected_symptoms(self, symptoms_model):
        selected = []
        for i in range(symptoms_model.rowCount()):
            item = symptoms_model.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        return selected

    def validate_form(self, symptoms_model, method_dropdown, next_btn):
        has_symptoms = len(self.get_selected_symptoms(symptoms_model)) > 0
        method_selected = method_dropdown.currentText() != "Select method"

        next_btn.setEnabled(has_symptoms and method_selected)

    def toggle_item(self, index, symptoms_model):
        item = symptoms_model.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
