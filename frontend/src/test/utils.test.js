/**
 * Tests for API utility functions
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mockApiResponse, mockFetch } from './utils'

describe('API Utilities', () => {
  let originalFetch

  beforeEach(() => {
    originalFetch = global.fetch
  })

  afterEach(() => {
    global.fetch = originalFetch
  })

  describe('mockApiResponse', () => {
    it('creates successful response', async () => {
      const data = { message: 'success' }
      const response = mockApiResponse(data, 200)

      expect(response.ok).toBe(true)
      expect(response.status).toBe(200)
      expect(await response.json()).toEqual(data)
    })

    it('creates error response', async () => {
      const data = { error: 'not found' }
      const response = mockApiResponse(data, 404)

      expect(response.ok).toBe(false)
      expect(response.status).toBe(404)
      expect(await response.json()).toEqual(data)
    })
  })

  describe('mockFetch', () => {
    it('returns mocked response', async () => {
      const data = { test: 'data' }
      const response = mockApiResponse(data)
      const fetch = mockFetch([response])

      global.fetch = fetch

      const result = await fetch('/api/test')
      const json = await result.json()

      expect(fetch).toHaveBeenCalledTimes(1)
      expect(json).toEqual(data)
    })

    it('handles multiple calls', async () => {
      const responses = [
        mockApiResponse({ page: 1 }),
        mockApiResponse({ page: 2 }),
      ]
      const fetch = mockFetch(responses)

      global.fetch = fetch

      const result1 = await fetch('/api/page1')
      const result2 = await fetch('/api/page2')

      expect(await result1.json()).toEqual({ page: 1 })
      expect(await result2.json()).toEqual({ page: 2 })
    })
  })
})
