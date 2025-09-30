/**
 * Payment API Client
 * 
 * Provides functions to interact with the cryptocurrency payment backend API.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Get list of supported cryptocurrencies
 */
export async function getSupportedCurrencies() {
  const response = await fetch(`${API_BASE_URL}/api/payments/currencies`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch supported currencies');
  }
  
  return data.currencies;
}

/**
 * Create a new payment request
 */
export async function createPayment(amount, currency = 'BTC', orderId = null, metadata = {}) {
  const response = await fetch(`${API_BASE_URL}/api/payments/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount,
      currency,
      order_id: orderId,
      metadata
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to create payment');
  }
  
  return data.payment;
}

/**
 * Get payment information
 */
export async function getPayment(paymentId) {
  const response = await fetch(`${API_BASE_URL}/api/payments/${paymentId}`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch payment');
  }
  
  return data.payment;
}

/**
 * Check payment status
 */
export async function checkPaymentStatus(paymentId) {
  const response = await fetch(`${API_BASE_URL}/api/payments/${paymentId}/status`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to check payment status');
  }
  
  return data.status;
}

/**
 * Verify a payment transaction
 */
export async function verifyPayment(paymentId, transactionHash) {
  const response = await fetch(`${API_BASE_URL}/api/payments/${paymentId}/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      transaction_hash: transactionHash
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to verify payment');
  }
  
  return data.payment;
}

/**
 * Connect a cryptocurrency wallet
 */
export async function connectWallet(walletType, address, signature = null) {
  const response = await fetch(`${API_BASE_URL}/api/payments/wallet/connect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      wallet_type: walletType,
      address,
      signature
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to connect wallet');
  }
  
  return data.connection;
}

/**
 * Disconnect a wallet
 */
export async function disconnectWallet(sessionId) {
  const response = await fetch(`${API_BASE_URL}/api/payments/wallet/${sessionId}/disconnect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to disconnect wallet');
  }
  
  return data;
}

/**
 * Get wallet information
 */
export async function getWalletInfo(sessionId) {
  const response = await fetch(`${API_BASE_URL}/api/payments/wallet/${sessionId}`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to get wallet info');
  }
  
  return data.wallet;
}

/**
 * Get list of supported wallet providers
 */
export async function getSupportedWallets() {
  const response = await fetch(`${API_BASE_URL}/api/payments/wallets`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch supported wallets');
  }
  
  return data.wallets;
}

/**
 * Verify a blockchain transaction
 */
export async function verifyTransaction(txHash, currency, expectedAmount, expectedAddress) {
  const response = await fetch(`${API_BASE_URL}/api/payments/transaction/${txHash}/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      currency,
      expected_amount: expectedAmount,
      expected_address: expectedAddress
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to verify transaction');
  }
  
  return data.verification;
}
