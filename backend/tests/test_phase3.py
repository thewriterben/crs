#!/usr/bin/env python3
"""
Basic tests for Phase 3 features
"""

import sys
sys.path.insert(0, '..')

def test_defi_integration():
    """Test DeFi integration functionality"""
    from defi.defi_integration import DEXAggregator, YieldFarmingManager, StakingManager
    
    # Test DEX Aggregator
    dex = DEXAggregator()
    quotes = dex.get_quote('ETH', 'USDT', 1.0)
    assert len(quotes) > 0, "Should return at least one quote"
    assert quotes[0].token_in == 'ETH', "Token in should be ETH"
    assert quotes[0].token_out == 'USDT', "Token out should be USDT"
    print("✓ DEX Aggregator test passed")
    
    # Test Yield Farming
    farming = YieldFarmingManager()
    opportunities = farming.get_opportunities()
    assert len(opportunities) > 0, "Should have farming opportunities"
    assert 'apy' in opportunities[0], "Should have APY"
    print("✓ Yield Farming test passed")
    
    # Test Staking
    staking = StakingManager()
    options = staking.get_staking_options()
    assert len(options) > 0, "Should have staking options"
    print("✓ Staking Manager test passed")


def test_social_trading():
    """Test social trading functionality"""
    from social.social_trading import CopyTradingSystem, TradingSignalsGenerator
    
    # Test Copy Trading
    copy_system = CopyTradingSystem()
    traders = copy_system.get_top_traders(limit=5)
    assert len(traders) > 0, "Should return traders"
    assert 'username' in traders[0], "Should have username"
    print("✓ Copy Trading test passed")
    
    # Test Trading Signals
    signals = TradingSignalsGenerator()
    all_signals = signals.get_signals()
    assert len(all_signals) > 0, "Should have signals"
    print("✓ Trading Signals test passed")


def test_portfolio_automation():
    """Test portfolio automation functionality"""
    from portfolio.portfolio_automation import (
        PortfolioRebalancer, RiskManagementSystem, DollarCostAveragingSystem
    )
    
    # Test Rebalancer
    rebalancer = PortfolioRebalancer()
    analysis = rebalancer.analyze_portfolio(
        {'BTC': 0.45, 'ETH': 0.35, 'USDT': 0.20},
        {'BTC': 0.40, 'ETH': 0.30, 'USDT': 0.30}
    )
    assert 'needs_rebalance' in analysis, "Should return rebalance analysis"
    print("✓ Portfolio Rebalancer test passed")
    
    # Test Risk Management
    risk_mgr = RiskManagementSystem()
    position_size = risk_mgr.calculate_position_size(100000, 0.02, 0.05)
    assert 'recommended_position' in position_size, "Should calculate position size"
    print("✓ Risk Management test passed")
    
    # Test DCA
    dca = DollarCostAveragingSystem()
    schedule = dca.create_dca_schedule('user1', 'BTC', 100, 'weekly', 12)
    assert 'schedule_id' in schedule, "Should create DCA schedule"
    print("✓ DCA System test passed")


if __name__ == '__main__':
    print("Running Phase 3 Tests...")
    print()
    
    try:
        test_defi_integration()
        print()
        test_social_trading()
        print()
        test_portfolio_automation()
        print()
        print("=" * 50)
        print("All Phase 3 tests passed! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
