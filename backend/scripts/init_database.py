#!/usr/bin/env python3
"""
Database initialization and migration script
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from src.database_config import init_database, DatabaseConfig
from src.models import db, User
from src.trading_models import TradingPair, Order, Trade, Portfolio, Transaction, MarketData, AuditLog


def create_app():
    """Create Flask app for database operations"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Initialize database
    db_instance, migrate = init_database(app)
    
    return app, db_instance


def init_db():
    """Initialize database tables"""
    app, db_instance = create_app()
    
    with app.app_context():
        print("🔄 Creating database tables...")
        db_instance.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default trading pairs
        print("\n🔄 Creating default trading pairs...")
        create_default_trading_pairs(db_instance)
        print("✅ Default trading pairs created!")
        
        print("\n✨ Database initialization complete!")


def create_default_trading_pairs(db_instance):
    """Create default trading pairs"""
    default_pairs = [
        {'symbol': 'BTC/USDT', 'base': 'BTC', 'quote': 'USDT', 'min_size': 0.0001, 'max_size': 1000},
        {'symbol': 'ETH/USDT', 'base': 'ETH', 'quote': 'USDT', 'min_size': 0.001, 'max_size': 10000},
        {'symbol': 'BNB/USDT', 'base': 'BNB', 'quote': 'USDT', 'min_size': 0.01, 'max_size': 100000},
        {'symbol': 'SOL/USDT', 'base': 'SOL', 'quote': 'USDT', 'min_size': 0.01, 'max_size': 50000},
        {'symbol': 'ADA/USDT', 'base': 'ADA', 'quote': 'USDT', 'min_size': 1.0, 'max_size': 1000000},
    ]
    
    for pair_data in default_pairs:
        existing = TradingPair.query.filter_by(symbol=pair_data['symbol']).first()
        if not existing:
            pair = TradingPair(
                symbol=pair_data['symbol'],
                base_currency=pair_data['base'],
                quote_currency=pair_data['quote'],
                min_order_size=pair_data['min_size'],
                max_order_size=pair_data['max_size']
            )
            db_instance.session.add(pair)
    
    db_instance.session.commit()


def reset_db():
    """Reset database (drop and recreate all tables)"""
    app, db_instance = create_app()
    
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("❌ Reset cancelled")
        return
    
    with app.app_context():
        print("\n🔄 Dropping all tables...")
        db_instance.drop_all()
        print("✅ Tables dropped!")
        
        print("\n🔄 Creating new tables...")
        db_instance.create_all()
        print("✅ Tables created!")
        
        print("\n🔄 Creating default data...")
        create_default_trading_pairs(db_instance)
        print("✅ Default data created!")
        
        print("\n✨ Database reset complete!")


def show_tables():
    """Show all database tables"""
    app, db_instance = create_app()
    
    with app.app_context():
        inspector = db.inspect(db_instance.engine)
        tables = inspector.get_table_names()
        
        print("\n📋 Database Tables:")
        print("=" * 50)
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\n{table}:")
            for col in columns:
                print(f"  - {col['name']} ({col['type']})")
        print("=" * 50)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python init_database.py [init|reset|show]")
        print("\nCommands:")
        print("  init  - Initialize database with tables")
        print("  reset - Drop and recreate all tables (WARNING: deletes all data)")
        print("  show  - Show all database tables and columns")
        return
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'reset':
        reset_db()
    elif command == 'show':
        show_tables()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, reset, show")


if __name__ == '__main__':
    main()
