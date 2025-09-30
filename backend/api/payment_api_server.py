"""
Payment API Server

Provides REST API endpoints for cryptocurrency payment processing.
"""

import sys
import os
from flask import Blueprint, jsonify, request
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payments.crypto_payment_processor import CryptoPaymentProcessor
from payments.transaction_verifier import TransactionVerifier
from payments.wallet_manager import WalletManager

# Create Blueprint
payment_api = Blueprint('payment_api', __name__)

# Initialize services
payment_processor = CryptoPaymentProcessor()
transaction_verifier = TransactionVerifier()
wallet_manager = WalletManager()


@payment_api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Payment API',
        'timestamp': datetime.now().isoformat()
    })


@payment_api.route('/currencies', methods=['GET'])
def get_supported_currencies():
    """Get list of supported cryptocurrencies"""
    try:
        currencies = payment_processor.get_supported_currencies()
        return jsonify({
            'success': True,
            'currencies': currencies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/create', methods=['POST'])
def create_payment():
    """
    Create a new payment request
    
    Request body:
    {
        "amount": 0.001,
        "currency": "BTC",
        "order_id": "order_123",
        "metadata": {}
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'amount' not in data:
            return jsonify({
                'success': False,
                'error': 'Amount is required'
            }), 400
        
        amount = float(data['amount'])
        currency = data.get('currency', 'BTC')
        order_id = data.get('order_id')
        metadata = data.get('metadata', {})
        
        # Create payment
        payment = payment_processor.create_payment(
            amount=amount,
            currency=currency,
            order_id=order_id,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'payment': payment
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get payment information by ID"""
    try:
        payment = payment_processor.get_payment(payment_id)
        
        if not payment:
            return jsonify({
                'success': False,
                'error': 'Payment not found'
            }), 404
        
        return jsonify({
            'success': True,
            'payment': payment
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/<payment_id>/status', methods=['GET'])
def check_payment_status(payment_id):
    """Check payment status"""
    try:
        status = payment_processor.check_payment_status(payment_id)
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/<payment_id>/verify', methods=['POST'])
def verify_payment(payment_id):
    """
    Verify a payment transaction
    
    Request body:
    {
        "transaction_hash": "0x..."
    }
    """
    try:
        data = request.get_json()
        
        if 'transaction_hash' not in data:
            return jsonify({
                'success': False,
                'error': 'Transaction hash is required'
            }), 400
        
        transaction_hash = data['transaction_hash']
        
        # Verify payment
        payment = payment_processor.verify_payment(payment_id, transaction_hash)
        
        return jsonify({
            'success': True,
            'payment': payment
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/wallet/connect', methods=['POST'])
def connect_wallet():
    """
    Connect a cryptocurrency wallet
    
    Request body:
    {
        "wallet_type": "metamask",
        "address": "0x...",
        "signature": "..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'wallet_type' not in data or 'address' not in data:
            return jsonify({
                'success': False,
                'error': 'Wallet type and address are required'
            }), 400
        
        wallet_type = data['wallet_type']
        address = data['address']
        signature = data.get('signature')
        
        # Connect wallet
        connection = wallet_manager.connect_wallet(
            wallet_type=wallet_type,
            address=address,
            signature=signature
        )
        
        return jsonify({
            'success': True,
            'connection': connection
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/wallet/<session_id>/disconnect', methods=['POST'])
def disconnect_wallet(session_id):
    """Disconnect a wallet session"""
    try:
        success = wallet_manager.disconnect_wallet(session_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Wallet disconnected successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/wallet/<session_id>', methods=['GET'])
def get_wallet_info(session_id):
    """Get wallet information"""
    try:
        wallet_info = wallet_manager.get_wallet_info(session_id)
        
        if not wallet_info:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'wallet': wallet_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/wallets', methods=['GET'])
def get_supported_wallets():
    """Get list of supported wallet providers"""
    try:
        wallets = wallet_manager.get_supported_wallets()
        return jsonify({
            'success': True,
            'wallets': wallets
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_api.route('/transaction/<tx_hash>/verify', methods=['POST'])
def verify_transaction(tx_hash):
    """
    Verify a blockchain transaction
    
    Request body:
    {
        "currency": "BTC",
        "expected_amount": 0.001,
        "expected_address": "..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'currency' not in data or 'expected_amount' not in data or 'expected_address' not in data:
            return jsonify({
                'success': False,
                'error': 'Currency, expected_amount, and expected_address are required'
            }), 400
        
        currency = data['currency']
        expected_amount = float(data['expected_amount'])
        expected_address = data['expected_address']
        
        # Verify transaction
        result = transaction_verifier.verify_transaction(
            tx_hash=tx_hash,
            currency=currency,
            expected_amount=expected_amount,
            expected_address=expected_address
        )
        
        return jsonify({
            'success': True,
            'verification': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Create Flask app with payment routes
def create_payment_app():
    """Create and configure the payment API app"""
    from flask import Flask
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    # Register payment blueprint
    app.register_blueprint(payment_api, url_prefix='/api/payments')
    
    return app


if __name__ == '__main__':
    app = create_payment_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
