"""
CFV API Endpoints

Provides REST API endpoints for CFV calculations, payment processing,
and order management with integrated discount functionality.
"""

import hashlib
import secrets
import time
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from src.models import db
from src.trading_models import Payment, EcommerceOrder
from services.cfv_service import CFVService

# Create blueprint
cfv_api = Blueprint('cfv_api', __name__)

# Initialize CFV service
cfv_service = CFVService()


@cfv_api.route('/api/cfv/coins', methods=['GET'])
def get_supported_coins():
    """Get list of supported DGF coins"""
    try:
        coins = cfv_service.get_supported_coins()
        
        # Add CFV data for each coin
        coins_with_cfv = []
        for coin in coins:
            try:
                cfv_data = cfv_service.calculate_cfv(coin['symbol'])
                coin['cfv'] = cfv_data
                
                # Calculate discount for display
                discount, _ = cfv_service.calculate_discount(coin['symbol'])
                coin['discount'] = discount
            except Exception as e:
                print(f"Error getting CFV for {coin['symbol']}: {e}")
                coin['cfv'] = None
                coin['discount'] = 0
            
            coins_with_cfv.append(coin)
        
        return jsonify({
            'success': True,
            'coins': coins_with_cfv,
            'count': len(coins_with_cfv)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cfv_api.route('/api/cfv/calculate/<symbol>', methods=['GET'])
def calculate_cfv(symbol):
    """Calculate CFV for a specific cryptocurrency"""
    try:
        symbol = symbol.upper()
        
        if not cfv_service.is_supported(symbol):
            return jsonify({
                'success': False,
                'error': f'Unsupported cryptocurrency: {symbol}'
            }), 400
        
        # Get force_refresh parameter
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        # Calculate CFV
        cfv_data = cfv_service.calculate_cfv(symbol, force_refresh)
        
        if not cfv_data:
            return jsonify({
                'success': False,
                'error': 'Failed to calculate CFV'
            }), 500
        
        # Calculate discount
        discount, cfv_metrics = cfv_service.calculate_discount(symbol)
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'cfv': cfv_data,
            'discount': discount,
            'metrics': cfv_metrics
        }), 200
        
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


@cfv_api.route('/api/cfv/payment-info/<symbol>', methods=['POST'])
def get_payment_info(symbol):
    """Get payment information with CFV discount"""
    try:
        data = request.get_json()
        
        if not data or 'amount_usd' not in data:
            return jsonify({
                'success': False,
                'error': 'amount_usd is required'
            }), 400
        
        amount_usd = float(data['amount_usd'])
        
        if amount_usd <= 0:
            return jsonify({
                'success': False,
                'error': 'amount_usd must be positive'
            }), 400
        
        # Get payment info with discount
        payment_info = cfv_service.get_payment_info(symbol, amount_usd)
        
        return jsonify({
            'success': True,
            'payment_info': payment_info
        }), 200
        
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


