import { beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';
import i18n from '../i18n';
import * as api from '../api';

vi.mock('../api', () => ({
  analyzeRepo: vi.fn(),
  ApiError: class ApiError extends Error {
    constructor(message, status, detail) {
      super(message);
      this.name = 'ApiError';
      this.status = status;
      this.detail = detail;
    }
  },
}));

vi.mock('mermaid', () => ({
  default: {
    initialize: vi.fn(),
    parse: vi.fn().mockResolvedValue(true),
    render: vi.fn().mockResolvedValue({
      svg: '<svg viewBox="0 0 100 100"><text>Diagram</text></svg>',
    }),
  },
}));

const result = {
  architecture_mermaid: 'flowchart LR\nA[Frontend] --> B[API]',
  flows: [{
    name: 'Authentication',
    description: 'Handles sign in',
    steps: ['Submit credentials'],
    files: ['auth.js'],
  }],
  guide: '## Start here\n\nRun the project.',
  repository_url: 'https://github.com/test/repo',
  files_analyzed: 42,
  language: 'en',
};

describe('Repo Accelerate app', () => {
  beforeEach(async () => {
    vi.clearAllMocks();
    localStorage.clear();
    await i18n.changeLanguage('en');
  });

  it('renders the rebranded analyzer', () => {
    render(<App />);
    expect(screen.getByText('Repo Accelerate')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /analyze repository/i })).toBeInTheDocument();
  });

  it('switches the complete interface language and persists it', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole('button', { name: 'ES' }));
    expect(await screen.findByRole('button', { name: /analizar repositorio/i })).toBeInTheDocument();
    expect(localStorage.getItem('repoAccelerateLanguage')).toBe('es');
    expect(document.documentElement.lang).toBe('es');
  });

  it('sends the active language and renders the tabbed workspace', async () => {
    const user = userEvent.setup();
    api.analyzeRepo.mockResolvedValueOnce(result);
    render(<App />);

    await user.type(
      screen.getByPlaceholderText(/github.com\/username\/repository/i),
      'https://github.com/test/repo',
    );
    await user.click(screen.getByRole('button', { name: /analyze repository/i }));

    await waitFor(() => expect(api.analyzeRepo).toHaveBeenCalledWith(
      'https://github.com/test/repo',
      'en',
    ));
    expect(await screen.findByText(/42 files analyzed/i)).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /architecture/i })).toHaveAttribute('aria-selected', 'true');

    await user.click(screen.getByRole('tab', { name: /key flows/i }));
    expect(screen.getByText('Authentication')).toBeInTheDocument();
  });

  it('preserves results and offers regeneration after a language change', async () => {
    const user = userEvent.setup();
    api.analyzeRepo.mockResolvedValueOnce(result);
    render(<App />);

    await user.type(screen.getByPlaceholderText(/github/i), 'https://github.com/test/repo');
    await user.click(screen.getByRole('button', { name: /analyze repository/i }));
    expect(await screen.findByText(/42 files analyzed/i)).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'ES' }));
    expect(screen.getByText(/Estos resultados fueron generados en inglés/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Analizar nuevamente en español/i })).toBeInTheDocument();
  });
});
