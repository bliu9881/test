"""
Healthcare Application with HIPAA Violations
This file contains intentional HIPAA compliance issues for testing
"""

import logging
import requests

# VIOLATION 1: Logging PHI without encryption
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatientRecord:
    """Patient medical record - contains PHI"""
    
    def __init__(self, patient_id, name, ssn, diagnosis, medications):
        self.patient_id = patient_id
        self.name = name
        self.ssn = ssn  # VIOLATION 2: Storing SSN without encryption
        self.diagnosis = diagnosis
        self.medications = medications
    
    def save_to_file(self, filename):
        """VIOLATION 3: Writing PHI to unencrypted file"""
        with open(filename, 'w') as f:
            f.write(f"Patient: {self.name}\n")
            f.write(f"SSN: {self.ssn}\n")
            f.write(f"Diagnosis: {self.diagnosis}\n")
            f.write(f"Medications: {self.medications}\n")
        
        # VIOLATION 4: Logging PHI in plain text
        logger.info(f"Saved patient record for {self.name} (SSN: {self.ssn})")


def send_patient_data_via_http(patient):
    """VIOLATION 5: Transmitting PHI over unencrypted HTTP"""
    url = "http://example.com/api/patients"  # Not HTTPS!
    
    data = {
        'name': patient.name,
        'ssn': patient.ssn,
        'diagnosis': patient.diagnosis
    }
    
    # VIOLATION 6: No authentication or authorization
    response = requests.post(url, json=data)
    
    # VIOLATION 7: Logging full response including PHI
    logger.info(f"API Response: {response.text}")
    
    return response


def search_patients(search_term):
    """VIOLATION 8: SQL injection vulnerability with PHI"""
    import sqlite3
    
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    
    # VIOLATION 9: SQL injection - no parameterized queries
    query = f"SELECT * FROM patients WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    # VIOLATION 10: Returning PHI without access control
    return results


def backup_patient_data():
    """VIOLATION 11: Backing up to unencrypted storage"""
    import shutil
    
    # VIOLATION 12: No encryption at rest
    shutil.copy('patients.db', '/tmp/backup/patients_backup.db')
    
    logger.info("Patient database backed up to /tmp/backup/")

class PatientAPI:
    """API for patient data access"""
    
    def get_patient(self, patient_id):
        """VIOLATION 13: No audit logging for PHI access"""
        # Fetch patient data without logging who accessed it
        patient = self._fetch_from_db(patient_id)
        return patient
    
    def update_patient(self, patient_id, data):
        """VIOLATION 14: No data validation or sanitization"""
        # Directly using user input without validation
        query = f"UPDATE patients SET data='{data}' WHERE id={patient_id}"
        # Execute without validation
        
    def share_patient_record(self, patient_id, recipient_email):
        """VIOLATION 15: Sharing PHI via unencrypted email"""
        import smtplib
        
        patient = self.get_patient(patient_id)
        
        # VIOLATION 16: Sending PHI in email body (unencrypted)
        message = f"""
        Patient Record:
        Name: {patient.name}
        SSN: {patient.ssn}
        Diagnosis: {patient.diagnosis}
        """
        
        # VIOLATION 17: No secure email transmission
        server = smtplib.SMTP('smtp.example.com', 25)  # Not using TLS
        server.sendmail('noreply@hospital.com', recipient_email, message)


# VIOLATION 18: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk_live_1234567890abcdef"


def authenticate_user(username, password):
    """VIOLATION 19: Weak password policy"""
    # No password complexity requirements
    # No multi-factor authentication
    if len(password) < 4:  # Very weak requirement
        return False
    return True


# VIOLATION 20: No data retention policy
def store_patient_record_forever(patient):
    """Stores patient data indefinitely without retention policy"""
    # No automatic deletion or archival
    pass


if __name__ == "__main__":
    # Example usage with violations
    patient = PatientRecord(
        patient_id="12345",
        name="John Doe",
        ssn="123-45-6789",
        diagnosis="Hypertension",
        medications=["Lisinopril", "Aspirin"]
    )
    
    # VIOLATION 21: Printing PHI to console
    print(f"Processing patient: {patient.name}, SSN: {patient.ssn}")
    
    patient.save_to_file("patient_data.txt")
    send_patient_data_via_http(patient)
    backup_patient_data()
