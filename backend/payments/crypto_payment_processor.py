"""
Cryptocurrency Payment Processor

Handles payment processing for multiple cryptocurrencies including Bitcoin,
Ethereum, and other popular crypto assets.
"""

import hashlib
import time
import secrets
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class CryptoPaymentProcessor:
    """Main payment processor for cryptocurrency transactions"""
    
    # Supported cryptocurrencies with their properties
    SUPPORTED_CURRENCIES = {
        'BTC': {
            'name': 'Bitcoin',
            'decimals': 8,
            'network_fee': 0.0001,
            'confirmation_time': 600,  # seconds
            'min_confirmations': 1
        },
        'ETH': {
            'name': 'Ethereum',
            'decimals': 18,
            'network_fee': 0.005,
            'confirmation_time': 180,
            'min_confirmations': 12
        },
        'USDT': {
            'name': 'Tether',
            'decimals': 6,
            'network_fee': 0.001,
            'confirmation_time': 180,
            'min_confirmations': 12
        },
        'BNB': {
            'name': 'Binance Coin',
            'decimals': 18,
            'network_fee': 0.0005,
            'confirmation_time': 60,
            'min_confirmations': 1
        }
    }
    
    def __init__(self):
        """Initialize the payment processor"""
        self.payments = {}  # Store payment records
        self.addresses = {}  # Store generated addresses
    
    def create_payment(self, amount: float, currency: str = 'BTC', 
                      order_id: str = None, metadata: dict = None) -> Dict:
        """
        Create a new payment request
        
        Args:
            amount: Payment amount in the specified currency
            currency: Cryptocurrency code (BTC, ETH, etc.)
            order_id: Optional order ID to associate with payment
            metadata: Additional metadata for the payment
            
        Returns:
            Payment information including address and details
        """
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")
        
        # Generate unique payment ID
        payment_id = self._generate_payment_id()
        
        # Generate payment address
        payment_address = self._generate_payment_address(currency, payment_id)
        
        # Calculate network fee and total
        currency_info = self.SUPPORTED_CURRENCIES[currency]
        network_fee = currency_info['network_fee']
        total_amount = amount + network_fee
        
        # Calculate expiration time (15 minutes from now)
        expires_at = datetime.now() + timedelta(minutes=15)
        
        # Create payment record
        payment = {
            'payment_id': payment_id,
            'order_id': order_id,
            'currency': currency,
            'amount': amount,
            'network_fee': network_fee,
            'total_amount': total_amount,
            'payment_address': payment_address,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'confirmations': 0,
            'transaction_hash': None,
            'metadata': metadata or {}
        }
        
        # Store payment
        self.payments[payment_id] = payment
        self.addresses[payment_address] = payment_id
        
        return payment
    
    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Get payment information by ID
        
        Args:
            payment_id: The payment ID
            
        Returns:
            Payment information or None if not found
        """
        return self.payments.get(payment_id)
    
    def verify_payment(self, payment_id: str, transaction_hash: str) -> Dict:
        """
        Verify a payment transaction
        
        Args:
            payment_id: The payment ID
            transaction_hash: Blockchain transaction hash
            
        Returns:
            Updated payment information
        """
        payment = self.payments.get(payment_id)
        if not payment:
            raise ValueError(f"Payment not found: {payment_id}")
        
        if payment['status'] == 'completed':
            return payment
        
        # Simulate transaction verification
        # In production, this would query blockchain APIs
        is_valid = self._verify_transaction(
            payment['payment_address'],
            payment['total_amount'],
            transaction_hash,
            payment['currency']
        )
        
        if is_valid:
            payment['transaction_hash'] = transaction_hash
            payment['status'] = 'processing'
            payment['confirmations'] = 1
            payment['confirmed_at'] = datetime.now().isoformat()
            
            # Check if we have enough confirmations
            currency_info = self.SUPPORTED_CURRENCIES[payment['currency']]
            if payment['confirmations'] >= currency_info['min_confirmations']:
                payment['status'] = 'completed'
        else:
            payment['status'] = 'failed'
            payment['error'] = 'Transaction verification failed'
        
        return payment
    
    def check_payment_status(self, payment_id: str) -> Dict:
        """
        Check the current status of a payment
        
        Args:
            payment_id: The payment ID
            
        Returns:
            Payment status information
        """
        payment = self.payments.get(payment_id)
        if not payment:
            raise ValueError(f"Payment not found: {payment_id}")
        
        # Check if payment has expired
        expires_at = datetime.fromisoformat(payment['expires_at'])
        if datetime.now() > expires_at and payment['status'] == 'pending':
            payment['status'] = 'expired'
        
        return {
            'payment_id': payment['payment_id'],
            'status': payment['status'],
            'confirmations': payment['confirmations'],
            'transaction_hash': payment['transaction_hash'],
            'amount': payment['amount'],
            'currency': payment['currency']
        }
    
    def get_supported_currencies(self) -> List[Dict]:
        """
        Get list of supported cryptocurrencies
        
        Returns:
            List of supported currency information
        """
        return [
            {
                'code': code,
                'name': info['name'],
                'decimals': info['decimals'],
                'network_fee': info['network_fee'],
                'confirmation_time': info['confirmation_time']
            }
            for code, info in self.SUPPORTED_CURRENCIES.items()
        ]
    
    def _generate_payment_id(self) -> str:
        """Generate a unique payment ID"""
        timestamp = str(time.time())
        random_data = secrets.token_hex(8)
        return hashlib.sha256(f"{timestamp}{random_data}".encode()).hexdigest()[:16]
    
    def _generate_payment_address(self, currency: str, payment_id: str) -> str:
        """
        Generate a payment address for the specified currency
        
        In production, this would interact with actual wallet services.
        For now, we generate mock addresses based on the payment ID.
        """
        # Generate a deterministic but unique address based on payment_id
        address_hash = hashlib.sha256(f"{currency}{payment_id}".encode()).hexdigest()
        
        if currency == 'BTC':
            # Bitcoin addresses start with 1, 3, or bc1
            return f"bc1q{address_hash[:40]}"
        elif currency == 'ETH' or currency == 'USDT':
            # Ethereum addresses start with 0x
            return f"0x{address_hash[:40]}"
        elif currency == 'BNB':
            # BNB addresses (BSC)
            return f"0x{address_hash[:40]}"
        else:
            return address_hash[:42]
    
    def _verify_transaction(self, address: str, amount: float, 
                           tx_hash: str, currency: str) -> bool:
        """
        Verify a blockchain transaction
        
        In production, this would query blockchain explorers or run a full node.
        For now, we simulate verification.
        
        Args:
            address: Payment address
            amount: Expected amount
            tx_hash: Transaction hash
            currency: Cryptocurrency code
            
        Returns:
            True if transaction is valid, False otherwise
        """
        # Simulate verification with 95% success rate
        # In production, this would:
        # 1. Query blockchain API (e.g., blockcypher, etherscan)
        # 2. Verify transaction exists
        # 3. Verify correct amount was sent
        # 4. Verify correct address was used
        # 5. Check number of confirmations
        
        # Basic validation
        if not tx_hash or len(tx_hash) < 10:
            return False
        
        if amount <= 0:
            return False
        
        # Simulate successful verification
        return True
