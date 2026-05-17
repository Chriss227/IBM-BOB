import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';
import * as api from '../api';

// Mock the API module
vi.mock('../api', () => ({
  analyzeRepo: vi.fn(),
  ApiError: class ApiError extends Error {
    constructor(message, status, detail) {
      super(message);
      this.name = 'ApiError';
      this.status = status;
      this.detail = detail;
    }
  }
}));

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render the input form', () => {
    render(<App />);
    
    expect(screen.getByPlaceholderText(/github repository url/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument();
  });

  it('should show loading state during analysis', async () => {
    const user = userEvent.setup();
    
    // Mock a slow API call
    api.analyzeRepo.mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 100))
    );

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Should show loading state
    expect(screen.getByText(/analyzing/i)).toBeInTheDocument();
  });

  it('should display results after successful analysis', async () => {
    const user = userEvent.setup();
    
    const mockResult = {
      architecture_mermaid: 'graph LR\n    A[Frontend] --> B[Backend]',
      flows: [
        {
          name: 'User Authentication',
          description: 'How users log in',
          steps: ['Submit credentials', 'Validate', 'Return token'],
          files: ['auth.js', 'user.js']
        }
      ],
      guide: '## 1. What does this project do?\n\nTest project',
      repository_url: 'https://github.com/test/repo',
      files_analyzed: 42
    };

    api.analyzeRepo.mockResolvedValueOnce(mockResult);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Wait for results to appear
    await waitFor(() => {
      expect(screen.getByText(/analysis complete/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/analyzed 42 files/i)).toBeInTheDocument();
    expect(screen.getByText('User Authentication')).toBeInTheDocument();
  });

  it('should display error message on API failure', async () => {
    const user = userEvent.setup();
    
    const mockError = new api.ApiError(
      'Repository not found',
      404,
      'The repository does not exist'
    );

    api.analyzeRepo.mockRejectedValueOnce(mockError);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/nonexistent');
    await user.click(button);

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/analysis failed/i)).toBeInTheDocument();
    });

    expect(screen.getByText('Repository not found')).toBeInTheDocument();
  });

  it('should display network error with troubleshooting tips', async () => {
    const user = userEvent.setup();
    
    const mockError = new api.ApiError(
      'Cannot connect to backend server',
      0,
      'Network error'
    );

    api.analyzeRepo.mockRejectedValueOnce(mockError);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/cannot connect to backend server/i)).toBeInTheDocument();
    });

    // Should show troubleshooting tips for network errors
    expect(screen.getByText(/troubleshooting tips/i)).toBeInTheDocument();
    expect(screen.getByText(/make sure the backend server is running/i)).toBeInTheDocument();
  });

  it('should allow resetting to analyze another repository', async () => {
    const user = userEvent.setup();
    
    const mockResult = {
      architecture_mermaid: 'graph LR\n    A --> B',
      flows: [{
        name: 'Test Flow',
        description: 'Test',
        steps: ['Step 1'],
        files: ['file.js']
      }],
      guide: '## Guide',
      repository_url: 'https://github.com/test/repo',
      files_analyzed: 10
    };

    api.analyzeRepo.mockResolvedValueOnce(mockResult);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText(/analysis complete/i)).toBeInTheDocument();
    });

    // Click reset button
    const resetButton = screen.getByRole('button', { name: /analyze another repository/i });
    await user.click(resetButton);

    // Results should be cleared
    expect(screen.queryByText(/analysis complete/i)).not.toBeInTheDocument();
    expect(screen.getByPlaceholderText(/github repository url/i)).toBeInTheDocument();
  });

  it('should clear error when starting new analysis', async () => {
    const user = userEvent.setup();
    
    // First request fails
    const mockError = new api.ApiError('Error', 500, 'Server error');
    api.analyzeRepo.mockRejectedValueOnce(mockError);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Wait for error
    await waitFor(() => {
      expect(screen.getByText(/analysis failed/i)).toBeInTheDocument();
    });

    // Second request succeeds
    const mockResult = {
      architecture_mermaid: 'graph LR\n    A --> B',
      flows: [{
        name: 'Test',
        description: 'Test',
        steps: ['Step'],
        files: ['file.js']
      }],
      guide: '## Guide',
      repository_url: 'https://github.com/test/repo2',
      files_analyzed: 5
    };
    api.analyzeRepo.mockResolvedValueOnce(mockResult);

    // Clear input and try again
    await user.clear(input);
    await user.type(input, 'https://github.com/test/repo2');
    await user.click(button);

    // Error should be cleared and results shown
    await waitFor(() => {
      expect(screen.queryByText(/analysis failed/i)).not.toBeInTheDocument();
      expect(screen.getByText(/analysis complete/i)).toBeInTheDocument();
    });
  });

  it('should handle unexpected errors gracefully', async () => {
    const user = userEvent.setup();
    
    // Throw a non-ApiError
    api.analyzeRepo.mockRejectedValueOnce(new Error('Unexpected error'));

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/test/repo');
    await user.click(button);

    // Should show generic error message
    await waitFor(() => {
      expect(screen.getByText(/an unexpected error occurred/i)).toBeInTheDocument();
    });
  });

  it('should display repository link in success message', async () => {
    const user = userEvent.setup();
    
    const mockResult = {
      architecture_mermaid: 'graph LR\n    A --> B',
      flows: [{
        name: 'Test',
        description: 'Test',
        steps: ['Step'],
        files: ['file.js']
      }],
      guide: '## Guide',
      repository_url: 'https://github.com/octocat/Hello-World',
      files_analyzed: 15
    };

    api.analyzeRepo.mockResolvedValueOnce(mockResult);

    render(<App />);
    
    const input = screen.getByPlaceholderText(/github repository url/i);
    const button = screen.getByRole('button', { name: /analyze/i });

    await user.type(input, 'https://github.com/octocat/Hello-World');
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByText(/analysis complete/i)).toBeInTheDocument();
    });

    // Should show repository name as link
    const repoLink = screen.getByRole('link', { name: /octocat\/Hello-World/i });
    expect(repoLink).toHaveAttribute('href', 'https://github.com/octocat/Hello-World');
    expect(repoLink).toHaveAttribute('target', '_blank');
  });
});

// Made with Bob
