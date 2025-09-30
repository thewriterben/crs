import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Input } from '@/components/ui/input.jsx';
import { api } from '@/lib/api.js';
import { 
  ShoppingCart, 
  Search, 
  Star, 
  Bitcoin, 
  Zap, 
  TrendingUp,
  Brain,
  Shield,
  Clock
} from 'lucide-react';

const ProductCatalog = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock product data - in real app this would come from API
  const mockProducts = [
    {
      id: 1,
      name: 'AI Trading Bot Premium',
      price: 0.001,
      currency: 'BTC',
      description: 'Advanced AI-powered trading bot with portfolio optimization and real-time market analysis',
      category: 'Trading Tools',
      rating: 4.8,
      features: ['24/7 Trading', 'Portfolio Optimization', 'Risk Management', 'Performance Analytics'],
      icon: Brain,
      popular: true
    },
    {
      id: 2,
      name: 'Market Analysis Pro',
      price: 0.0005,
      currency: 'BTC',
      description: 'Real-time market sentiment analysis and predictions using advanced ML algorithms',
      category: 'Analytics',
      rating: 4.6,
      features: ['Sentiment Analysis', 'Price Predictions', 'News Integration', 'Social Media Monitoring'],
      icon: TrendingUp,
      popular: false
    },
    {
      id: 3,
      name: 'Crypto Security Suite',
      price: 0.0003,
      currency: 'BTC',
      description: 'Comprehensive security tools for cryptocurrency wallets and transactions',
      category: 'Security',
      rating: 4.9,
      features: ['Wallet Security', 'Transaction Monitoring', 'Threat Detection', '2FA Integration'],
      icon: Shield,
      popular: false
    },
    {
      id: 4,
      name: 'Lightning Fast Executor',
      price: 0.0008,
      currency: 'BTC',
      description: 'High-speed trade execution engine with minimal latency for professional traders',
      category: 'Trading Tools',
      rating: 4.7,
      features: ['Ultra-Low Latency', 'Multi-Exchange Support', 'Order Types', 'Smart Routing'],
      icon: Zap,
      popular: true
    },
    {
      id: 5,
      name: 'DeFi Yield Optimizer',
      price: 0.0012,
      currency: 'BTC',
      description: 'Automated yield farming and liquidity provision optimization across DeFi protocols',
      category: 'DeFi',
      rating: 4.5,
      features: ['Yield Farming', 'Liquidity Optimization', 'Risk Assessment', 'Multi-Protocol Support'],
      icon: Clock,
      popular: false
    },
    {
      id: 6,
      name: 'Crypto Tax Calculator',
      price: 0.0002,
      currency: 'BTC',
      description: 'Automated cryptocurrency tax calculation and reporting for multiple jurisdictions',
      category: 'Utilities',
      rating: 4.4,
      features: ['Tax Calculations', 'Multi-Jurisdiction', 'Export Reports', 'Transaction History'],
      icon: Bitcoin,
      popular: false
    }
  ];

  useEffect(() => {
    // Load products from API
    const loadProducts = async () => {
      try {
        setLoading(true);
        const data = await api.marketplace.getProducts();
        const productsWithIcons = data.products.map(product => ({
          ...product,
          icon: getIconForCategory(product.category)
        }));
        setProducts(productsWithIcons);
        setFilteredProducts(productsWithIcons);
      } catch (error) {
        console.error('Error loading products:', error);
        // Fallback to mock data
        const productsWithIcons = mockProducts.map(product => ({
          ...product,
          icon: getIconForCategory(product.category)
        }));
        setProducts(productsWithIcons);
        setFilteredProducts(productsWithIcons);
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, []);

  const getIconForCategory = (category) => {
    const iconMap = {
      'Trading Tools': Brain,
      'Analytics': TrendingUp,
      'Security': Shield,
      'DeFi': Clock,
      'Utilities': Bitcoin
    };
    return iconMap[category] || Zap;
  };

  useEffect(() => {
    if (searchTerm) {
      const filtered = products.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.category.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredProducts(filtered);
    } else {
      setFilteredProducts(products);
    }
  }, [searchTerm, products]);

  const handleAddToCart = async (product) => {
    try {
      await api.marketplace.addToCart(product.id, 1);
      alert(`Added ${product.name} to cart!`);
    } catch (error) {
      console.error('Error adding to cart:', error);
      // Fallback to simple alert
      alert(`Added ${product.name} to cart!`);
    }
  };

  const formatPrice = (price, currency) => {
    return `${price} ${currency}`;
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star 
        key={i} 
        className={`w-4 h-4 ${i < Math.floor(rating) ? 'text-yellow-400 fill-current' : 'text-gray-400'}`} 
      />
    ));
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading products...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header and Search */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Crypto Marketplace</h1>
          <p className="text-gray-400">Discover AI-powered tools and services for cryptocurrency trading</p>
        </div>
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
          />
        </div>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.map((product) => {
          const IconComponent = product.icon;
          return (
            <Card key={product.id} className="bg-gray-800 border-gray-700 hover:border-gray-600 transition-colors">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-600 rounded-lg">
                      <IconComponent className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <CardTitle className="text-white text-lg">{product.name}</CardTitle>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex">{renderStars(product.rating)}</div>
                        <span className="text-sm text-gray-400">({product.rating})</span>
                      </div>
                    </div>
                  </div>
                  {product.popular && (
                    <Badge variant="secondary" className="bg-orange-600 text-white">
                      Popular
                    </Badge>
                  )}
                </div>
                <CardDescription className="text-gray-300 mt-2">
                  {product.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {/* Category and Price */}
                <div className="flex justify-between items-center">
                  <Badge variant="outline" className="border-gray-600 text-gray-300">
                    {product.category}
                  </Badge>
                  <div className="text-right">
                    <div className="text-xl font-bold text-white">
                      {formatPrice(product.price, product.currency)}
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-300 mb-2">Key Features:</h4>
                  <div className="flex flex-wrap gap-1">
                    {product.features.slice(0, 3).map((feature, index) => (
                      <Badge key={index} variant="outline" className="text-xs border-gray-600 text-gray-400">
                        {feature}
                      </Badge>
                    ))}
                    {product.features.length > 3 && (
                      <Badge variant="outline" className="text-xs border-gray-600 text-gray-400">
                        +{product.features.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Add to Cart Button */}
                <Button 
                  onClick={() => handleAddToCart(product)}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                  <ShoppingCart className="w-4 h-4 mr-2" />
                  Add to Cart
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* No Results */}
      {filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <Search className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No products found</h3>
          <p className="text-gray-400">Try adjusting your search terms or browse all categories</p>
        </div>
      )}
    </div>
  );
};

export default ProductCatalog;