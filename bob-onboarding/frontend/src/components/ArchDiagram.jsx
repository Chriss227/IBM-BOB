import { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

// Initialize Mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'ui-sans-serif, system-ui, sans-serif',
});

/**
 * ArchDiagram component for rendering Mermaid architecture diagrams.
 * 
 * @param {Object} props
 * @param {string} props.mermaid - Mermaid diagram code
 */
export default function ArchDiagram({ mermaid: mermaidCode }) {
  const containerRef = useRef(null);
  const [error, setError] = useState(null);
  const [isRendering, setIsRendering] = useState(true);

  useEffect(() => {
    if (!mermaidCode || !containerRef.current) {
      return;
    }

    const renderDiagram = async () => {
      setIsRendering(true);
      setError(null);

      try {
        // Clear previous content
        containerRef.current.innerHTML = '';

        // Validate that it looks like Mermaid code
        if (!mermaidCode.trim().startsWith('graph')) {
          throw new Error('Invalid Mermaid diagram format');
        }

        // Generate unique ID for this diagram
        const id = `mermaid-${Date.now()}`;

        // Render the diagram
        const { svg } = await mermaid.render(id, mermaidCode);
        
        // Insert the SVG
        containerRef.current.innerHTML = svg;
        setIsRendering(false);
      } catch (err) {
        console.error('Mermaid rendering error:', err);
        setError('Could not render architecture diagram. The diagram format may be invalid.');
        setIsRendering(false);
      }
    };

    renderDiagram();
  }, [mermaidCode]);

  if (!mermaidCode) {
    return null;
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
        <svg className="w-6 h-6 mr-2 text-bob-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        Architecture Overview
      </h2>

      {isRendering && (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <svg className="animate-spin h-8 w-8 text-bob-blue mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-gray-600">Rendering diagram...</p>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Diagram Rendering Issue
              </h3>
              <p className="mt-1 text-sm text-yellow-700">
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {!isRendering && !error && (
        <div 
          ref={containerRef}
          className="flex justify-center items-center overflow-x-auto py-4"
          style={{ minHeight: '200px' }}
        />
      )}

      <div className="mt-4 pt-4 border-t border-gray-200">
        <details className="group">
          <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-bob-blue flex items-center">
            <svg className="w-4 h-4 mr-1 transform group-open:rotate-90 transition-transform" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
            View Mermaid Code
          </summary>
          <pre className="mt-2 p-3 bg-gray-50 rounded text-xs overflow-x-auto">
            <code>{mermaidCode}</code>
          </pre>
        </details>
      </div>
    </div>
  );
}

// Made with Bob
