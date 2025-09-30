/**
 * Test utilities and helpers
 */
import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

/**
 * Render component with router
 */
export function renderWithRouter(ui, { route = '/' } = {}) {
  window.history.pushState({}, 'Test page', route)
  
  return render(ui, { wrapper: BrowserRouter })
}

/**
 * Mock API response
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
 * Mock fetch function
 */
export function mockFetch(responses = []) {
  let callCount = 0
  
  return vi.fn().mockImplementation(() => {
    const response = responses[callCount] || responses[responses.length - 1]
    callCount++
    return Promise.resolve(response)
  })
}

/**
 * Wait for async operations
 */
export function waitFor(callback, { timeout = 1000, interval = 50 } = {}) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now()
    
    const check = () => {
      try {
        callback()
        resolve()
      } catch (error) {
        if (Date.now() - startTime > timeout) {
          reject(error)
        } else {
          setTimeout(check, interval)
        }
      }
    }
    
    check()
  })
}
