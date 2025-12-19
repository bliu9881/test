# HIPAA Compliance Test Files

⚠️ **WARNING**: These files contain intentional HIPAA violations for testing purposes only. DO NOT use in production!

## Purpose

These files are designed to test the HIPAA Compliance Checker's ability to detect various types of HIPAA violations in healthcare applications.

## Files

### 1. patient_api.py
A Flask-based REST API with 27 intentional HIPAA violations including:
- Logging PHI in plain text
- Hardcoded credentials
- No encryption for PHI storage
- Missing authentication/authorization
- No audit logging
- SQL injection vulnerabilities
- Exposing SSNs and other sensitive data
- No data validation
- Insecure data deletion
- Unencrypted data export
- Missing BAA verification
- Debug mode in production

### 2. infrastructure.ts
An AWS CDK infrastructure stack with 59 intentional HIPAA violations including:
- No encryption at rest (RDS, S3, EBS, CloudWatch)
- Public accessibility of databases
- Overly permissive security groups (0.0.0.0/0)
- Resources in public subnets
- No VPC segmentation
- Missing backup retention
- No deletion protection
- Hardcoded credentials
- No API authentication
- Missing audit logging (CloudTrail)
- No compliance monitoring (Config)
- Infinite log retention
- Exposing sensitive information in outputs
- No MFA requirements
- Missing encryption in transit enforcement

## Expected Detections

The HIPAA Compliance Checker should detect violations related to:

### Technical Safeguards (§164.312)
- Access Control (§164.312(a))
- Audit Controls (§164.312(b))
- Integrity (§164.312(c))
- Transmission Security (§164.312(e))

### Physical Safeguards (§164.310)
- Facility Access Controls (§164.310(a))
- Workstation Security (§164.310(c))
- Device and Media Controls (§164.310(d))

### Administrative Safeguards (§164.308)
- Security Management Process (§164.308(a)(1))
- Assigned Security Responsibility (§164.308(a)(2))
- Workforce Security (§164.308(a)(3))
- Information Access Management (§164.308(a)(4))

## Testing Instructions

1. Upload these files to a GitHub repository
2. Submit the repository URL to the HIPAA Compliance Checker
3. Review the generated compliance report
4. Verify that the checker identifies the violations listed above

## Violation Categories

- **Encryption**: Missing encryption at rest and in transit
- **Access Control**: No authentication, authorization, or role-based access
- **Audit Logging**: Missing or insufficient audit trails
- **Data Protection**: Exposing PHI, SSNs, and other sensitive data
- **Network Security**: Public accessibility, overly permissive security groups
- **Credential Management**: Hardcoded passwords and API keys
- **Data Retention**: Missing or improper retention policies
- **Backup & Recovery**: No backup retention or disaster recovery
- **Monitoring**: Missing CloudTrail, Config, GuardDuty
- **Input Validation**: SQL injection and other injection vulnerabilities

## Compliance Standards Violated

These files violate multiple HIPAA requirements:
- 45 CFR § 164.308 - Administrative Safeguards
- 45 CFR § 164.310 - Physical Safeguards
- 45 CFR § 164.312 - Technical Safeguards
- 45 CFR § 164.314 - Organizational Requirements
- 45 CFR § 164.316 - Policies and Procedures

## Disclaimer

These files are for testing purposes only. They demonstrate common security and compliance mistakes that should be avoided in real healthcare applications. Always follow HIPAA guidelines and security best practices when handling Protected Health Information (PHI).
