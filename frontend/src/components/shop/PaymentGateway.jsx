import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Separator } from '@/components/ui/separator.jsx';
import { 
  CreditCard, 
  Bitcoin,
  Wallet,
  Shield,
  Copy,
  CheckCircle,
  AlertCircle,
  QrCode,
  Timer
} from 'lucide-react';
import { createPayment, verifyPayment, getSupportedCurrencies } from '@/lib/paymentApi.js';

const PaymentGateway = ({ orderTotal = 0.001, currency = 'BTC', orderId = null, onPaymentComplete }) => {
  const [selectedMethod, setSelectedMethod] = useState('bitcoin');
  const [paymentStatus, setPaymentStatus] = useState('pending'); // pending, processing, completed, failed
  const [transactionId, setTransactionId] = useState('');
  const [copied, setCopied] = useState(false);
  const [timeLeft, setTimeLeft] = useState(15 * 60); // 15 minutes in seconds
  const [paymentData, setPaymentData] = useState(null);
  const [supportedCurrencies, setSupportedCurrencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Payment methods
  const paymentMethods = [
    {
      id: 'bitcoin',
      name: 'Bitcoin',
      icon: Bitcoin,
      description: 'Pay directly with Bitcoin',
      currency: 'BTC',
      supported: true
    },
    {
      id: 'ethereum',
      name: 'Ethereum',
      icon: Wallet,
      description: 'Pay with Ethereum',
      currency: 'ETH',
      supported: true
    },
    {
      id: 'wallet',
      name: 'Crypto Wallet',
      icon: Wallet,
      description: 'Connect your crypto wallet',
      currency: currency,
      supported: true
    }
  ];

  // Load supported currencies on mount
  useEffect(() => {
    const loadCurrencies = async () => {
      try {
        const currencies = await getSupportedCurrencies();
        setSupportedCurrencies(currencies);
      } catch (err) {
        console.error('Failed to load currencies:', err);
      }
    };
    loadCurrencies();
  }, []);

  // Create payment when component mounts or currency changes
  useEffect(() => {
    const initPayment = async () => {
      if (paymentData) return; // Already initialized
      
      try {
        setLoading(true);
        const selectedCurrency = paymentMethods.find(m => m.id === selectedMethod)?.currency || currency;
        const payment = await createPayment(orderTotal, selectedCurrency, orderId, {
          method: selectedMethod
        });
        setPaymentData(payment);
        setError(null);
      } catch (err) {
        console.error('Failed to create payment:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    initPayment();
  }, [orderTotal, currency, orderId, selectedMethod]);

  // Countdown timer
  useEffect(() => {
    if (paymentStatus !== 'pending') return;
    
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 0) {
          clearInterval(timer);
          setPaymentStatus('expired');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    
    return () => clearInterval(timer);
  }, [paymentStatus]);

  // Format time for countdown
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handlePayment = async () => {
    if (!paymentData) {
      setError('Payment not initialized');
      return;
    }
    
    setPaymentStatus('processing');
    setLoading(true);
    
    try {
      // Simulate user completing the transaction
      // In production, this would wait for actual blockchain transaction
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Generate mock transaction hash
      const mockTxId = '0x' + Math.random().toString(16).substring(2, 66);
      setTransactionId(mockTxId);
      
      // Verify the payment with the backend
      const verifiedPayment = await verifyPayment(paymentData.payment_id, mockTxId);
      
      if (verifiedPayment.status === 'completed' || verifiedPayment.status === 'processing') {
        setPaymentStatus('completed');
        onPaymentComplete && onPaymentComplete({
          transactionId: mockTxId,
          paymentId: paymentData.payment_id,
          amount: orderTotal,
          currency: paymentData.currency,
          method: selectedMethod
        });
      } else {
        setPaymentStatus('failed');
        setError('Payment verification failed');
      }
    } catch (error) {
      console.error('Payment error:', error);
      setPaymentStatus('failed');
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const renderPaymentForm = () => {
    if (loading && !paymentData) {
      return (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-400 mt-4">Initializing payment...</p>
        </div>
      );
    }

    if (error && !paymentData) {
      return (
        <div className="text-center py-8">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p className="text-red-400">{error}</p>
        </div>
      );
    }

    if (selectedMethod === 'bitcoin' || selectedMethod === 'ethereum') {
      const paymentAddress = paymentData?.payment_address || '';
      const displayAmount = paymentData?.total_amount || orderTotal;
      const displayCurrency = paymentData?.currency || currency;
      
      return (
        <div className="space-y-4">
          <div className="text-center space-y-4">
            {/* QR Code placeholder */}
            <div className="mx-auto w-48 h-48 bg-white rounded-lg flex items-center justify-center">
              <QrCode className="w-32 h-32 text-gray-800" />
            </div>
            
            <div>
              <Label className="text-gray-300">
                Send {selectedMethod === 'ethereum' ? 'Ethereum' : 'Bitcoin'} to this address:
              </Label>
              <div className="flex items-center gap-2 mt-2">
                <Input
                  value={paymentAddress}
                  readOnly
                  className="bg-gray-700 border-gray-600 text-white font-mono text-sm"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyToClipboard(paymentAddress)}
                  className="border-gray-600 text-gray-300 hover:bg-gray-700"
                >
                  {copied ? <CheckCircle className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                </Button>
              </div>
            </div>

            <div className="text-center">
              <div className="text-2xl font-bold text-white">{displayAmount} {displayCurrency}</div>
              <div className="text-sm text-gray-400">Exact amount required</div>
            </div>
          </div>
        </div>
      );
    }

    if (selectedMethod === 'wallet') {
      return (
        <div className="space-y-4">
          <div className="text-center space-y-4">
            <Wallet className="w-16 h-16 text-blue-400 mx-auto" />
            <div>
              <h3 className="text-lg font-semibold text-white">Connect Your Wallet</h3>
              <p className="text-gray-400">We'll redirect you to your wallet to complete the payment</p>
            </div>
            
            <div className="space-y-2">
              <div className="text-xl font-bold text-white">
                {paymentData?.total_amount || orderTotal} {paymentData?.currency || currency}
              </div>
              <div className="text-sm text-gray-400">
                Network fee: {paymentData?.network_fee || '0.00005'} {paymentData?.currency || currency}
              </div>
            </div>
          </div>
        </div>
      );
    }
  };

  const renderPaymentStatus = () => {
    switch (paymentStatus) {
      case 'processing':
        return (
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto"></div>
            <div>
              <h3 className="text-lg font-semibold text-white">Processing Payment</h3>
              <p className="text-gray-400">Please wait while we confirm your transaction...</p>
            </div>
          </div>
        );
        
      case 'completed':
        return (
          <div className="text-center space-y-4">
            <CheckCircle className="w-16 h-16 text-green-400 mx-auto" />
            <div>
              <h3 className="text-lg font-semibold text-white">Payment Successful!</h3>
              <p className="text-gray-400">Your payment has been confirmed</p>
            </div>
            {transactionId && (
              <div className="bg-gray-700 p-3 rounded-lg">
                <div className="text-sm text-gray-400">Transaction ID:</div>
                <div className="font-mono text-sm text-white break-all">{transactionId}</div>
              </div>
            )}
          </div>
        );
        
      case 'failed':
        return (
          <div className="text-center space-y-4">
            <AlertCircle className="w-16 h-16 text-red-400 mx-auto" />
            <div>
              <h3 className="text-lg font-semibold text-white">Payment Failed</h3>
              <p className="text-gray-400">There was an issue processing your payment. Please try again.</p>
            </div>
            <Button 
              onClick={() => setPaymentStatus('pending')}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              Try Again
            </Button>
          </div>
        );
        
      default:
        return null;
    }
  };

  if (paymentStatus === 'processing' || paymentStatus === 'completed' || paymentStatus === 'failed') {
    return (
      <div className="space-y-6">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-8">
            {renderPaymentStatus()}
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Payment</h1>
        <p className="text-gray-400">Complete your purchase securely with cryptocurrency</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Payment Methods */}
        <div className="lg:col-span-2">
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="text-white">Select Payment Method</CardTitle>
              <CardDescription className="text-gray-400">
                Choose how you'd like to pay for your order
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {paymentMethods.map((method) => {
                const IconComponent = method.icon;
                return (
                  <div
                    key={method.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedMethod === method.id
                        ? 'border-blue-500 bg-blue-900/20'
                        : 'border-gray-600 hover:border-gray-500'
                    }`}
                    onClick={() => setSelectedMethod(method.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <IconComponent className="w-8 h-8 text-orange-400" />
                        <div>
                          <div className="font-semibold text-white">{method.name}</div>
                          <div className="text-sm text-gray-400">{method.description}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        {method.supported && (
                          <Badge variant="outline" className="border-green-600 text-green-400 text-xs">
                            Supported
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}

              <Separator className="bg-gray-700" />

              {/* Payment Form */}
              {renderPaymentForm()}

              {/* Action Button */}
              <Button 
                onClick={handlePayment}
                disabled={loading || !paymentData}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50"
              >
                <CreditCard className="w-4 h-4 mr-2" />
                {loading ? 'Processing...' : 'Complete Payment'}
              </Button>

              {error && (
                <div className="flex items-center gap-2 p-3 bg-red-900/20 border border-red-700 rounded-lg text-sm text-red-400">
                  <AlertCircle className="w-4 h-4 flex-shrink-0" />
                  <span>{error}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <Card className="bg-gray-800 border-gray-700 sticky top-6">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Shield className="w-5 h-5 text-green-400" />
                Secure Payment
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Order total */}
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-400">Order Total</span>
                  <span className="text-white">{orderTotal} {paymentData?.currency || currency}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Network Fee</span>
                  <span className="text-white">
                    {paymentData?.network_fee || '0.00005'} {paymentData?.currency || currency}
                  </span>
                </div>
                <Separator className="bg-gray-700" />
                <div className="flex justify-between font-semibold">
                  <span className="text-white">Total</span>
                  <span className="text-white">
                    {paymentData?.total_amount?.toFixed(6) || (orderTotal + 0.00005).toFixed(6)} {paymentData?.currency || currency}
                  </span>
                </div>
              </div>

              {/* Payment timer */}
              <div className="flex items-center gap-2 p-3 bg-orange-900/20 border border-orange-700 rounded-lg">
                <Timer className="w-4 h-4 text-orange-400" />
                <div className="text-sm">
                  <div className="text-orange-400">Payment expires in</div>
                  <div className="font-mono text-white">{formatTime(timeLeft)}</div>
                </div>
              </div>

              {/* Security features */}
              <div className="space-y-2 text-xs text-gray-400">
                <div className="flex items-center gap-2">
                  <Shield className="w-3 h-3" />
                  <span>256-bit SSL encryption</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3" />
                  <span>Blockchain verified transactions</span>
                </div>
                <div className="flex items-center gap-2">
                  <Shield className="w-3 h-3" />
                  <span>No personal data stored</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PaymentGateway;