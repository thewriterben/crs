/**
 * CFV Payment API Client
 * 
 * Provides functions to interact with the CFV-enabled payment backend API.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Get list of supported DGF cryptocurrencies with CFV data
 */
export async function getSupportedCoins() {
  const response = await fetch(`${API_BASE_URL}/api/cfv/coins`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to fetch supported coins');
  }
  
  return data.coins;
}

/**
 * Calculate CFV for a specific cryptocurrency
 */
export async function calculateCFV(symbol, forceRefresh = false) {
  const url = new URL(`${API_BASE_URL}/api/cfv/calculate/${symbol}`);
  if (forceRefresh) {
    url.searchParams.append('refresh', 'true');
  }
  
  const response = await fetch(url);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to calculate CFV');
  }
  
  return data;
}

/**
 * Get payment information with CFV discount
 */
export async function getPaymentInfo(symbol, amountUSD) {
  const response = await fetch(`${API_BASE_URL}/api/cfv/payment-info/${symbol}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount_usd: amountUSD
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to get payment info');
  }
  
  return data.payment_info;
}

/**
 * Create a new order with CFV discount
 */
export async function createOrder(orderData) {
  const response = await fetch(`${API_BASE_URL}/api/orders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(orderData)
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to create order');
  }
  
  return data.order;
}

/**
 * Create a payment for an order
 */
export async function createPayment(orderId, cryptocurrency, metadata = {}) {
  const response = await fetch(`${API_BASE_URL}/api/payments/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      order_id: orderId,
      cryptocurrency,
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
 * Get payment information by order ID
 */
export async function getPaymentByOrder(orderId) {
  const response = await fetch(`${API_BASE_URL}/api/payments/order/${orderId}`);
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to get payment');
  }
  
  return {
    order: data.order,
    payments: data.payments
  };
}

/**
 * Confirm a payment with transaction hash
 */
export async function confirmPayment(paymentId, transactionHash) {
  const response = await fetch(`${API_BASE_URL}/api/payments/confirm`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      payment_id: paymentId,
      transaction_hash: transactionHash
    })
  });
  
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error || 'Failed to confirm payment');
  }
  
  return {
    payment: data.payment,
    order: data.order
  };
}

/**
 * Format currency amount for display
 */
export function formatCurrency(amount, decimals = 2) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(amount);
}

/**
 * Format cryptocurrency amount for display
 */
export function formatCrypto(amount, decimals = 8) {
  return Number(amount).toFixed(decimals);
}

/**
 * Get valuation status color
 */
export function getValuationColor(status) {
  const colors = {
    undervalued: 'text-green-400',
    fair: 'text-yellow-400',
    overvalued: 'text-red-400'
  };
  return colors[status] || 'text-gray-400';
}

/**
 * Get valuation status icon
 */
export function getValuationIcon(status) {
  const icons = {
    undervalued: '📈',
    fair: '➡️',
    overvalued: '📉'
  };
  return icons[status] || '❓';
}
