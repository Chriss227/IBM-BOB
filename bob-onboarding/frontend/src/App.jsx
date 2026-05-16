import { useState } from 'react';
import RepoInput from './components/RepoInput';
import ArchDiagram from './components/ArchDiagram';
import FlowCards from './components/FlowCards';
import GuidePanel from './components/GuidePanel';
import { analyzeRepo, ApiError } from './api';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (url) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeRepo(url);
      setResult(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError({
          message: err.message,
          detail: err.detail,
          status: err.status
        });
      } else {
        setError({
          message: 'An unexpected error occurred',
          detail: err.message
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header with input */}
        <RepoInput onSubmit={handleAnalyze} loading={loading} />

        {/* Error display */}
        {error && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-6 w-6 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3 flex-1">
                  <h3 className="text-lg font-medium text-red-800">
                    Analysis Failed
                  </h3>
                  <p className="mt-2 text-sm text-red-700">
                    {error.message}
                  </p>
                  {error.detail && error.detail !== error.message && (
                    <p className="mt-1 text-xs text-red-600">
                      Details: {error.detail}
                    </p>
                  )}
                  {error.status === 0 && (
                    <div className="mt-4 text-sm text-red-700">
                      <p className="font-medium">Troubleshooting tips:</p>
                      <ul className="list-disc list-inside mt-2 space-y-1">
                        <li>Make sure the backend server is running on port 8000</li>
                        <li>Check that you've set up the .env file with Bob API credentials</li>
                        <li>Verify your network connection</li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results display */}
        {result && (
          <div className="space-y-8 animate-fade-in">
            {/* Success banner */}
            <div className="max-w-4xl mx-auto">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-green-800">
                      Analysis complete! Analyzed {result.files_analyzed} files from{' '}
                      <a 
                        href={result.repository_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="underline hover:text-green-900"
                      >
                        {result.repository_url.replace('https://github.com/', '')}
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Architecture diagram */}
            <div className="max-w-6xl mx-auto">
              <ArchDiagram mermaid={result.architecture_mermaid} />
            </div>

            {/* Flow cards */}
            <div className="max-w-6xl mx-auto">
              <FlowCards flows={result.flows} />
            </div>

            {/* Onboarding guide */}
            <div className="max-w-4xl mx-auto">
              <GuidePanel guide={result.guide} />
            </div>

            {/* Footer with actions */}
            <div className="max-w-4xl mx-auto">
              <div className="card bg-gradient-to-r from-bob-blue to-blue-600 text-white">
                <div className="text-center">
                  <h3 className="text-xl font-bold mb-2">
                    Ready to contribute? 🚀
                  </h3>
                  <p className="text-blue-100 mb-4">
                    You now have everything you need to start working on this project!
                  </p>
                  <button
                    onClick={() => {
                      setResult(null);
                      setError(null);
                    }}
                    className="bg-white text-bob-blue px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                  >
                    Analyze Another Repository
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 pt-8">
          <p>
            Powered by{' '}
            <span className="font-semibold text-bob-blue">IBM Bob AI</span>
            {' '}• Built for the IBM Bob Hackathon
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;

// Made with Bob
