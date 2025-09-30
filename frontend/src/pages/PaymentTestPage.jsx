import React from 'react';
import PaymentGateway from '@/components/shop/PaymentGateway.jsx';

const PaymentTestPage = () => {
  const handlePaymentComplete = (paymentInfo) => {
    console.log('Payment completed successfully!', paymentInfo);
    alert(`Payment completed! Transaction ID: ${paymentInfo.transactionId}`);
  };

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <PaymentGateway
          orderTotal={0.001}
          currency="BTC"
          orderId="test_order_123"
          onPaymentComplete={handlePaymentComplete}
        />
      </div>
    </div>
  );
};

export default PaymentTestPage;
