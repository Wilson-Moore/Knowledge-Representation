from Knowledge.Hierarchy import Patient

def has_mri_abnormality(patient: Patient,mri_name: str):
    return any(mri.name==mri_name and mri.present for mri in patient.MRIs)

def has_symptom(patient: Patient,symptom_name: str):
    return any(symptom.name==symptom_name for symptom in patient.symptoms)

def test_above(patient: Patient,test_name: str,threshold: float):
    return any(test.name==test_name and test.value>threshold for test in patient.lab_tests)