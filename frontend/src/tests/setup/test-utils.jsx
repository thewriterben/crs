import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

/**
 * Custom render function that wraps components with necessary providers
 */
export function renderWithRouter(ui, options = {}) {
  return render(ui, {
    wrapper: ({ children }) => <BrowserRouter>{children}</BrowserRouter>,
    ...options,
  })
}

/**
 * Create mock API response
 */
export function mockApiResponse(data, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
    text: async () => JSON.stringify(data),
  }
}

/**
 * Wait for async operations
 */
export function waitForAsync() {
  return new Promise(resolve => setTimeout(resolve, 0))
}

/**
 * Mock localStorage
 */
export function mockLocalStorage() {
  let store = {}
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => {
      store[key] = value.toString()
    },
    removeItem: (key) => {
      delete store[key]
    },
    clear: () => {
      store = {}
    },
  }
}
