#!/usr/bin/env python3
"""
Phase 3 API Demo Script
Demonstrates key Phase 3 features
"""

import sys
sys.path.insert(0, 'backend')

from defi.defi_integration import DEXAggregator, YieldFarmingManager, StakingManager
from social.social_trading import CopyTradingSystem, TradingSignalsGenerator, PortfolioSharingSystem
from portfolio.portfolio_automation import PortfolioRebalancer, RiskManagementSystem, DollarCostAveragingSystem


def demo_defi_features():
    """Demonstrate DeFi integration features"""
    print("\n" + "="*60)
    print("1. DEFI INTEGRATION DEMO")
    print("="*60)
    
    # DEX Trading
    print("\n[DEX Aggregator]")
    dex = DEXAggregator()
    quotes = dex.get_quote('ETH', 'USDT', 1.0)
    print(f"Best quote for 1 ETH -> USDT:")
    print(f"  Exchange: {quotes[0].dex_name}")
    print(f"  Amount Out: {quotes[0].amount_out:.2f} USDT")
    print(f"  Price Impact: {quotes[0].price_impact:.4f}%")
    print(f"  Gas Estimate: {quotes[0].gas_estimate:.5f} ETH")
    
    # Yield Farming
    print("\n[Yield Farming]")
    farming = YieldFarmingManager()
    opportunities = farming.get_opportunities(min_apy=50)
    print(f"High-yield opportunities (>50% APY):")
    for opp in opportunities[:3]:
        print(f"  {opp['pool_name']}: {opp['apy']:.1f}% APY on {opp['protocol']}")
    
    # Staking
    print("\n[Staking]")
    staking = StakingManager()
    options = staking.get_staking_options()
    print(f"Available staking options:")
    for opt in options[:3]:
        print(f"  {opt['token']}: {opt['apy']:.1f}% APY ({opt['type']})")


def demo_social_trading():
    """Demonstrate social trading features"""
    print("\n" + "="*60)
    print("2. SOCIAL TRADING DEMO")
    print("="*60)
    
    # Top Traders
    print("\n[Top Traders]")
    copy_trading = CopyTradingSystem()
    traders = copy_trading.get_top_traders(limit=3)
    print("Top 3 traders to follow:")
    for trader in traders:
        print(f"  #{trader['rank']} {trader['username']}:")
        print(f"    Win Rate: {trader['win_rate']*100:.1f}%")
        print(f"    Avg Return: {trader['avg_return']*100:.1f}%")
        print(f"    Followers: {trader['total_followers']:,}")
        print(f"    Risk: {trader['risk_score']}")
    
    # Trading Signals
    print("\n[AI Trading Signals]")
    signals = TradingSignalsGenerator()
    all_signals = signals.get_signals()
    print(f"Active trading signals:")
    for signal in all_signals[:3]:
        print(f"  {signal['symbol']}: {signal['signal_type']}")
        print(f"    Strength: {signal['strength']:.0%}")
        print(f"    Confidence: {signal['confidence']:.0%}")
        print(f"    Target: ${signal['price_target']:,.2f}")
    
    # Featured Portfolios
    print("\n[Featured Portfolios]")
    sharing = PortfolioSharingSystem()
    portfolios = sharing.get_featured_portfolios(sort_by='return')
    print("Top performing portfolios:")
    for portfolio in portfolios[:2]:
        print(f"  {portfolio['owner']}:")
        print(f"    Value: ${portfolio['value']:,.0f}")
        print(f"    Yearly Return: {portfolio['return']:.1f}%")
        print(f"    Followers: {portfolio['followers']:,}")


def demo_portfolio_automation():
    """Demonstrate portfolio automation features"""
    print("\n" + "="*60)
    print("3. PORTFOLIO AUTOMATION DEMO")
    print("="*60)
    
    # Portfolio Rebalancing
    print("\n[Portfolio Rebalancing]")
    rebalancer = PortfolioRebalancer()
    current = {'BTC': 0.50, 'ETH': 0.30, 'USDT': 0.20}
    target = {'BTC': 0.40, 'ETH': 0.35, 'USDT': 0.25}
    analysis = rebalancer.analyze_portfolio(current, target)
    print(f"Portfolio drift analysis:")
    print(f"  Needs Rebalancing: {analysis['needs_rebalance']}")
    print(f"  Total Drift: {analysis['total_drift']:.2%}")
    for asset, info in analysis['drifts'].items():
        print(f"  {asset}: {info['current']:.1%} -> {info['target']:.1%} ({info['action']})")
    
    # Risk Management
    print("\n[Risk Management]")
    risk_mgr = RiskManagementSystem()
    position = risk_mgr.calculate_position_size(
        portfolio_value=100000,
        risk_per_trade=0.02,
        stop_loss_pct=0.05
    )
    print(f"Optimal position sizing:")
    print(f"  Portfolio Value: $100,000")
    print(f"  Risk Per Trade: 2%")
    print(f"  Stop Loss: 5%")
    print(f"  Recommended Position: ${position['recommended_position']:,.2f}")
    
    # DCA Strategy
    print("\n[Dollar-Cost Averaging]")
    dca = DollarCostAveragingSystem()
    schedule = dca.create_dca_schedule('demo_user', 'BTC', 500, 'weekly', 12)
    print(f"DCA Schedule Created:")
    print(f"  Asset: {schedule['asset']}")
    print(f"  Amount Per Period: ${schedule['amount_per_period']}")
    print(f"  Frequency: {schedule['frequency']}")
    print(f"  Duration: {schedule['duration_months']} months")
    print(f"  Total Investment: ${schedule['total_investment']:,.2f}")
    print(f"  Total Periods: {schedule['total_periods']}")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("PHASE 3 FEATURES DEMONSTRATION")
    print("Cryptons.com Cryptocurrency Marketplace")
    print("="*60)
    
    try:
        demo_defi_features()
        demo_social_trading()
        demo_portfolio_automation()
        
        print("\n" + "="*60)
        print("DEMO COMPLETE")
        print("="*60)
        print("\nAll Phase 3 features are operational!")
        print("\nTo explore more:")
        print("  - Start the API server: ./scripts/start_phase3_api.sh")
        print("  - Run tests: cd backend && python3 tests/test_phase3.py")
        print("  - View docs: docs/PHASE_3_IMPLEMENTATION.md")
        print()
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
