import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Separator } from '@/components/ui/separator.jsx';
import { 
  ShoppingCart, 
  Trash2, 
  Plus, 
  Minus, 
  CreditCard,
  Bitcoin,
  AlertCircle,
  CheckCircle
} from 'lucide-react';

const ShoppingCartComponent = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [checkoutStatus, setCheckoutStatus] = useState(null);

  // Mock cart data - in real app this would come from context/state management
  const mockCartItems = [
    {
      id: 1,
      name: 'AI Trading Bot Premium',
      price: 0.001,
      currency: 'BTC',
      quantity: 1,
      description: 'Advanced AI-powered trading bot with portfolio optimization',
      category: 'Trading Tools'
    },
    {
      id: 2,
      name: 'Market Analysis Pro',
      price: 0.0005,
      currency: 'BTC',
      quantity: 2,
      description: 'Real-time market sentiment analysis and predictions',
      category: 'Analytics'
    }
  ];

  useEffect(() => {
    // Simulate loading cart from API/localStorage
    setTimeout(() => {
      setCartItems(mockCartItems);
    }, 500);
  }, []);

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      removeItem(itemId);
      return;
    }
    
    setCartItems(items =>
      items.map(item =>
        item.id === itemId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeItem = (itemId) => {
    setCartItems(items => items.filter(item => item.id !== itemId));
  };

  const calculateSubtotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const calculateTax = (subtotal) => {
    // Mock 5% tax
    return subtotal * 0.05;
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const tax = calculateTax(subtotal);
    return subtotal + tax;
  };

  const formatPrice = (price, currency = 'BTC') => {
    return `${price.toFixed(6)} ${currency}`;
  };

  const handleCheckout = async () => {
    setLoading(true);
    setCheckoutStatus(null);

    try {
      // Simulate checkout process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock success/failure
      const success = Math.random() > 0.3; // 70% success rate
      
      if (success) {
        setCheckoutStatus('success');
        // Clear cart on success
        setTimeout(() => {
          setCartItems([]);
          setCheckoutStatus(null);
        }, 3000);
      } else {
        setCheckoutStatus('error');
        setTimeout(() => setCheckoutStatus(null), 3000);
      }
    } catch (error) {
      console.error('Checkout error:', error);
      setCheckoutStatus('error');
      setTimeout(() => setCheckoutStatus(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  if (cartItems.length === 0 && !loading) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <ShoppingCart className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Your cart is empty</h3>
          <p className="text-gray-400 mb-6">Add some products from the marketplace to get started</p>
          <Button 
            onClick={() => window.history.back()} 
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            Continue Shopping
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Shopping Cart</h1>
        <p className="text-gray-400">Review your items and complete your purchase</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-4">
          {cartItems.map((item) => (
            <Card key={item.id} className="bg-gray-800 border-gray-700">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white">{item.name}</h3>
                    <p className="text-gray-400 text-sm mt-1">{item.description}</p>
                    <Badge variant="outline" className="border-gray-600 text-gray-300 mt-2">
                      {item.category}
                    </Badge>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeItem(item.id)}
                    className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>

                <div className="flex items-center justify-between mt-4">
                  <div className="flex items-center gap-3">
                    <span className="text-gray-400">Quantity:</span>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="h-8 w-8 p-0 border-gray-600 text-gray-300 hover:bg-gray-700"
                      >
                        <Minus className="w-3 h-3" />
                      </Button>
                      <span className="text-white font-medium w-8 text-center">{item.quantity}</span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="h-8 w-8 p-0 border-gray-600 text-gray-300 hover:bg-gray-700"
                      >
                        <Plus className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-400">
                      {formatPrice(item.price)} each
                    </div>
                    <div className="text-lg font-bold text-white">
                      {formatPrice(item.price * item.quantity)}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <Card className="bg-gray-800 border-gray-700 sticky top-6">
            <CardHeader>
              <CardTitle className="text-white">Order Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Item count */}
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Items ({cartItems.length})</span>
                <span className="text-white">{formatPrice(calculateSubtotal())}</span>
              </div>

              {/* Tax */}
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Network fees (5%)</span>
                <span className="text-white">{formatPrice(calculateTax(calculateSubtotal()))}</span>
              </div>

              <Separator className="bg-gray-700" />

              {/* Total */}
              <div className="flex justify-between">
                <span className="text-lg font-semibold text-white">Total</span>
                <span className="text-lg font-bold text-white">{formatPrice(calculateTotal())}</span>
              </div>

              {/* Payment Methods */}
              <div className="space-y-3 pt-4">
                <div className="text-sm font-medium text-gray-300 mb-2">Payment Methods:</div>
                <div className="flex items-center gap-2 p-2 border border-gray-600 rounded-lg bg-gray-700/50">
                  <Bitcoin className="w-5 h-5 text-orange-400" />
                  <span className="text-white text-sm">Bitcoin (BTC)</span>
                </div>
              </div>

              {/* Status Messages */}
              {checkoutStatus === 'success' && (
                <div className="flex items-center gap-2 p-3 bg-green-900/30 border border-green-700 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-green-400 text-sm">Payment successful! Thank you for your purchase.</span>
                </div>
              )}

              {checkoutStatus === 'error' && (
                <div className="flex items-center gap-2 p-3 bg-red-900/30 border border-red-700 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-red-400" />
                  <span className="text-red-400 text-sm">Payment failed. Please try again.</span>
                </div>
              )}

              {/* Checkout Button */}
              <Button 
                onClick={handleCheckout}
                disabled={loading || cartItems.length === 0}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Processing...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <CreditCard className="w-4 h-4" />
                    Proceed to Checkout
                  </div>
                )}
              </Button>

              {/* Security Note */}
              <div className="text-xs text-gray-500 text-center pt-2">
                🔒 Secure cryptocurrency payments
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ShoppingCartComponent;