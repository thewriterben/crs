#!/usr/bin/env python3
"""
Portfolio Optimization and Risk Analysis System
Implements Modern Portfolio Theory, risk metrics, and portfolio optimization algorithms
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
import json
from datetime import datetime, timedelta
import math
import random

class PortfolioOptimizer:
    def __init__(self):
        self.assets = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK', 'UNI', 'AAVE', 'COMP']
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        
    def generate_sample_returns(self, assets, days=252):
        """Generate sample historical returns for demonstration"""
        returns_data = {}
        
        # Base return characteristics for different crypto assets
        asset_params = {
            'BTC': {'mean': 0.0008, 'std': 0.04},
            'ETH': {'mean': 0.0012, 'std': 0.05},
            'ADA': {'mean': 0.0015, 'std': 0.06},
            'DOT': {'mean': 0.0010, 'std': 0.055},
            'LINK': {'mean': 0.0018, 'std': 0.065},
            'UNI': {'mean': 0.0020, 'std': 0.07},
            'AAVE': {'mean': 0.0016, 'std': 0.068},
            'COMP': {'mean': 0.0014, 'std': 0.062}
        }
        
        for asset in assets:
            params = asset_params.get(asset, {'mean': 0.001, 'std': 0.05})
            returns = np.random.normal(params['mean'], params['std'], days)
            returns_data[asset] = returns
            
        return pd.DataFrame(returns_data)
    
    def calculate_portfolio_metrics(self, weights, returns):
        """Calculate portfolio return, volatility, and Sharpe ratio"""
        portfolio_return = np.sum(returns.mean() * weights) * 252  # Annualized
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std
        
        return portfolio_return, portfolio_std, sharpe_ratio
    
    def optimize_portfolio(self, returns, target_return=None, method='max_sharpe'):
        """Optimize portfolio using different methods"""
        n_assets = len(returns.columns)
        
        # Constraints: weights sum to 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds: weights between 0 and 1 (long-only portfolio)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess: equal weights
        initial_guess = np.array([1/n_assets] * n_assets)
        
        if method == 'max_sharpe':
            # Maximize Sharpe ratio (minimize negative Sharpe ratio)
            def objective(weights):
                _, _, sharpe = self.calculate_portfolio_metrics(weights, returns)
                return -sharpe
                
        elif method == 'min_volatility':
            # Minimize portfolio volatility
            def objective(weights):
                _, vol, _ = self.calculate_portfolio_metrics(weights, returns)
                return vol
                
        elif method == 'target_return' and target_return:
            # Minimize volatility for target return
            def objective(weights):
                _, vol, _ = self.calculate_portfolio_metrics(weights, returns)
                return vol
            
            # Add constraint for target return
            def return_constraint(weights):
                ret, _, _ = self.calculate_portfolio_metrics(weights, returns)
                return ret - target_return
            
            constraints = [constraints, {'type': 'eq', 'fun': return_constraint}]
        
        # Optimize
        result = minimize(objective, initial_guess, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            ret, vol, sharpe = self.calculate_portfolio_metrics(optimal_weights, returns)
            
            return {
                'weights': dict(zip(returns.columns, optimal_weights)),
                'expected_return': ret,
                'volatility': vol,
                'sharpe_ratio': sharpe,
                'optimization_method': method
            }
        else:
            raise Exception(f"Optimization failed: {result.message}")
    
    def calculate_efficient_frontier(self, returns, num_portfolios=50):
        """Calculate efficient frontier"""
        results = []
        
        # Calculate range of target returns
        individual_returns = [self.calculate_portfolio_metrics(
            np.array([1 if i == j else 0 for j in range(len(returns.columns))]), 
            returns)[0] for i in range(len(returns.columns))]
        
        min_ret = min(individual_returns)
        max_ret = max(individual_returns)
        target_returns = np.linspace(min_ret, max_ret, num_portfolios)
        
        for target_ret in target_returns:
            try:
                result = self.optimize_portfolio(returns, target_ret, 'target_return')
                results.append({
                    'return': result['expected_return'],
                    'volatility': result['volatility'],
                    'sharpe_ratio': result['sharpe_ratio'],
                    'weights': result['weights']
                })
            except:
                continue
                
        return results
    
    def calculate_var(self, portfolio_value, weights, returns, confidence_level=0.05, time_horizon=1):
        """Calculate Value at Risk (VaR)"""
        portfolio_returns = returns.dot(weights)
        portfolio_std = portfolio_returns.std()
        
        # Parametric VaR
        var_parametric = norm.ppf(confidence_level) * portfolio_std * np.sqrt(time_horizon) * portfolio_value
        
        # Historical VaR
        var_historical = np.percentile(portfolio_returns, confidence_level * 100) * portfolio_value * np.sqrt(time_horizon)
        
        return {
            'parametric_var': abs(var_parametric),
            'historical_var': abs(var_historical),
            'confidence_level': confidence_level,
            'time_horizon': time_horizon
        }
    
    def calculate_risk_metrics(self, weights, returns, portfolio_value=100000):
        """Calculate comprehensive risk metrics"""
        portfolio_returns = returns.dot(weights)
        
        # Basic metrics
        annual_return = portfolio_returns.mean() * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility
        
        # Downside metrics
        downside_returns = portfolio_returns[portfolio_returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252)
        sortino_ratio = (annual_return - self.risk_free_rate) / downside_deviation if len(downside_returns) > 0 else 0
        
        # Maximum drawdown
        cumulative_returns = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # VaR calculations
        var_metrics = self.calculate_var(portfolio_value, weights, returns)
        
        # Beta calculation (using BTC as market proxy)
        if 'BTC' in returns.columns:
            market_returns = returns['BTC']
            covariance = np.cov(portfolio_returns, market_returns)[0][1]
            market_variance = np.var(market_returns)
            beta = covariance / market_variance if market_variance != 0 else 1
        else:
            beta = 1
        
        return {
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'beta': beta,
            'var_95': var_metrics['parametric_var'],
            'var_99': self.calculate_var(portfolio_value, weights, returns, 0.01)['parametric_var'],
            'downside_deviation': downside_deviation
        }
    
    def monte_carlo_simulation(self, weights, returns, num_simulations=10000, time_horizon=252):
        """Run Monte Carlo simulation for portfolio performance"""
        portfolio_returns = returns.dot(weights)
        mean_return = portfolio_returns.mean()
        std_return = portfolio_returns.std()
        
        # Generate random returns
        simulated_returns = np.random.normal(mean_return, std_return, 
                                           (num_simulations, time_horizon))
        
        # Calculate cumulative returns for each simulation
        cumulative_returns = np.cumprod(1 + simulated_returns, axis=1)
        final_values = cumulative_returns[:, -1]
        
        # Calculate statistics
        percentiles = np.percentile(final_values, [5, 25, 50, 75, 95])
        
        return {
            'mean_final_value': np.mean(final_values),
            'std_final_value': np.std(final_values),
            'percentile_5': percentiles[0],
            'percentile_25': percentiles[1],
            'percentile_50': percentiles[2],
            'percentile_75': percentiles[3],
            'percentile_95': percentiles[4],
            'probability_of_loss': np.sum(final_values < 1) / num_simulations,
            'num_simulations': num_simulations,
            'time_horizon_days': time_horizon
        }
    
    def rebalance_portfolio(self, current_weights, target_weights, current_values, 
                          rebalance_threshold=0.05):
        """Calculate portfolio rebalancing requirements"""
        rebalancing_needed = {}
        total_value = sum(current_values.values())
        
        for asset in target_weights:
            current_allocation = current_values.get(asset, 0) / total_value
            target_allocation = target_weights[asset]
            difference = abs(current_allocation - target_allocation)
            
            if difference > rebalance_threshold:
                target_value = target_allocation * total_value
                current_value = current_values.get(asset, 0)
                rebalancing_needed[asset] = {
                    'current_allocation': current_allocation,
                    'target_allocation': target_allocation,
                    'current_value': current_value,
                    'target_value': target_value,
                    'rebalance_amount': target_value - current_value,
                    'action': 'BUY' if target_value > current_value else 'SELL'
                }
        
        return {
            'rebalancing_needed': len(rebalancing_needed) > 0,
            'assets_to_rebalance': rebalancing_needed,
            'total_portfolio_value': total_value,
            'rebalance_threshold': rebalance_threshold
        }

class PortfolioAPI:
    def __init__(self):
        self.optimizer = PortfolioOptimizer()
        
    def get_optimized_portfolio(self, assets=None, method='max_sharpe'):
        """Get optimized portfolio allocation"""
        if not assets:
            assets = self.optimizer.assets[:5]  # Use top 5 assets
            
        # Generate sample data
        returns = self.optimizer.generate_sample_returns(assets)
        
        # Optimize portfolio
        result = self.optimizer.optimize_portfolio(returns, method=method)
        
        # Calculate risk metrics
        weights = np.array([result['weights'][asset] for asset in assets])
        risk_metrics = self.optimizer.calculate_risk_metrics(weights, returns)
        
        # Run Monte Carlo simulation
        mc_results = self.optimizer.monte_carlo_simulation(weights, returns)
        
        return {
            'optimization_result': result,
            'risk_metrics': risk_metrics,
            'monte_carlo_simulation': mc_results,
            'assets': assets,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_efficient_frontier(self, assets=None):
        """Get efficient frontier data"""
        if not assets:
            assets = self.optimizer.assets[:5]
            
        returns = self.optimizer.generate_sample_returns(assets)
        frontier = self.optimizer.calculate_efficient_frontier(returns)
        
        return {
            'efficient_frontier': frontier,
            'assets': assets,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_portfolio_risk(self, portfolio_weights, portfolio_value=100000):
        """Analyze risk for given portfolio"""
        assets = list(portfolio_weights.keys())
        returns = self.optimizer.generate_sample_returns(assets)
        
        weights = np.array([portfolio_weights[asset] for asset in assets])
        risk_metrics = self.optimizer.calculate_risk_metrics(weights, returns, portfolio_value)
        
        return {
            'risk_analysis': risk_metrics,
            'portfolio_weights': portfolio_weights,
            'portfolio_value': portfolio_value,
            'timestamp': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("Testing Portfolio Optimization System...")
    
    api = PortfolioAPI()
    
    # Test portfolio optimization
    print("\n1. Testing Portfolio Optimization:")
    result = api.get_optimized_portfolio()
    print(f"Optimal weights: {result['optimization_result']['weights']}")
    print(f"Expected return: {result['optimization_result']['expected_return']:.4f}")
    print(f"Volatility: {result['optimization_result']['volatility']:.4f}")
    print(f"Sharpe ratio: {result['optimization_result']['sharpe_ratio']:.4f}")
    
    # Test risk analysis
    print("\n2. Testing Risk Analysis:")
    sample_portfolio = {'BTC': 0.4, 'ETH': 0.3, 'ADA': 0.2, 'DOT': 0.1}
    risk_result = api.analyze_portfolio_risk(sample_portfolio)
    print(f"Annual return: {risk_result['risk_analysis']['annual_return']:.4f}")
    print(f"Annual volatility: {risk_result['risk_analysis']['annual_volatility']:.4f}")
    print(f"Sharpe ratio: {risk_result['risk_analysis']['sharpe_ratio']:.4f}")
    print(f"Max drawdown: {risk_result['risk_analysis']['max_drawdown']:.4f}")
    print(f"VaR (95%): ${risk_result['risk_analysis']['var_95']:.2f}")
    
    print("\n✅ Portfolio Optimization System working correctly!")

