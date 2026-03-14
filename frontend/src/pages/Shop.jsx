import React from 'react';
import ProductCatalog from '@/components/shop/ProductCatalog';
import ShoppingCart from '@/components/shop/ShoppingCart';

export default function Shop() {
  return (
    <div className="space-y-6">
      <ProductCatalog />
      <ShoppingCart />
    </div>
  );
}
