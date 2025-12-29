"""
Patient API - Healthcare Application
WARNING: This file contains intentional HIPAA violations for testing purposes
"""

import logging
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# VIOLATION 1: Logging PHI without encryption
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='patient_records.log'  # Logs contain PHI
)

# VIOLATION 2: Hardcoded database credentials
DB_HOST = "prod-db.hospital.com"
DB_USER = "admin"
DB_PASSWORD = "Hospital123!"  # Hardcoded password
DB_NAME = "patient_records"

# VIOLATION 3: No encryption for PHI storage
patient_cache = {}  # In-memory cache without encryption


@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients - VIOLATION: No access controls"""
    # VIOLATION 4: No authentication or authorization
    # VIOLATION 5: No audit logging of PHI access
    
    patients = [
        {
            "id": 1,
            "name": "John Doe",
            "ssn": "123-45-6789",  # VIOLATION 6: Exposing SSN
            "dob": "1980-05-15",
            "diagnosis": "Type 2 Diabetes",
            "medications": ["Metformin", "Insulin"],
            "insurance": "Blue Cross 987654321"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "ssn": "987-65-4321",
            "dob": "1975-08-22",
            "diagnosis": "Hypertension",
            "medications": ["Lisinopril"],
            "insurance": "Aetna 123456789"
        }
    ]
    
    # VIOLATION 7: Logging PHI in plain text
    logging.info(f"Retrieved {len(patients)} patient records")
    logging.info(f"Patient data: {json.dumps(patients)}")
    logging.info("Exported all patient records to /tmp/patient_export.json")
    
    return jsonify(patients)


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID - VIOLATION: No minimum necessary principle"""
    # VIOLATION 8: Returning all PHI regardless of need
    
    # VIOLATION 9: SQL injection vulnerability
    query = f"SELECT * FROM patients WHERE id = {patient_id}"
    
    patient = {
        "id": patient_id,
        "name": "John Doe",
        "ssn": "123-45-6789",
        "dob": "1980-05-15",
        "address": "123 Main St, Anytown, USA",
        "phone": "555-1234",
        "email": "john.doe@email.com",
        "diagnosis": "Type 2 Diabetes",
        "medications": ["Metformin", "Insulin"],
        "lab_results": {
            "hba1c": 7.2,
            "glucose": 145
        },
        "insurance": "Blue Cross 987654321",
        "emergency_contact": {
            "name": "Jane Doe",
            "phone": "555-5678"
        }
    }
    
    # VIOLATION 10: No encryption in transit verification
    return jsonify(patient)


@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Create new patient - VIOLATION: No input validation"""
    data = request.get_json()
    
    # VIOLATION 11: No data validation or sanitization
    # VIOLATION 12: Storing PHI without encryption
    patient_cache[data['id']] = data
    
    # VIOLATION 13: Logging PHI during creation
    logging.info(f"Created patient: {data['name']}, SSN: {data['ssn']}")
    
    return jsonify({"status": "created", "patient": data}), 201


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient - VIOLATION: No version control or audit trail"""
    data = request.get_json()
    
    # VIOLATION 14: No audit trail for PHI modifications
    # VIOLATION 15: No data retention policy enforcement
    patient_cache[patient_id] = data
    
    logging.info(f"Updated patient {patient_id}")
    
    return jsonify({"status": "updated"})


@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete patient - VIOLATION: No secure deletion"""
    # VIOLATION 16: Simple deletion without secure erasure
    if patient_id in patient_cache:
        del patient_cache[patient_id]
    
    # VIOLATION 17: No verification of deletion authorization
    return jsonify({"status": "deleted"})


@app.route('/api/export', methods=['GET'])
def export_patients():
    """Export patient data - VIOLATION: No encryption for data export"""
    # VIOLATION 18: Exporting PHI without encryption
    # VIOLATION 19: No access controls on bulk export
    
    with open('/tmp/patient_export.json', 'w') as f:
        json.dump(patient_cache, f)
    
    logging.info("Exported all patient records to /tmp/patient_export.json")
    
    return jsonify({"status": "exported", "file": "/tmp/patient_export.json"})


@app.route('/api/search', methods=['GET'])
def search_patients():
    """Search patients - VIOLATION: No query parameter validation"""
    # VIOLATION 20: SQL injection via search parameter
    search_term = request.args.get('q', '')
    query = f"SELECT * FROM patients WHERE name LIKE '%{search_term}%'"
    
    # VIOLATION 21: Logging search queries that may contain PHI
    logging.info(f"Search query: {search_term}")
    
    return jsonify({"results": []})


@app.route('/api/share', methods=['POST'])
def share_patient_data():
    """Share patient data - VIOLATION: No BAA verification"""
    data = request.get_json()
    recipient_email = data.get('email')
    patient_id = data.get('patient_id')
    
    # VIOLATION 22: Sharing PHI without verifying BAA
    # VIOLATION 23: No encryption for email transmission
    # VIOLATION 24: No patient consent verification
    
    patient_data = patient_cache.get(patient_id, {})
    
    # Simulate sending email (VIOLATION: Unencrypted email)
    logging.info(f"Sharing patient {patient_id} data with {recipient_email}")
    logging.info(f"Shared data: {json.dumps(patient_data)}")
    
    return jsonify({"status": "shared"})


@app.errorhandler(Exception)
def handle_error(error):
    """Error handler - VIOLATION: Exposing sensitive info in errors"""
    # VIOLATION 25: Detailed error messages may leak PHI
    logging.error(f"Error occurred: {str(error)}")
    
    return jsonify({
        "error": str(error),
        "stack_trace": str(error.__traceback__)  # VIOLATION: Exposing stack traces
    }), 500


if __name__ == '__main__':
    # VIOLATION 26: Running in debug mode in production
    # VIOLATION 27: No HTTPS enforcement
    app.run(host='0.0.0.0', port=5000, debug=True)
