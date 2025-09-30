# KYC/AML Compliance Guide

This document outlines the Know Your Customer (KYC) and Anti-Money Laundering (AML) compliance requirements and implementation guidelines for the CRS cryptocurrency marketplace.

## Table of Contents

1. [Overview](#overview)
2. [Regulatory Requirements](#regulatory-requirements)
3. [KYC Implementation](#kyc-implementation)
4. [AML Implementation](#aml-implementation)
5. [Transaction Monitoring](#transaction-monitoring)
6. [Reporting](#reporting)
7. [Data Retention](#data-retention)

---

## Overview

### Why KYC/AML is Required

Cryptocurrency exchanges must comply with KYC/AML regulations to:

1. **Prevent Money Laundering**: Detect and prevent illicit financial activities
2. **Combat Terrorist Financing**: Identify and report suspicious transactions
3. **Meet Regulatory Requirements**: Comply with local and international laws
4. **Protect Users**: Verify identities to prevent fraud and theft
5. **Maintain Banking Relationships**: Required by financial institutions

### Applicable Regulations

- **FinCEN (USA)**: Financial Crimes Enforcement Network
- **FATF**: Financial Action Task Force recommendations
- **5AMLD/6AMLD (EU)**: Anti-Money Laundering Directives
- **BSA**: Bank Secrecy Act
- **Local Regulations**: Country-specific requirements

---

## Regulatory Requirements

### Customer Identification Program (CIP)

**Required Information:**

1. **Personal Information**
   - Full legal name
   - Date of birth
   - Residential address
   - Nationality
   - Phone number
   - Email address

2. **Identity Verification**
   - Government-issued ID (passport, driver's license, national ID)
   - Proof of address (utility bill, bank statement)
   - Selfie with ID (liveness check)

3. **Business Information (for corporate accounts)**
   - Business name and registration number
   - Business address
   - Business type and activities
   - Beneficial ownership information
   - Source of funds

### Risk-Based Approach

**User Risk Tiers:**

1. **Low Risk** (Standard KYC)
   - Transaction limits: $1,000/day, $10,000/month
   - Basic identity verification
   - Proof of address

2. **Medium Risk** (Enhanced KYC)
   - Transaction limits: $10,000/day, $100,000/month
   - Enhanced identity verification
   - Source of funds declaration
   - Additional documentation

3. **High Risk** (Enhanced Due Diligence)
   - Transaction limits: Custom
   - Full Enhanced Due Diligence (EDD)
   - Source of wealth verification
   - Ongoing monitoring
   - Senior management approval

**High-Risk Indicators:**
- Politically Exposed Persons (PEPs)
- High-risk jurisdictions
- Cash-intensive businesses
- Unusual transaction patterns
- Large transaction amounts

---

## KYC Implementation

### Database Models

```python
from datetime import datetime
from src.models import db

class KYCVerification(db.Model):
    """KYC verification records"""
    __tablename__ = 'kyc_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Personal information
    full_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String(3), nullable=False)  # ISO 3166-1 alpha-3
    address_line1 = db.Column(db.String(200))
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(3), nullable=False)
    
    # Verification documents
    id_type = db.Column(db.String(50))  # passport, drivers_license, national_id
    id_number = db.Column(db.String(100))
    id_document_url = db.Column(db.String(500))
    proof_of_address_url = db.Column(db.String(500))
    selfie_url = db.Column(db.String(500))
    
    # Verification status
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, expired
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high
    verification_method = db.Column(db.String(50))  # manual, automated, hybrid
    
    # Verification results
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # KYC re-verification required
```

### Verification Workflow

#### 1. Initial Submission

```python
@app.route('/api/kyc/submit', methods=['POST'])
@jwt_required()
def submit_kyc():
    user_id = get_jwt_identity()
    data = request.json
    
    # Validate required fields
    required_fields = ['full_name', 'date_of_birth', 'nationality', 'address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check age requirement (18+)
    age = calculate_age(data['date_of_birth'])
    if age < 18:
        return jsonify({'error': 'Must be 18 or older'}), 400
    
    # Create KYC record
    kyc = KYCVerification(
        user_id=user_id,
        full_name=data['full_name'],
        date_of_birth=data['date_of_birth'],
        nationality=data['nationality'],
        # ... other fields
        status='pending'
    )
    db.session.add(kyc)
    db.session.commit()
    
    # Trigger verification process
    initiate_verification(kyc.id)
    
    return jsonify({
        'message': 'KYC submitted successfully',
        'kyc_id': kyc.id,
        'status': 'pending'
    }), 201
```

#### 2. Document Upload

```python
@app.route('/api/kyc/<int:kyc_id>/upload', methods=['POST'])
@jwt_required()
def upload_kyc_document(kyc_id):
    user_id = get_jwt_identity()
    
    # Verify ownership
    kyc = KYCVerification.query.filter_by(
        id=kyc_id,
        user_id=user_id
    ).first_or_404()
    
    # Handle file upload
    if 'document' not in request.files:
        return jsonify({'error': 'No document provided'}), 400
    
    file = request.files['document']
    document_type = request.form.get('type')  # id_document, proof_of_address, selfie
    
    # Validate file
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Upload to secure storage (S3, etc.)
    file_url = upload_to_storage(file, user_id, document_type)
    
    # Update KYC record
    if document_type == 'id_document':
        kyc.id_document_url = file_url
    elif document_type == 'proof_of_address':
        kyc.proof_of_address_url = file_url
    elif document_type == 'selfie':
        kyc.selfie_url = file_url
    
    db.session.commit()
    
    return jsonify({
        'message': 'Document uploaded successfully',
        'document_type': document_type
    }), 200
```

#### 3. Automated Verification

```python
def initiate_verification(kyc_id):
    """Start automated KYC verification process"""
    kyc = KYCVerification.query.get(kyc_id)
    
    # 1. Document verification (OCR, authenticity check)
    document_result = verify_document(kyc.id_document_url)
    
    # 2. Face matching (selfie vs ID photo)
    face_match_result = verify_face_match(
        kyc.selfie_url,
        kyc.id_document_url
    )
    
    # 3. Liveness detection
    liveness_result = verify_liveness(kyc.selfie_url)
    
    # 4. Sanctions screening
    sanctions_result = screen_sanctions(
        kyc.full_name,
        kyc.date_of_birth,
        kyc.nationality
    )
    
    # 5. PEP screening
    pep_result = screen_pep(kyc.full_name, kyc.country)
    
    # Determine verification status
    if all([
        document_result['valid'],
        face_match_result['match'],
        liveness_result['is_live'],
        not sanctions_result['is_sanctioned'],
    ]):
        # Auto-approve if all checks pass
        kyc.status = 'approved'
        kyc.verified_at = datetime.utcnow()
        kyc.risk_level = 'low' if not pep_result['is_pep'] else 'high'
        kyc.expires_at = datetime.utcnow() + timedelta(days=365)
    else:
        # Flag for manual review
        kyc.status = 'pending_review'
        kyc.notes = generate_review_notes(
            document_result,
            face_match_result,
            liveness_result,
            sanctions_result,
            pep_result
        )
    
    db.session.commit()
    
    # Notify user
    send_kyc_status_notification(kyc.user_id, kyc.status)
```

#### 4. Manual Review

```python
@app.route('/api/admin/kyc/<int:kyc_id>/review', methods=['POST'])
@jwt_required()
@admin_required()
def review_kyc(kyc_id):
    admin_id = get_jwt_identity()
    data = request.json
    
    kyc = KYCVerification.query.get_or_404(kyc_id)
    
    # Update verification status
    kyc.status = data['status']  # approved, rejected
    kyc.verified_by = admin_id
    kyc.verified_at = datetime.utcnow()
    
    if data['status'] == 'approved':
        kyc.risk_level = data.get('risk_level', 'low')
        kyc.expires_at = datetime.utcnow() + timedelta(days=365)
    elif data['status'] == 'rejected':
        kyc.rejection_reason = data.get('reason')
    
    kyc.notes = data.get('notes')
    db.session.commit()
    
    # Notify user
    send_kyc_status_notification(kyc.user_id, kyc.status)
    
    return jsonify({
        'message': 'KYC review completed',
        'status': kyc.status
    }), 200
```

---

## AML Implementation

### Transaction Monitoring

```python
class TransactionMonitor:
    """AML transaction monitoring system"""
    
    # Thresholds for alerts
    DAILY_THRESHOLD = 10000  # $10,000
    WEEKLY_THRESHOLD = 50000  # $50,000
    MONTHLY_THRESHOLD = 100000  # $100,000
    
    # Suspicious patterns
    RAPID_TRANSACTIONS = 10  # transactions within 1 hour
    ROUND_AMOUNT_THRESHOLD = 0.95  # 95% transactions are round amounts
    
    @staticmethod
    def check_transaction(user_id, amount, currency):
        """Check transaction for AML compliance"""
        alerts = []
        
        # 1. Check against thresholds
        daily_total = get_daily_transaction_total(user_id)
        if daily_total + amount > TransactionMonitor.DAILY_THRESHOLD:
            alerts.append({
                'type': 'daily_threshold_exceeded',
                'threshold': TransactionMonitor.DAILY_THRESHOLD,
                'total': daily_total + amount
            })
        
        # 2. Check for rapid transactions
        recent_count = count_recent_transactions(user_id, hours=1)
        if recent_count >= TransactionMonitor.RAPID_TRANSACTIONS:
            alerts.append({
                'type': 'rapid_transactions',
                'count': recent_count,
                'timeframe': '1 hour'
            })
        
        # 3. Check for structuring (smurfing)
        if is_structuring_pattern(user_id):
            alerts.append({
                'type': 'potential_structuring',
                'description': 'Multiple transactions just below reporting threshold'
            })
        
        # 4. Check for round amount pattern
        if has_round_amount_pattern(user_id):
            alerts.append({
                'type': 'round_amount_pattern',
                'description': 'Unusual number of round amount transactions'
            })
        
        # 5. Geographic risk check
        if is_high_risk_location(user_id):
            alerts.append({
                'type': 'high_risk_location',
                'description': 'Transaction from high-risk jurisdiction'
            })
        
        # Create alert if needed
        if alerts:
            create_aml_alert(user_id, amount, currency, alerts)
        
        return len(alerts) == 0, alerts
```

### Suspicious Activity Reports (SAR)

```python
class SuspiciousActivity(db.Model):
    """Suspicious activity tracking"""
    __tablename__ = 'suspicious_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Activity details
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10))
    
    # Investigation
    status = db.Column(db.String(20), default='pending')  # pending, investigating, resolved, reported
    investigated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    investigation_notes = db.Column(db.Text)
    
    # Reporting
    reported_to = db.Column(db.String(100))  # FinCEN, local authority
    reported_at = db.Column(db.DateTime)
    report_reference = db.Column(db.String(100))
    
    # Timestamps
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
```

### Enhanced Due Diligence (EDD)

For high-risk customers:

```python
def perform_edd(user_id):
    """Perform Enhanced Due Diligence"""
    user = User.query.get(user_id)
    kyc = KYCVerification.query.filter_by(user_id=user_id).first()
    
    edd_checks = {
        'source_of_funds': verify_source_of_funds(user_id),
        'source_of_wealth': verify_source_of_wealth(user_id),
        'business_activities': verify_business_activities(user_id),
        'expected_transaction_volume': assess_transaction_volume(user_id),
        'adverse_media': screen_adverse_media(kyc.full_name),
        'ongoing_monitoring': enable_ongoing_monitoring(user_id)
    }
    
    # Require senior management approval
    approval_required = any([
        kyc.risk_level == 'high',
        edd_checks['adverse_media']['has_concerns'],
        kyc.country in HIGH_RISK_COUNTRIES
    ])
    
    return {
        'edd_required': True,
        'checks': edd_checks,
        'approval_required': approval_required
    }
```

---

## Transaction Monitoring

### Real-Time Monitoring

```python
@app.before_request
def monitor_transaction():
    """Monitor all transactions in real-time"""
    if request.endpoint and 'transaction' in request.endpoint:
        user_id = get_jwt_identity()
        data = request.json
        
        # Check AML compliance
        is_compliant, alerts = TransactionMonitor.check_transaction(
            user_id,
            data.get('amount'),
            data.get('currency')
        )
        
        if not is_compliant:
            # Log alerts
            for alert in alerts:
                log_aml_alert(user_id, alert)
            
            # Block if critical
            if any(alert['type'] in CRITICAL_ALERTS for alert in alerts):
                return jsonify({
                    'error': 'Transaction blocked for review',
                    'reason': 'AML compliance review required'
                }), 403
```

### Daily Reports

```python
def generate_daily_aml_report():
    """Generate daily AML monitoring report"""
    today = datetime.utcnow().date()
    
    report = {
        'date': today,
        'high_value_transactions': get_high_value_transactions(today),
        'new_alerts': get_new_aml_alerts(today),
        'pending_investigations': get_pending_investigations(),
        'suspicious_patterns': detect_suspicious_patterns(today),
        'blocked_transactions': get_blocked_transactions(today),
        'stats': {
            'total_transactions': count_transactions(today),
            'total_volume': sum_transaction_volume(today),
            'alert_rate': calculate_alert_rate(today)
        }
    }
    
    # Send to compliance team
    send_compliance_report(report)
    
    return report
```

---

## Reporting

### Currency Transaction Reports (CTR)

Required for transactions over $10,000:

```python
def file_ctr(transaction):
    """File Currency Transaction Report"""
    if transaction.amount > 10000:
        ctr = {
            'transaction_id': transaction.id,
            'user_id': transaction.user_id,
            'amount': transaction.amount,
            'currency': transaction.currency,
            'date': transaction.created_at,
            'type': 'CTR',
            'filing_deadline': datetime.utcnow() + timedelta(days=15)
        }
        
        # Submit to FinCEN
        submit_to_fincen(ctr)
```

### Suspicious Activity Reports (SAR)

```python
def file_sar(suspicious_activity):
    """File Suspicious Activity Report"""
    sar = {
        'activity_id': suspicious_activity.id,
        'user_id': suspicious_activity.user_id,
        'description': suspicious_activity.description,
        'amount': suspicious_activity.amount,
        'date': suspicious_activity.detected_at,
        'type': 'SAR',
        'filing_deadline': datetime.utcnow() + timedelta(days=30)
    }
    
    # Submit to FinCEN
    submit_to_fincen(sar)
    
    # Update status
    suspicious_activity.status = 'reported'
    suspicious_activity.reported_at = datetime.utcnow()
    db.session.commit()
```

---

## Data Retention

### Retention Requirements

**Minimum retention periods:**

- **KYC Documents**: 5 years after account closure
- **Transaction Records**: 5 years
- **SAR Records**: 5 years
- **CTR Records**: 5 years
- **AML Alerts**: 5 years

### Implementation

```python
def archive_old_records():
    """Archive records older than retention period"""
    retention_date = datetime.utcnow() - timedelta(days=5*365)
    
    # Archive but don't delete (for legal holds)
    old_records = Transaction.query.filter(
        Transaction.created_at < retention_date
    ).all()
    
    for record in old_records:
        archive_to_cold_storage(record)
        mark_as_archived(record)
```

---

## Best Practices

1. **Risk-Based Approach**: Apply appropriate KYC level based on risk
2. **Continuous Monitoring**: Monitor transactions in real-time
3. **Regular Updates**: Re-verify KYC annually
4. **Staff Training**: Train compliance team regularly
5. **Documentation**: Document all decisions and actions
6. **Technology**: Use automated tools for efficiency
7. **Cooperation**: Work with regulators and law enforcement
8. **Privacy**: Balance compliance with user privacy

---

## Resources

- [FinCEN Guidance](https://www.fincen.gov/)
- [FATF Recommendations](https://www.fatf-gafi.org/)
- [BSA/AML Manual](https://www.ffiec.gov/bsa_aml_infobase/)
