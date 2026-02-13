# Database Migration Guide

Guide for migrating the database to support CFV (Crypto Fair Value) integration.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Migration Steps](#migration-steps)
- [Rollback Procedures](#rollback-procedures)
- [Data Validation](#data-validation)
- [Troubleshooting](#troubleshooting)

## Overview

This migration adds two new tables to support CFV-based cryptocurrency payments and e-commerce orders:

1. **ecommerce_orders** - E-commerce orders with CFV discount support
2. **payments** - Cryptocurrency payments with CFV metrics

### New Tables

#### ecommerce_orders

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| order_id | String(64) | Unique order identifier |
| user_id | Integer | Foreign key to users table |
| items | JSON | Array of order items |
| subtotal | Float | Subtotal before shipping |
| original_price_usd | Float | Price before CFV discount |
| cfv_discount | Float | Discount percentage (0-100) |
| cfv_metrics | JSON | CFV calculation metrics |
| total | Float | Final total after discount |
| status | String(20) | Order status |
| shipping_address | JSON | Shipping address information |
| shipping_method | String(50) | Shipping method |
| shipping_cost | Float | Shipping cost |
| tracking_number | String(100) | Package tracking number |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |
| paid_at | DateTime | Payment timestamp |
| shipped_at | DateTime | Shipping timestamp |
| completed_at | DateTime | Completion timestamp |

#### payments

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| payment_id | String(64) | Unique payment identifier |
| order_id | Integer | Foreign key to ecommerce_orders |
| user_id | Integer | Foreign key to users table |
| cryptocurrency | String(20) | Cryptocurrency symbol |
| amount_crypto | Float | Amount in cryptocurrency |
| amount_usd | Float | USD equivalent |
| fair_value | Float | CFV calculated fair value |
| cfv_discount | Float | Discount percentage applied |
| cfv_metrics | JSON | CFV metrics (status, percent, etc.) |
| payment_address | String(255) | Cryptocurrency payment address |
| transaction_hash | String(255) | Blockchain transaction hash |
| confirmations | Integer | Number of confirmations |
| network_fee | Float | Network transaction fee |
| total_amount | Float | Total including fees |
| status | String(20) | Payment status |
| created_at | DateTime | Creation timestamp |
| expires_at | DateTime | Payment expiration |
| confirmed_at | DateTime | Confirmation timestamp |
| completed_at | DateTime | Completion timestamp |
| metadata | JSON | Additional metadata |

## Prerequisites

Before running the migration:

1. **Backup your database:**
   ```bash
   # PostgreSQL
   pg_dump -U username -d cryptons_db > backup_$(date +%Y%m%d_%H%M%S).sql
   
   # SQLite
   sqlite3 cryptons.db ".backup backup_$(date +%Y%m%d_%H%M%S).db"
   ```

2. **Ensure application is stopped:**
   ```bash
   # Stop the Flask application
   pkill -f "python main.py"
   ```

3. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   - Ensure `DATABASE_URL` is set in `.env`
   - Verify database connection

## Migration Steps

### Step 1: Verify Current Database State

Check existing tables:

```bash
# PostgreSQL
psql -U username -d cryptons_db -c "\dt"

# SQLite
sqlite3 cryptons.db ".tables"
```

### Step 2: Run Migration

Execute the migration script:

```bash
cd backend
python migrations/add_cfv_models.py upgrade
```

**Expected Output:**
```
Creating tables for CFV integration...
✓ Successfully created Payment and EcommerceOrder tables

New tables:
  - ecommerce_orders: E-commerce orders with CFV discount support
  - payments: Cryptocurrency payments with CFV metrics
```

### Step 3: Validate Migration

Validate that the migration was successful:

```bash
python migrations/add_cfv_models.py validate
```

**Expected Output:**
```
Validating migration...
✓ All required tables exist
✓ Payment table has all required columns
✓ EcommerceOrder table has all required columns

✓ Migration validation successful!
```

### Step 4: Verify Database Schema

Check the new tables:

```bash
# PostgreSQL
psql -U username -d cryptons_db -c "\d ecommerce_orders"
psql -U username -d cryptons_db -c "\d payments"

# SQLite
sqlite3 cryptons.db ".schema ecommerce_orders"
sqlite3 cryptons.db ".schema payments"
```

### Step 5: Test Basic Operations

Create a test order and payment:

```python
from app import create_app
from src.models import db
from src.trading_models import EcommerceOrder, Payment
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Create test order
    order = EcommerceOrder(
        order_id='TEST-ORDER-001',
        user_id=1,
        items=[{'product_id': 'test', 'name': 'Test Product', 'quantity': 1, 'price': 100.0}],
        subtotal=100.0,
        original_price_usd=100.0,
        cfv_discount=10.0,
        cfv_metrics={'valuationStatus': 'undervalued', 'valuationPercent': 50},
        total=90.0,
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    
    print(f"✓ Created test order: {order.order_id}")
    
    # Create test payment
    payment = Payment(
        payment_id='TEST-PAYMENT-001',
        order_id=order.id,
        user_id=1,
        cryptocurrency='XNO',
        amount_crypto=0.9,
        amount_usd=90.0,
        fair_value=165.0,
        cfv_discount=10.0,
        cfv_metrics={'valuationStatus': 'undervalued', 'valuationPercent': 50},
        payment_address='nano_test123',
        network_fee=0.001,
        total_amount=0.901,
        status='pending',
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )
    db.session.add(payment)
    db.session.commit()
    
    print(f"✓ Created test payment: {payment.payment_id}")
```

### Step 6: Restart Application

```bash
cd backend
python main.py
```

## Rollback Procedures

If you need to rollback the migration:

### Step 1: Stop Application

```bash
pkill -f "python main.py"
```

### Step 2: Run Downgrade

```bash
cd backend
python migrations/add_cfv_models.py downgrade
```

**Expected Output:**
```
Removing CFV tables...
✓ Successfully removed Payment and EcommerceOrder tables
```

### Step 3: Restore from Backup (if needed)

```bash
# PostgreSQL
psql -U username -d cryptons_db < backup_YYYYMMDD_HHMMSS.sql

# SQLite
mv backup_YYYYMMDD_HHMMSS.db cryptons.db
```

### Step 4: Verify Rollback

```bash
# Check that tables are removed
psql -U username -d cryptons_db -c "\dt"
```

## Data Validation

### Validation Script

Create a script to validate data integrity:

```python
from app import create_app
from src.models import db
from src.trading_models import EcommerceOrder, Payment

app = create_app()

with app.app_context():
    # Check for orphaned payments (payments without orders)
    orphaned_payments = db.session.query(Payment)\
        .outerjoin(EcommerceOrder, Payment.order_id == EcommerceOrder.id)\
        .filter(EcommerceOrder.id == None).all()
    
    if orphaned_payments:
        print(f"⚠ Found {len(orphaned_payments)} orphaned payments")
    else:
        print("✓ No orphaned payments")
    
    # Check for invalid CFV discount values
    invalid_discounts = EcommerceOrder.query.filter(
        (EcommerceOrder.cfv_discount < 0) | (EcommerceOrder.cfv_discount > 100)
    ).all()
    
    if invalid_discounts:
        print(f"⚠ Found {len(invalid_discounts)} orders with invalid discounts")
    else:
        print("✓ All discounts are valid (0-100%)")
    
    # Check for missing required fields
    orders_missing_metrics = EcommerceOrder.query.filter(
        EcommerceOrder.cfv_metrics == None
    ).filter(EcommerceOrder.cfv_discount > 0).all()
    
    if orders_missing_metrics:
        print(f"⚠ Found {len(orders_missing_metrics)} orders with discounts but no CFV metrics")
    else:
        print("✓ All discounted orders have CFV metrics")
    
    # Summary
    total_orders = EcommerceOrder.query.count()
    total_payments = Payment.query.count()
    print(f"\nSummary:")
    print(f"  Total orders: {total_orders}")
    print(f"  Total payments: {total_payments}")
```

### Automated Validation

Run validation after migration:

```bash
python migrations/validate_cfv_data.py
```

## Troubleshooting

### Common Issues

#### 1. Table Already Exists

**Error:**
```
Table 'ecommerce_orders' already exists
```

**Solution:**
```bash
# Drop the existing table and re-run migration
# WARNING: This will delete all data in the table
psql -U username -d cryptons_db -c "DROP TABLE IF EXISTS ecommerce_orders CASCADE;"
psql -U username -d cryptons_db -c "DROP TABLE IF EXISTS payments CASCADE;"
python migrations/add_cfv_models.py upgrade
```

#### 2. Foreign Key Constraint Fails

**Error:**
```
Foreign key constraint fails for user_id
```

**Solution:**
Ensure the users table exists before running migration:
```bash
# Check if users table exists
psql -U username -d cryptons_db -c "\d users"

# If not, create base tables first
python -c "from app import create_app; from src.models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

#### 3. JSON Column Not Supported

**Error:**
```
JSON column type not supported
```

**Solution:**
- For PostgreSQL: Ensure version 9.2+ (supports JSON)
- For SQLite: Ensure version 3.9.0+ (supports JSON1 extension)
- For MySQL: Ensure version 5.7.8+ (supports JSON)

#### 4. Migration Script Not Found

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
```bash
# Run from backend directory
cd backend
python migrations/add_cfv_models.py upgrade
```

### Getting Help

If you encounter issues:

1. Check application logs: `tail -f logs/app.log`
2. Verify database connection: Test with direct SQL queries
3. Review migration script: `cat migrations/add_cfv_models.py`
4. Contact support with error messages and logs

## Post-Migration Checklist

- [ ] Tables created successfully
- [ ] Validation script passes
- [ ] Test order created
- [ ] Test payment created
- [ ] Application starts without errors
- [ ] API endpoints respond correctly
- [ ] No orphaned records
- [ ] Backup created and verified
- [ ] Documentation updated
- [ ] Team notified of changes

## Notes

- Always backup before migration
- Test in development environment first
- Monitor application logs after migration
- Validate data integrity regularly
- Document any custom modifications

---

**Last Updated:** 2026-02-13  
**Version:** 1.0.0
