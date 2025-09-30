import { useState } from 'react'
import { Search, ShoppingCart, User, Globe, LogIn, UserPlus, Bitcoin, Zap, Shield } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import './App.css'

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('default')
  const [selectedCoin, setSelectedCoin] = useState('all')
  const [minPrice, setMinPrice] = useState(1)
  const [maxPrice, setMaxPrice] = useState(100000)
  const [condition, setCondition] = useState('all')

  const cryptoCoins = [
    { name: 'DGB', count: 10, color: 'bg-blue-500' },
    { name: 'SOL', count: 7, color: 'bg-purple-500' },
    { name: 'DADDY', count: 2, color: 'bg-pink-500' },
    { name: 'XMR', count: 1, color: 'bg-orange-500' },
    { name: 'BTC', count: 6, color: 'bg-yellow-500' },
    { name: 'USDT', count: 1, color: 'bg-green-500' },
    { name: 'ETH', count: 2, color: 'bg-indigo-500' }
  ]

  const products = [
    {
      id: 1,
      title: 'The DigiDollar Strategy Manual (Supporter Edition)',
      price: 25.00,
      coin: 'DGB',
      image: 'https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=400&h=300&fit=crop',
      description: 'This paid listing is optional for supporters. The file is identical. A field manual to cryptocurrency strategy and investment approaches.'
    },
    {
      id: 2,
      title: 'Anyone Hardware Router',
      price: 499.00,
      coin: 'DGB',
      image: 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop',
      description: 'The Anyone Router is the device to protect your entire internet connection, by routing over the secure network infrastructure.'
    },
    {
      id: 3,
      title: 'Red Pill?',
      price: 31.00,
      coin: 'SOL',
      image: 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop',
      description: 'You take the red pill—you stay in Wonderland, and I show you how deep the rabbit hole goes. A philosophical journey into crypto.'
    }
  ]

  const navigationItems = [
    { name: 'HOME', color: 'bg-teal-500', active: false },
    { name: 'SHOP', color: 'bg-pink-500', active: true },
    { name: 'STORES', color: 'bg-purple-500', active: false },
    { name: 'CONTACT', color: 'bg-orange-500', active: false },
    { name: 'ACCOUNT', color: 'bg-green-500', active: false },
    { name: 'DONATE', color: 'bg-yellow-500', active: false }
  ]

  const getCoinColor = (coinName) => {
    const coin = cryptoCoins.find(c => c.name === coinName)
    return coin ? coin.color : 'bg-gray-500'
  }

  return (
    <div className="min-h-screen crypto-bg text-white">
      {/* Header */}
      <header className="bg-slate-800/90 backdrop-blur-sm border-b border-slate-700/50 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Badge className="bg-green-600 text-white hover:bg-green-700 transition-colors">
                <Globe className="w-3 h-3 mr-1" />
                GLOBAL
              </Badge>
              <div className="flex space-x-2">
                <Button variant="outline" size="sm" className="text-white border-slate-600 hover:border-slate-500 nav-button">
                  <UserPlus className="w-4 h-4 mr-1" />
                  REGISTER
                </Button>
                <Button variant="outline" size="sm" className="text-white border-slate-600 hover:border-slate-500 nav-button">
                  <LogIn className="w-4 h-4 mr-1" />
                  LOGIN
                </Button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" className="text-white hover:bg-slate-700 nav-button">
                <User className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="sm" className="text-white hover:bg-slate-700 nav-button relative">
                <ShoppingCart className="w-4 h-4" />
                <Badge className="absolute -top-2 -right-2 bg-red-500 text-xs min-w-[1.25rem] h-5 flex items-center justify-center">
                  2
                </Badge>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-slate-700/90 backdrop-blur-sm border-b border-slate-600/50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between py-3">
            <h1 className="text-2xl font-bold text-purple-400 flex items-center gap-2">
              <Bitcoin className="w-6 h-6" />
              Crypto Corner Shop
            </h1>
            <div className="flex space-x-1">
              {navigationItems.map((item) => (
                <Button
                  key={item.name}
                  variant={item.active ? "default" : "ghost"}
                  size="sm"
                  className={`${item.active ? item.color : 'bg-transparent hover:bg-slate-600'} text-white nav-button transition-all duration-200`}
                >
                  {item.name}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="crypto-hero py-16 relative">
        <div className="crypto-symbols">
          <Bitcoin />
          <Zap />
          <Shield />
          <Bitcoin />
        </div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <h2 className="text-5xl font-bold mb-4 animate-fade-in-up">Shop</h2>
          <p className="text-xl text-slate-300 animate-fade-in-up" style={{animationDelay: '0.2s'}}>
            Discover amazing crypto products
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-1/4 animate-fade-in-up" style={{animationDelay: '0.3s'}}>
            <div className="space-y-6">
              {/* Products By Coins */}
              <Card className="sidebar-card">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Bitcoin className="w-4 h-4" />
                    Products By Coins
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {cryptoCoins.map((coin) => (
                      <div key={coin.name} className="flex items-center justify-between hover:bg-slate-700/50 p-2 rounded transition-colors">
                        <Badge className={`${coin.color} text-white coin-badge`}>
                          {coin.name}
                        </Badge>
                        <span className="text-slate-400">({coin.count})</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Price Range */}
              <Card className="sidebar-card">
                <CardHeader>
                  <CardTitle className="text-white">Price Range</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-slate-400 min-w-[40px]">Min: $</span>
                      <Input
                        type="number"
                        value={minPrice}
                        onChange={(e) => setMinPrice(e.target.value)}
                        className="bg-slate-700/50 border-slate-600 text-white focus:border-yellow-500 transition-colors"
                      />
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-slate-400 min-w-[40px]">Max: $</span>
                      <Input
                        type="number"
                        value={maxPrice}
                        onChange={(e) => setMaxPrice(e.target.value)}
                        className="bg-slate-700/50 border-slate-600 text-white focus:border-yellow-500 transition-colors"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Condition */}
              <Card className="sidebar-card">
                <CardHeader>
                  <CardTitle className="text-white">Condition</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {['All', 'New', 'Used', 'Refurbished'].map((conditionOption) => (
                      <label key={conditionOption} className="flex items-center space-x-2 cursor-pointer hover:bg-slate-700/50 p-2 rounded transition-colors">
                        <input 
                          type="radio" 
                          name="condition" 
                          value={conditionOption.toLowerCase()}
                          checked={condition === conditionOption.toLowerCase()}
                          onChange={(e) => setCondition(e.target.value)}
                          className="condition-radio text-yellow-500 focus:ring-yellow-500" 
                        />
                        <span className="text-slate-300">{conditionOption}</span>
                      </label>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </aside>

          {/* Main Content */}
          <main className="lg:w-3/4 animate-fade-in-up" style={{animationDelay: '0.4s'}}>
            <div className="space-y-6">
              {/* Shop Now Header */}
              <h3 className="text-2xl font-bold text-white flex items-center gap-2">
                <Zap className="w-6 h-6 text-yellow-500" />
                Shop Now
              </h3>

              {/* Search and Sort */}
              <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
                <div className="relative flex-1 max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                  <Input
                    type="text"
                    placeholder="Search Products"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 bg-slate-800/50 border-slate-600 text-white search-glow transition-all duration-200"
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <span className="text-slate-400">Sorting:</span>
                  <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger className="w-48 bg-slate-800/50 border-slate-600 text-white hover:border-slate-500 transition-colors">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-800 border-slate-600">
                      <SelectItem value="default">Default</SelectItem>
                      <SelectItem value="newest">Newest</SelectItem>
                      <SelectItem value="price-low">Price: Low to High</SelectItem>
                      <SelectItem value="price-high">Price: High to Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Products Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 product-grid">
                {products.map((product) => (
                  <Card key={product.id} className="product-card group">
                    <CardHeader className="p-0">
                      <div className="relative overflow-hidden rounded-t-lg">
                        <img
                          src={product.image}
                          alt={product.title}
                          className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                          onError={(e) => {
                            e.target.src = 'https://via.placeholder.com/400x300/1e293b/64748b?text=Product+Image'
                          }}
                        />
                        <Badge className={`absolute top-2 left-2 ${getCoinColor(product.coin)} text-white coin-badge`}>
                          {product.coin}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="p-4">
                      <CardTitle className="text-white text-lg mb-2 line-clamp-2 group-hover:text-yellow-400 transition-colors">
                        {product.title}
                      </CardTitle>
                      <CardDescription className="text-slate-400 mb-4 line-clamp-3">
                        {product.description}
                      </CardDescription>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold price-text">
                          ${product.price.toFixed(2)} USD
                        </span>
                        <Button className="add-to-cart-btn">
                          Add to Cart
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </main>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-slate-800/90 backdrop-blur-sm border-t border-slate-700/50 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="animate-fade-in-up" style={{animationDelay: '0.6s'}}>
              <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-yellow-500" />
                About us!
              </h4>
              <p className="text-slate-400 mb-4">
                At Crypto Corner Shop, we empower sellers and buyers with cryptocurrency freedom, 
                enabling anyone to open an online shop, list products, and accept crypto payments — no bank needed.
              </p>
              <Button className="bg-yellow-600 hover:bg-yellow-700 text-black font-semibold transition-all duration-200 hover:scale-105">
                Sign Up
              </Button>
            </div>
            <div className="animate-fade-in-up" style={{animationDelay: '0.7s'}}>
              <h4 className="text-lg font-bold text-white mb-4">Contact</h4>
              <div className="space-y-2 text-slate-400">
                <p className="hover:text-yellow-400 transition-colors cursor-pointer">
                  Email: info@cryptocornershop.com
                </p>
                <p className="hover:text-yellow-400 transition-colors cursor-pointer">
                  Phone: +1 (415) 371-9275
                </p>
              </div>
            </div>
            <div className="text-slate-400 animate-fade-in-up" style={{animationDelay: '0.8s'}}>
              <p className="mb-2">Crypto Corner Shop, All right reserved.</p>
              <p className="text-yellow-400 hover:text-yellow-300 transition-colors cursor-pointer">
                Developed By MySkyPower
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
