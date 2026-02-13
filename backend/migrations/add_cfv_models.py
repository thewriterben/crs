"""
Database Migration Script for CFV Integration

Adds Payment and EcommerceOrder models to support CFV-based discounts
and cryptocurrency payment processing.

Run this script to create the new tables in the database.
"""

from src.models import db
from src.trading_models import Payment, EcommerceOrder
import sys


def upgrade():
    """Create new tables for CFV integration"""
    try:
        print("Creating tables for CFV integration...")
        
        # Create tables
        db.create_all()
        
        print("✓ Successfully created Payment and EcommerceOrder tables")
        print("\nNew tables:")
        print("  - ecommerce_orders: E-commerce orders with CFV discount support")
        print("  - payments: Cryptocurrency payments with CFV metrics")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False


def downgrade():
    """Remove CFV tables"""
    try:
        print("Removing CFV tables...")
        
        # Drop tables
        Payment.__table__.drop(db.engine, checkfirst=True)
        EcommerceOrder.__table__.drop(db.engine, checkfirst=True)
        
        print("✓ Successfully removed Payment and EcommerceOrder tables")
        
        return True
        
    except Exception as e:
        print(f"✗ Error removing tables: {e}")
        return False


def validate():
    """Validate the migration"""
    try:
        print("Validating migration...")
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = ['ecommerce_orders', 'payments']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"✗ Missing tables: {', '.join(missing_tables)}")
            return False
        
        print("✓ All required tables exist")
        
        # Validate columns for Payment table
        payment_columns = [col['name'] for col in inspector.get_columns('payments')]
        required_payment_columns = [
            'id', 'payment_id', 'order_id', 'user_id', 'cryptocurrency',
            'amount_crypto', 'amount_usd', 'fair_value', 'cfv_discount',
            'cfv_metrics', 'payment_address', 'status'
        ]
        
        missing_payment_cols = [c for c in required_payment_columns if c not in payment_columns]
        if missing_payment_cols:
            print(f"✗ Missing Payment columns: {', '.join(missing_payment_cols)}")
            return False
        
        print("✓ Payment table has all required columns")
        
        # Validate columns for EcommerceOrder table
        order_columns = [col['name'] for col in inspector.get_columns('ecommerce_orders')]
        required_order_columns = [
            'id', 'order_id', 'user_id', 'items', 'subtotal',
            'original_price_usd', 'cfv_discount', 'cfv_metrics', 'total', 'status'
        ]
        
        missing_order_cols = [c for c in required_order_columns if c not in order_columns]
        if missing_order_cols:
            print(f"✗ Missing EcommerceOrder columns: {', '.join(missing_order_cols)}")
            return False
        
        print("✓ EcommerceOrder table has all required columns")
        print("\n✓ Migration validation successful!")
        
        return True
        
    except Exception as e:
        print(f"✗ Error validating migration: {e}")
        return False


if __name__ == '__main__':
    from app import create_app
    
    app = create_app()
    
    with app.app_context():
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == 'upgrade':
                success = upgrade()
            elif command == 'downgrade':
                success = downgrade()
            elif command == 'validate':
                success = validate()
            else:
                print(f"Unknown command: {command}")
                print("Usage: python add_cfv_models.py [upgrade|downgrade|validate]")
                sys.exit(1)
            
            sys.exit(0 if success else 1)
        else:
            print("Database Migration: CFV Integration")
            print("\nUsage:")
            print("  python migrations/add_cfv_models.py upgrade    - Create new tables")
            print("  python migrations/add_cfv_models.py downgrade  - Remove tables")
            print("  python migrations/add_cfv_models.py validate   - Validate migration")
            sys.exit(0)
