import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

/**
 * GuidePanel component for displaying the onboarding guide with markdown rendering.
 * 
 * @param {Object} props
 * @param {string} props.guide - Markdown content of the onboarding guide
 */
export default function GuidePanel({ guide }) {
  const [copied, setCopied] = useState(false);

  if (!guide) {
    return null;
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(guide);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <svg className="w-6 h-6 mr-2 text-bob-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Onboarding Guide
        </h2>

        <button
          onClick={handleCopy}
          className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-bob-blue transition-colors"
        >
          {copied ? (
            <>
              <svg className="w-4 h-4 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Copied!
            </>
          ) : (
            <>
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy Guide
            </>
          )}
        </button>
      </div>

      <div className="prose prose-sm max-w-none">
        <ReactMarkdown
          components={{
            // Customize heading styles
            h1: ({ node, ...props }) => (
              <h1 className="text-2xl font-bold text-gray-900 mt-6 mb-4 pb-2 border-b-2 border-gray-200" {...props} />
            ),
            h2: ({ node, ...props }) => (
              <h2 className="text-xl font-bold text-gray-900 mt-6 mb-3" {...props} />
            ),
            h3: ({ node, ...props }) => (
              <h3 className="text-lg font-semibold text-gray-900 mt-4 mb-2" {...props} />
            ),
            // Customize paragraph styles
            p: ({ node, ...props }) => (
              <p className="text-gray-700 mb-4 leading-relaxed" {...props} />
            ),
            // Customize list styles
            ul: ({ node, ...props }) => (
              <ul className="list-disc list-inside space-y-2 mb-4 text-gray-700" {...props} />
            ),
            ol: ({ node, ...props }) => (
              <ol className="list-decimal list-inside space-y-2 mb-4 text-gray-700" {...props} />
            ),
            li: ({ node, ...props }) => (
              <li className="ml-4" {...props} />
            ),
            // Customize code styles
            code: ({ node, inline, ...props }) => (
              inline ? (
                <code className="px-1.5 py-0.5 bg-gray-100 text-red-600 rounded text-sm font-mono" {...props} />
              ) : (
                <code className="block p-4 bg-gray-900 text-gray-100 rounded-lg overflow-x-auto text-sm font-mono" {...props} />
              )
            ),
            pre: ({ node, ...props }) => (
              <pre className="mb-4 rounded-lg overflow-hidden" {...props} />
            ),
            // Customize blockquote styles
            blockquote: ({ node, ...props }) => (
              <blockquote className="border-l-4 border-bob-blue pl-4 italic text-gray-600 my-4" {...props} />
            ),
            // Customize link styles
            a: ({ node, ...props }) => (
              <a className="text-bob-blue hover:text-bob-blue-hover underline" {...props} />
            ),
            // Customize strong/bold styles
            strong: ({ node, ...props }) => (
              <strong className="font-bold text-gray-900" {...props} />
            ),
          }}
        >
          {guide}
        </ReactMarkdown>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="flex items-start space-x-3 text-sm text-gray-600">
          <svg className="w-5 h-5 text-bob-blue flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <p>
            This guide was automatically generated by IBM Bob AI. While it provides a great starting point, 
            always verify critical information and consult the repository's official documentation.
          </p>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