@cfv_api.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new e-commerce order with CFV discount"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['items', 'cryptocurrency']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        items = data['items']
        cryptocurrency = data['cryptocurrency'].upper()
        user_id = data.get('user_id', 1)  # Default to user 1 for testing
        
        # Calculate subtotal
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        
        # Get shipping cost
        shipping_cost = data.get('shipping_cost', 0.0)
        original_total = subtotal + shipping_cost
        
        # Calculate CFV discount
        discount_percent, cfv_metrics = cfv_service.calculate_discount(cryptocurrency)
        
        # Apply discount to total
        final_total = original_total * (1 - discount_percent / 100)
        
        # Generate order ID
        order_id = _generate_order_id()
        
        # Create order
        order = EcommerceOrder(
            order_id=order_id,
            user_id=user_id,
            items=items,
            subtotal=subtotal,
            original_price_usd=original_total,
            cfv_discount=discount_percent,
            cfv_metrics=cfv_metrics,
            total=final_total,
            shipping_address=data.get('shipping_address'),
            shipping_method=data.get('shipping_method'),
            shipping_cost=shipping_cost,
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cfv_api.route('/api/payments/create', methods=['POST'])
def create_payment():
    """Create a payment for an order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['order_id', 'cryptocurrency']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        order_id_str = data['order_id']
        cryptocurrency = data['cryptocurrency'].upper()
        
        # Find order
        order = EcommerceOrder.query.filter_by(order_id=order_id_str).first()
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        if order.status != 'pending':
            return jsonify({
                'success': False,
                'error': f'Order is already {order.status}'
            }), 400
        
        # Validate cryptocurrency
        if not cfv_service.is_supported(cryptocurrency):
            return jsonify({
                'success': False,
                'error': f'Unsupported cryptocurrency: {cryptocurrency}'
            }), 400
        
        # Get CFV data
        cfv_data = cfv_service.calculate_cfv(cryptocurrency)
        current_price = cfv_data.get('currentPrice', 100.0) if cfv_data else 100.0
        
        # Calculate crypto amount
        amount_crypto = order.total / current_price
        
        # Generate payment ID and address
        payment_id = _generate_payment_id()
        payment_address = _generate_payment_address(cryptocurrency, payment_id)
        
        # Network fee (mock for now)
        network_fee = amount_crypto * 0.001  # 0.1% fee
        total_amount = amount_crypto + network_fee
        
        # Create payment
        payment = Payment(
            payment_id=payment_id,
            order_id=order.id,
            user_id=order.user_id,
            cryptocurrency=cryptocurrency,
            amount_crypto=amount_crypto,
            amount_usd=order.total,
            fair_value=cfv_data.get('fairValue') if cfv_data else None,
            cfv_discount=order.cfv_discount,
            cfv_metrics=order.cfv_metrics,
            payment_address=payment_address,
            network_fee=network_fee,
            total_amount=total_amount,
            status='pending',
            expires_at=datetime.utcnow() + timedelta(minutes=15),
            metadata=data.get('metadata', {})
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cfv_api.route('/api/payments/order/<order_id>', methods=['GET'])
def get_payment_by_order(order_id):
    """Get payment information by order ID"""
    try:
        # Find order
        order = EcommerceOrder.query.filter_by(order_id=order_id).first()
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        # Get payments for this order
        payments = Payment.query.filter_by(order_id=order.id).all()
        
        return jsonify({
            'success': True,
            'order': order.to_dict(),
            'payments': [p.to_dict() for p in payments]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@cfv_api.route('/api/payments/confirm', methods=['POST'])
def confirm_payment():
    """Confirm a payment with transaction hash"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['payment_id', 'transaction_hash']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        payment_id = data['payment_id']
        transaction_hash = data['transaction_hash']
        
        # Find payment
        payment = Payment.query.filter_by(payment_id=payment_id).first()
        
        if not payment:
            return jsonify({
                'success': False,
                'error': 'Payment not found'
            }), 404
        
        # Check if payment is expired
        if datetime.utcnow() > payment.expires_at:
            payment.status = 'expired'
            db.session.commit()
            return jsonify({
                'success': False,
                'error': 'Payment has expired'
            }), 400
        
        # Update payment
        payment.transaction_hash = transaction_hash
        payment.status = 'processing'
        payment.confirmations = 1
        payment.confirmed_at = datetime.utcnow()
        
        # For now, auto-complete (in production, would verify on blockchain)
        payment.status = 'completed'
        payment.completed_at = datetime.utcnow()
        
        # Update order status
        order = EcommerceOrder.query.get(payment.order_id)
        if order:
            order.status = 'paid'
            order.paid_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'order': order.to_dict() if order else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _generate_order_id():
    """Generate a unique order ID"""
    timestamp = str(time.time())
    random_data = secrets.token_hex(4)
    return f"ORD-{hashlib.sha256(f'{timestamp}{random_data}'.encode()).hexdigest()[:12].upper()}"


def _generate_payment_id():
    """Generate a unique payment ID"""
    timestamp = str(time.time())
    random_data = secrets.token_hex(8)
    return hashlib.sha256(f"{timestamp}{random_data}".encode()).hexdigest()[:16]


def _generate_payment_address(currency, payment_id):
    """Generate a payment address for the specified currency"""
    address_hash = hashlib.sha256(f"{currency}{payment_id}".encode()).hexdigest()
    
    if currency in ['BTC', 'BTC-LN']:
        return f"bc1q{address_hash[:40]}"
    elif currency in ['ETH', 'USDT']:
        return f"0x{address_hash[:40]}"
    elif currency == 'XNO':
        return f"nano_{address_hash[:60]}"
    elif currency == 'XMR':
        return f"4{address_hash[:94]}"
    else:
        return f"{currency.lower()}_{address_hash[:40]}"
