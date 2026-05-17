import { describe, it, expect, beforeEach, vi } from 'vitest';
import { analyzeRepo, checkHealth, ApiError } from '../api';

describe('API Client', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    global.fetch = vi.fn();
  });

  describe('analyzeRepo', () => {
    it('should successfully analyze a repository', async () => {
      const mockData = {
        architecture_mermaid: 'graph LR\n    A --> B',
        flows: [
          {
            name: 'Test Flow',
            description: 'Test description',
            steps: ['Step 1', 'Step 2'],
            files: ['file1.js', 'file2.js']
          }
        ],
        guide: '## Guide\nTest guide content',
        repository_url: 'https://github.com/test/repo',
        files_analyzed: 42
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockData
      });

      const result = await analyzeRepo('https://github.com/test/repo');

      expect(result).toEqual(mockData);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/analyze',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: 'https://github.com/test/repo' })
        })
      );
    });

    it('should throw ApiError on 400 error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid repository URL' })
      });

      await expect(analyzeRepo('invalid-url')).rejects.toThrow(ApiError);
      await expect(analyzeRepo('invalid-url')).rejects.toThrow('Invalid repository URL');
    });

    it('should throw ApiError on 500 error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Internal server error' })
      });

      await expect(analyzeRepo('https://github.com/test/repo')).rejects.toThrow(ApiError);
    });

    it('should throw ApiError with status 0 on network error', async () => {
      global.fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

      try {
        await analyzeRepo('https://github.com/test/repo');
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.status).toBe(0);
        expect(error.message).toContain('Cannot connect to backend server');
      }
    });

    it('should handle error response with error field', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 422,
        json: async () => ({ error: 'Validation error' })
      });

      try {
        await analyzeRepo('https://github.com/test/repo');
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.message).toBe('Validation error');
        expect(error.status).toBe(422);
      }
    });

    it('should handle unknown error format', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({})
      });

      try {
        await analyzeRepo('https://github.com/test/repo');
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.message).toBe('Unknown error occurred');
      }
    });
  });

  describe('checkHealth', () => {
    it('should successfully check health', async () => {
      const mockHealth = {
        status: 'ok',
        version: '1.0.0'
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockHealth
      });

      const result = await checkHealth();

      expect(result).toEqual(mockHealth);
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/health');
    });

    it('should throw ApiError on health check failure', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 503
      });

      try {
        await checkHealth();
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.message).toBe('Health check failed');
        expect(error.status).toBe(503);
      }
    });

    it('should throw ApiError on network error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      try {
        await checkHealth();
        expect.fail('Should have thrown an error');
      } catch (error) {
        expect(error).toBeInstanceOf(ApiError);
        expect(error.message).toBe('Cannot connect to backend server');
        expect(error.status).toBe(0);
      }
    });
  });

  describe('ApiError', () => {
    it('should create ApiError with all properties', () => {
      const error = new ApiError('Test message', 400, 'Test detail');

      expect(error).toBeInstanceOf(Error);
      expect(error).toBeInstanceOf(ApiError);
      expect(error.name).toBe('ApiError');
      expect(error.message).toBe('Test message');
      expect(error.status).toBe(400);
      expect(error.detail).toBe('Test detail');
    });

    it('should be throwable', () => {
      expect(() => {
        throw new ApiError('Test error', 500, 'Detail');
      }).toThrow(ApiError);
    });
  });
});

// Made with Bob
