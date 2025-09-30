import React, { useState } from 'react';
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

const PaymentGateway = ({ orderTotal = 0.001, currency = 'BTC', onPaymentComplete }) => {
  const [selectedMethod, setSelectedMethod] = useState('bitcoin');
  const [paymentStatus, setPaymentStatus] = useState('pending'); // pending, processing, completed, failed
  const [walletAddress, setWalletAddress] = useState('');
  const [transactionId, setTransactionId] = useState('');
  const [copied, setCopied] = useState(false);
  const [timeLeft, setTimeLeft] = useState(15 * 60); // 15 minutes in seconds

  // Mock Bitcoin address for payment
  const mockBitcoinAddress = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa';
  
  // Mock payment methods
  const paymentMethods = [
    {
      id: 'bitcoin',
      name: 'Bitcoin',
      icon: Bitcoin,
      description: 'Pay directly with Bitcoin',
      fee: '0.0001 BTC',
      supported: true
    },
    {
      id: 'wallet',
      name: 'Crypto Wallet',
      icon: Wallet,
      description: 'Connect your crypto wallet',
      fee: '0.00005 BTC',
      supported: true
    }
  ];

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
    setPaymentStatus('processing');
    
    try {
      // Simulate payment processing
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Mock transaction ID
      const mockTxId = '0x' + Math.random().toString(16).substring(2, 18);
      setTransactionId(mockTxId);
      
      // Simulate success/failure (90% success rate)
      const success = Math.random() > 0.1;
      
      if (success) {
        setPaymentStatus('completed');
        onPaymentComplete && onPaymentComplete({
          transactionId: mockTxId,
          amount: orderTotal,
          currency: currency,
          method: selectedMethod
        });
      } else {
        setPaymentStatus('failed');
      }
    } catch (error) {
      setPaymentStatus('failed');
    }
  };

  const renderPaymentForm = () => {
    if (selectedMethod === 'bitcoin') {
      return (
        <div className="space-y-4">
          <div className="text-center space-y-4">
            {/* QR Code placeholder */}
            <div className="mx-auto w-48 h-48 bg-white rounded-lg flex items-center justify-center">
              <QrCode className="w-32 h-32 text-gray-800" />
            </div>
            
            <div>
              <Label className="text-gray-300">Send Bitcoin to this address:</Label>
              <div className="flex items-center gap-2 mt-2">
                <Input
                  value={mockBitcoinAddress}
                  readOnly
                  className="bg-gray-700 border-gray-600 text-white font-mono text-sm"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyToClipboard(mockBitcoinAddress)}
                  className="border-gray-600 text-gray-300 hover:bg-gray-700"
                >
                  {copied ? <CheckCircle className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                </Button>
              </div>
            </div>

            <div className="text-center">
              <div className="text-2xl font-bold text-white">{orderTotal} {currency}</div>
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
              <div className="text-xl font-bold text-white">{orderTotal} {currency}</div>
              <div className="text-sm text-gray-400">Network fee: 0.00005 BTC</div>
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
                        <div className="text-sm text-gray-400">Fee: {method.fee}</div>
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
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                <CreditCard className="w-4 h-4 mr-2" />
                Complete Payment
              </Button>
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
                  <span className="text-white">{orderTotal} {currency}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Network Fee</span>
                  <span className="text-white">0.00005 {currency}</span>
                </div>
                <Separator className="bg-gray-700" />
                <div className="flex justify-between font-semibold">
                  <span className="text-white">Total</span>
                  <span className="text-white">{(orderTotal + 0.00005).toFixed(6)} {currency}</span>
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