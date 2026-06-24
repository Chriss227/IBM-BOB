// Use VITE_API_URL in production. Local development defaults to the FastAPI port.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Custom error class for API errors.
 */
export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

/**
 * @param {string} url - GitHub repository URL
 * @param {'en'|'es'} language - Requested response language
 * @returns {Promise<Object>} Analysis results with architecture, flows, and guide
 * @throws {ApiError} If the request fails
 */
export async function analyzeRepo(url, language = 'en') {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url, language }),
    });

    // Parse response
    const data = await response.json();

    // Handle errors
    if (!response.ok) {
      const errorMessage = data.detail || data.error || 'Unknown error occurred';
      throw new ApiError(
        errorMessage,
        response.status,
        data.detail
      );
    }

    return data;
  } catch (error) {
    // Network errors or JSON parsing errors
    if (error instanceof ApiError) {
      throw error;
    }

    // Handle network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new ApiError(
        `Cannot connect to backend server at ${API_BASE_URL}. Configure VITE_API_URL in Vercel or start the local backend.`,
        0,
        'Network error'
      );
    }

    // Handle other errors
    throw new ApiError(
      error.message || 'An unexpected error occurred',
      0,
      'Unknown error'
    );
  }
}

/**
 * Check backend health status.
 * 
 * @returns {Promise<Object>} Health status
 * @throws {ApiError} If the request fails
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new ApiError('Health check failed', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      `Cannot connect to backend server at ${API_BASE_URL}`,
      0,
      'Network error'
    );
  }
}
