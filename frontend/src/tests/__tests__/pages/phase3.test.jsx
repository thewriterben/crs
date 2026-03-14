/**
 * Tests for Phase 3 frontend pages and API integration
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';

// Mock the API module
vi.mock('@/lib/api', () => ({
  api: {
    phase3: {
      ai: {
        lstmPredict: vi.fn(),
        transformerPredict: vi.fn(),
        ensemblePredict: vi.fn(),
        analyzeSentiment: vi.fn(),
      },
      defi: {
        getDexQuote: vi.fn(),
        executeSwap: vi.fn(),
        getFarmingOpportunities: vi.fn(),
        getFarmingPositions: vi.fn(),
        getStakingOptions: vi.fn(),
        getStakingPositions: vi.fn(),
        getLiquidityPools: vi.fn(),
        getLiquidityPositions: vi.fn(),
      },
      social: {
        getTopTraders: vi.fn(),
        followTrader: vi.fn(),
        getSignals: vi.fn(),
        getFeaturedPortfolios: vi.fn(),
      },
      portfolio: {
        analyzeRebalance: vi.fn(),
        generateRebalanceOrders: vi.fn(),
        assessRisk: vi.fn(),
        getDCASchedules: vi.fn(),
        createDCA: vi.fn(),
        getActiveStopLosses: vi.fn(),
        createStopLoss: vi.fn(),
      },
    },
    cfv: {
      getSupportedCurrencies: vi.fn(),
      createPayment: vi.fn(),
      getPaymentStatus: vi.fn(),
      getDiscounts: vi.fn(),
    },
  },
}));

// Import after mocking
import { api } from '@/lib/api';
import Trading from '@/pages/Trading';
import DeFi from '@/pages/DeFi';
import Social from '@/pages/Social';
import Portfolio from '@/pages/Portfolio';

const mockPredictionData = {
  symbol: 'BTC',
  predictions: [{ timestamp: Date.now(), price: 45000, confidence: 0.82 }],
  confidence: 0.82,
  trend: 'bullish',
  model: 'LSTM',
};

const mockSentimentData = {
  symbol: 'BTC',
  sentiment_score: 0.68,
  sentiment_label: 'BULLISH',
  confidence: 0.76,
  sources: { news: 0.72, social: 0.64, reddit: 0.68 },
};

const mockTradersData = {
  traders: [
    { id: 'trader_001', username: 'CryptoMaster', winRate: 0.72, avgReturn: 0.18, followers: 2547, verified: true },
    { id: 'trader_002', username: 'BullRunner', winRate: 0.68, avgReturn: 0.14, followers: 1832, verified: false },
  ],
};

const mockSignalsData = {
  signals: [
    { id: 'sig_1', symbol: 'BTC', action: 'BUY', strength: 0.74, confidence: 0.72, timestamp: Date.now() },
    { id: 'sig_2', symbol: 'ETH', action: 'HOLD', strength: 0.55, confidence: 0.65, timestamp: Date.now() },
  ],
};

const mockPortfoliosData = {
  portfolios: [
    { id: 'pf_1', name: 'DeFi Focus', owner: 'CryptoMaster', yearlyReturn: 0.452, riskLevel: 'high' },
  ],
};

const mockFarmingData = {
  pools: [
    { id: 'pool_1', protocol: 'Raydium', pair: 'SOL-USDC', apy: 68.5, tvl: 12500000 },
  ],
};

const mockStakingOptions = {
  options: [
    { token: 'ETH', minAmount: 0.1, apy: 5.5, lockPeriod: 0, protocol: 'Ethereum' },
  ],
};

const mockLiquidityPools = {
  pools: [
    { id: 'lp_1', name: 'ETH/USDT', protocol: 'Uniswap V3', fee: 0.003, tvl: 125000000 },
  ],
};

function renderWithRouter(component) {
  return render(<MemoryRouter>{component}</MemoryRouter>);
}

// ===== Trading Page Tests =====
describe('Trading Page', () => {
  beforeEach(() => {
    api.phase3.ai.lstmPredict.mockResolvedValue(mockPredictionData);
    api.phase3.ai.transformerPredict.mockResolvedValue({ ...mockPredictionData, model: 'Transformer' });
    api.phase3.ai.ensemblePredict.mockResolvedValue({ ...mockPredictionData, model: 'Ensemble' });
    api.phase3.ai.analyzeSentiment.mockResolvedValue(mockSentimentData);
    api.phase3.social.getTopTraders.mockResolvedValue(mockTradersData);
  });

  afterEach(() => { vi.clearAllMocks(); });

  it('renders the Trading page with title', () => {
    renderWithRouter(<Trading />);
    expect(screen.getByText('AI Trading')).toBeInTheDocument();
  });

  it('shows symbol selector buttons', () => {
    renderWithRouter(<Trading />);
    expect(screen.getByRole('button', { name: 'BTC' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'ETH' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'SOL' })).toBeInTheDocument();
  });

  it('shows prediction tab content by default', () => {
    renderWithRouter(<Trading />);
    expect(screen.getByText('Predictions')).toBeInTheDocument();
  });

  it('shows LSTM model label after predictions load', async () => {
    renderWithRouter(<Trading />);
    await waitFor(() => {
      expect(screen.getAllByText(/LSTM/i).length).toBeGreaterThan(0);
    });
  });

  it('shows sentiment analysis data after loading', async () => {
    renderWithRouter(<Trading />);
    const sentimentTab = screen.getByText('Sentiment');
    await userEvent.click(sentimentTab);
    await waitFor(() => {
      expect(api.phase3.ai.analyzeSentiment).toHaveBeenCalled();
    });
  });

  it('shows copy trading tab', async () => {
    renderWithRouter(<Trading />);
    const copyTab = screen.getByText('Copy Trade');
    await userEvent.click(copyTab);
    await waitFor(() => {
      expect(screen.getByText('Copy Trading — Top Bots & Traders')).toBeInTheDocument();
    });
  });

  it('loads top traders in copy trade tab', async () => {
    renderWithRouter(<Trading />);
    const copyTab = screen.getByText('Copy Trade');
    await userEvent.click(copyTab);
    await waitFor(() => {
      expect(screen.getByText('CryptoMaster')).toBeInTheDocument();
    });
  });
});

// ===== DeFi Page Tests =====
describe('DeFi Page', () => {
  beforeEach(() => {
    api.phase3.defi.getDexQuote.mockResolvedValue({
      quotes: [{ exchange: 'Uniswap', amountOut: 2796.25, priceImpact: 0.001, fee: 0.003 }],
      bestQuote: { exchange: 'Uniswap', amountOut: 2796.25 },
    });
    api.phase3.defi.getFarmingOpportunities.mockResolvedValue(mockFarmingData);
    api.phase3.defi.getFarmingPositions.mockResolvedValue({ positions: [] });
    api.phase3.defi.getStakingOptions.mockResolvedValue(mockStakingOptions);
    api.phase3.defi.getStakingPositions.mockResolvedValue({ positions: [] });
    api.phase3.defi.getLiquidityPools.mockResolvedValue(mockLiquidityPools);
    api.phase3.defi.getLiquidityPositions.mockResolvedValue({ positions: [] });
  });

  afterEach(() => { vi.clearAllMocks(); });

  it('renders the DeFi page with title', () => {
    renderWithRouter(<DeFi />);
    expect(screen.getByText('DeFi Features')).toBeInTheDocument();
  });

  it('shows DEX swap tab by default', () => {
    renderWithRouter(<DeFi />);
    expect(screen.getByText('DEX Aggregator')).toBeInTheDocument();
  });

  it('shows farming tab content', async () => {
    renderWithRouter(<DeFi />);
    const farmingTab = screen.getByText('Farming');
    await userEvent.click(farmingTab);
    await waitFor(() => {
      expect(screen.getByText('Yield Farming')).toBeInTheDocument();
    });
  });

  it('loads farming pools', async () => {
    renderWithRouter(<DeFi />);
    const farmingTab = screen.getByText('Farming');
    await userEvent.click(farmingTab);
    await waitFor(() => {
      expect(screen.getByText('SOL-USDC')).toBeInTheDocument();
    });
  });

  it('shows staking tab content', async () => {
    renderWithRouter(<DeFi />);
    const stakingTab = screen.getByRole('tab', { name: /Staking/i });
    await userEvent.click(stakingTab);
    await waitFor(() => {
      expect(screen.getByText('Stake tokens to earn rewards')).toBeInTheDocument();
      expect(screen.getByText('ETH')).toBeInTheDocument();
    });
  });

  it('shows liquidity pools tab', async () => {
    renderWithRouter(<DeFi />);
    const liquidityTab = screen.getByText('Liquidity');
    await userEvent.click(liquidityTab);
    await waitFor(() => {
      expect(screen.getByText('ETH/USDT')).toBeInTheDocument();
    });
  });
});

// ===== Social Page Tests =====
describe('Social Page', () => {
  beforeEach(() => {
    api.phase3.social.getTopTraders.mockResolvedValue(mockTradersData);
    api.phase3.social.getSignals.mockResolvedValue(mockSignalsData);
    api.phase3.social.getFeaturedPortfolios.mockResolvedValue(mockPortfoliosData);
    api.phase3.social.followTrader.mockResolvedValue({ success: true });
  });

  afterEach(() => { vi.clearAllMocks(); });

  it('renders the Social page with title', () => {
    renderWithRouter(<Social />);
    expect(screen.getByText('Social Trading')).toBeInTheDocument();
  });

  it('shows leaderboard by default', () => {
    renderWithRouter(<Social />);
    expect(screen.getByText('Top Traders Leaderboard')).toBeInTheDocument();
  });

  it('loads top traders', async () => {
    renderWithRouter(<Social />);
    await waitFor(() => {
      expect(screen.getByText('CryptoMaster')).toBeInTheDocument();
    });
  });

  it('shows verified badge for verified traders', async () => {
    renderWithRouter(<Social />);
    await waitFor(() => {
      expect(screen.getByText('✓')).toBeInTheDocument();
    });
  });

  it('loads trading signals', async () => {
    renderWithRouter(<Social />);
    const signalsTab = screen.getByText('Signals');
    await userEvent.click(signalsTab);
    await waitFor(() => {
      expect(screen.getByText('BUY')).toBeInTheDocument();
    });
  });

  it('loads featured portfolios', async () => {
    renderWithRouter(<Social />);
    const portfoliosTab = screen.getByText('Portfolios');
    await userEvent.click(portfoliosTab);
    await waitFor(() => {
      expect(screen.getByText('DeFi Focus')).toBeInTheDocument();
    });
  });

  it('shows copy trading setup form', async () => {
    renderWithRouter(<Social />);
    const copyTab = screen.getByText('Copy Trade');
    await userEvent.click(copyTab);
    expect(screen.getByText('Copy Trading Setup')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/e.g. trader_001/i)).toBeInTheDocument();
  });
});

// ===== Portfolio Page Tests =====
describe('Portfolio Page', () => {
  beforeEach(() => {
    api.phase3.portfolio.analyzeRebalance.mockResolvedValue({ drift: 0.2, needs_rebalancing: true });
    api.phase3.portfolio.assessRisk.mockResolvedValue({ metrics: { overall_risk: 'MEDIUM', volatility: 0.42, sharpe_ratio: 1.28, max_drawdown: -0.18, beta: 0.87, var_95: -0.06 } });
    api.phase3.portfolio.getDCASchedules.mockResolvedValue({ schedules: [] });
    api.phase3.portfolio.getActiveStopLosses.mockResolvedValue({ stops: [] });
  });

  afterEach(() => { vi.clearAllMocks(); });

  it('renders the Portfolio page', () => {
    renderWithRouter(<Portfolio />);
    expect(screen.getByText('Portfolio Management')).toBeInTheDocument();
  });

  it('shows stat cards', () => {
    renderWithRouter(<Portfolio />);
    expect(screen.getByText('Total Value')).toBeInTheDocument();
    expect(screen.getByText('24h Change')).toBeInTheDocument();
    expect(screen.getByText('Assets')).toBeInTheDocument();
  });

  it('shows rebalance tab by default', () => {
    renderWithRouter(<Portfolio />);
    expect(screen.getByText('Portfolio Rebalancing')).toBeInTheDocument();
  });

  it('loads risk assessment', async () => {
    renderWithRouter(<Portfolio />);
    const riskTab = screen.getByText('Risk');
    await userEvent.click(riskTab);
    await waitFor(() => {
      expect(screen.getByText('Risk Assessment')).toBeInTheDocument();
    });
  });

  it('shows DCA manager', async () => {
    renderWithRouter(<Portfolio />);
    const dcaTab = screen.getByText('DCA');
    await userEvent.click(dcaTab);
    expect(screen.getByText('DCA Schedule Manager')).toBeInTheDocument();
  });

  it('shows stop-loss controls', async () => {
    renderWithRouter(<Portfolio />);
    const stopTab = screen.getByText('Stop-Loss');
    await userEvent.click(stopTab);
    expect(screen.getByText('Stop-Loss Controls')).toBeInTheDocument();
  });

  it('shows "no active stop-loss" message when empty', async () => {
    renderWithRouter(<Portfolio />);
    const stopTab = screen.getByText('Stop-Loss');
    await userEvent.click(stopTab);
    await waitFor(() => {
      expect(screen.getByText('No active stop-loss orders')).toBeInTheDocument();
    });
  });
});

// ===== API Phase3 endpoint structure tests =====
describe('Phase 3 API structure', () => {
  it('api.phase3.ai has all required methods', () => {
    expect(typeof api.phase3.ai.lstmPredict).toBe('function');
    expect(typeof api.phase3.ai.transformerPredict).toBe('function');
    expect(typeof api.phase3.ai.ensemblePredict).toBe('function');
    expect(typeof api.phase3.ai.analyzeSentiment).toBe('function');
  });

  it('api.phase3.defi has all required methods', () => {
    expect(typeof api.phase3.defi.getDexQuote).toBe('function');
    expect(typeof api.phase3.defi.getFarmingOpportunities).toBe('function');
    expect(typeof api.phase3.defi.getStakingOptions).toBe('function');
    expect(typeof api.phase3.defi.getLiquidityPools).toBe('function');
  });

  it('api.phase3.social has all required methods', () => {
    expect(typeof api.phase3.social.getTopTraders).toBe('function');
    expect(typeof api.phase3.social.followTrader).toBe('function');
    expect(typeof api.phase3.social.getSignals).toBe('function');
    expect(typeof api.phase3.social.getFeaturedPortfolios).toBe('function');
  });

  it('api.phase3.portfolio has all required methods', () => {
    expect(typeof api.phase3.portfolio.analyzeRebalance).toBe('function');
    expect(typeof api.phase3.portfolio.assessRisk).toBe('function');
    expect(typeof api.phase3.portfolio.createDCA).toBe('function');
    expect(typeof api.phase3.portfolio.createStopLoss).toBe('function');
  });
});
