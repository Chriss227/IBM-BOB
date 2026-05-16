import { useState } from 'react';

/**
 * RepoInput component for entering and validating GitHub repository URLs.
 * 
 * @param {Object} props
 * @param {Function} props.onSubmit - Callback function when form is submitted with valid URL
 * @param {boolean} props.loading - Whether analysis is in progress
 */
export default function RepoInput({ onSubmit, loading }) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const validateUrl = (urlString) => {
    if (!urlString.trim()) {
      return 'Please enter a repository URL';
    }

    if (!urlString.startsWith('https://github.com/')) {
      return 'URL must start with https://github.com/';
    }

    // Basic validation for GitHub URL format
    const urlPattern = /^https:\/\/github\.com\/[\w-]+\/[\w.-]+\/?$/;
    if (!urlPattern.test(urlString.trim())) {
      return 'Please enter a valid GitHub repository URL (e.g., https://github.com/user/repo)';
    }

    return null;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const validationError = validateUrl(url);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError('');
    onSubmit(url.trim());
  };

  const handleChange = (e) => {
    setUrl(e.target.value);
    // Clear error when user starts typing
    if (error) {
      setError('');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="card">
        <div className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🤖 Bob Onboarding Accelerator
          </h1>
          <p className="text-gray-600">
            Understand any GitHub repository in under 5 minutes using IBM Bob AI
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="repo-url" className="block text-sm font-medium text-gray-700 mb-2">
              GitHub Repository URL
            </label>
            <input
              id="repo-url"
              type="text"
              value={url}
              onChange={handleChange}
              placeholder="https://github.com/username/repository"
              className={`input-field ${error ? 'border-red-500 focus:ring-red-500' : ''}`}
              disabled={loading}
              autoFocus
            />
            {error && (
              <p className="mt-2 text-sm text-red-600 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {error}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Bob is reading the repository...
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Analyze with Bob
              </>
            )}
          </button>
        </form>

        {loading && (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-blue-400 animate-pulse-slow" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Analysis in progress
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <ul className="list-disc list-inside space-y-1">
                    <li>Cloning repository...</li>
                    <li>Reading code files...</li>
                    <li>Analyzing with Bob AI...</li>
                    <li>Generating documentation...</li>
                  </ul>
                </div>
                <p className="mt-2 text-xs text-blue-600">
                  This usually takes 30-60 seconds
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob
