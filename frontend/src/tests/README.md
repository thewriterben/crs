# Frontend Tests

This directory contains the test suite for the CRS Cryptocurrency Marketplace frontend.

## Quick Start

```bash
# Run tests in watch mode
npm test

# Run tests once
npm run test:run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Test Structure

```
tests/
├── setup/
│   ├── test-setup.js          # Global test configuration
│   └── test-utils.jsx         # Custom render utilities
└── __tests__/
    ├── components/            # Component tests
    │   ├── ui/               # UI component tests
    │   ├── ai/               # AI component tests
    │   └── auth/             # Auth component tests
    ├── hooks/                # Custom hooks tests
    ├── contexts/             # Context tests
    └── utils/                # Utility function tests
```

## Current Test Coverage

- ✅ Button component (7 tests)
- ✅ Card component (6 tests)
- ✅ useMobile hook (4 tests)
- ✅ Utils (cn function) (7 tests)

**Total: 24 tests passing**

## Writing Tests

### Component Test Example

```javascript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MyComponent } from '@/components/MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const handleClick = vi.fn()
    render(<MyComponent onClick={handleClick} />)
    
    await userEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalled()
  })
})
```

### Hook Test Example

```javascript
import { renderHook, act } from '@testing-library/react'
import { useMyHook } from '@/hooks/useMyHook'

describe('useMyHook', () => {
  it('returns expected value', () => {
    const { result } = renderHook(() => useMyHook())
    expect(result.current).toBeDefined()
  })
})
```

## Test Utilities

### renderWithRouter

Custom render function that wraps components with BrowserRouter:

```javascript
import { renderWithRouter } from '@/tests/setup/test-utils'

renderWithRouter(<MyComponent />)
```

### mockApiResponse

Create mock API responses:

```javascript
import { mockApiResponse } from '@/tests/setup/test-utils'

const mockData = mockApiResponse({ data: 'value' }, 200)
```

## Best Practices

1. **Use Semantic Queries**: Prefer `getByRole`, `getByLabelText`, `getByText`
2. **Test User Behavior**: Focus on what users see and do
3. **Avoid Implementation Details**: Don't test internal state
4. **Keep Tests Isolated**: Each test should be independent
5. **Use userEvent**: Prefer `userEvent` over `fireEvent` for interactions

## Resources

- [Full Testing Documentation](../../docs/TESTING.md)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)

---

For more detailed information, see the [main testing documentation](../../docs/TESTING.md).
