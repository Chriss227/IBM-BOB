import { beforeEach, describe, expect, it, vi } from 'vitest';
import { analyzeRepo, checkHealth, ApiError } from '../api';

describe('API client', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('sends the selected language with an analysis request', async () => {
    const mockData = {
      architecture_mermaid: 'flowchart LR\nA --> B',
      flows: [],
      guide: '## Guide',
      repository_url: 'https://github.com/test/repo',
      files_analyzed: 2,
      language: 'es',
    };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockData,
    });

    await expect(analyzeRepo('https://github.com/test/repo', 'es')).resolves.toEqual(mockData);
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/analyze$/),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          url: 'https://github.com/test/repo',
          language: 'es',
        }),
      }),
    );
  });

  it('uses English as the backward-compatible language default', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({}),
    });

    await analyzeRepo('https://github.com/test/repo');
    expect(global.fetch.mock.calls[0][1].body).toBe(
      JSON.stringify({ url: 'https://github.com/test/repo', language: 'en' }),
    );
  });

  it('converts API and network failures to ApiError', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Invalid repository URL' }),
    });
    await expect(analyzeRepo('invalid')).rejects.toMatchObject({
      name: 'ApiError',
      status: 400,
      message: 'Invalid repository URL',
    });

    global.fetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));
    await expect(analyzeRepo('https://github.com/test/repo')).rejects.toBeInstanceOf(ApiError);
  });

  it('checks service health', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: 'ok', version: '3.0.0' }),
    });
    await expect(checkHealth()).resolves.toEqual({ status: 'ok', version: '3.0.0' });
  });
});
