/**
 * FlowCards component for displaying key system flows in a responsive grid.
 * 
 * @param {Object} props
 * @param {Array} props.flows - Array of flow objects with name, description, steps, and files
 */
export default function FlowCards({ flows }) {
  if (!flows || flows.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 flex items-center">
        <svg className="w-6 h-6 mr-2 text-bob-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Key System Flows
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {flows.map((flow, index) => (
          <FlowCard key={index} flow={flow} index={index} />
        ))}
      </div>
    </div>
  );
}

/**
 * Individual flow card component.
 */
function FlowCard({ flow, index }) {
  const colors = [
    'bg-blue-50 border-blue-200',
    'bg-green-50 border-green-200',
    'bg-purple-50 border-purple-200',
  ];

  const badgeColors = [
    'bg-blue-100 text-blue-800',
    'bg-green-100 text-green-800',
    'bg-purple-100 text-purple-800',
  ];

  const colorClass = colors[index % colors.length];
  const badgeColor = badgeColors[index % badgeColors.length];

  return (
    <div className={`card ${colorClass} border-2 hover:shadow-lg transition-shadow duration-200`}>
      {/* Flow number badge */}
      <div className="flex items-start justify-between mb-3">
        <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full ${badgeColor} font-bold text-sm`}>
          {index + 1}
        </span>
      </div>

      {/* Flow name */}
      <h3 className="text-lg font-bold text-gray-900 mb-2">
        {flow.name}
      </h3>

      {/* Flow description */}
      <p className="text-sm text-gray-700 mb-4">
        {flow.description}
      </p>

      {/* Steps */}
      {flow.steps && flow.steps.length > 0 && (
        <div className="mb-4">
          <h4 className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
            Steps
          </h4>
          <ol className="space-y-2">
            {flow.steps.map((step, stepIndex) => (
              <li key={stepIndex} className="flex items-start text-sm text-gray-700">
                <span className="flex-shrink-0 w-5 h-5 rounded-full bg-white border-2 border-gray-300 flex items-center justify-center mr-2 mt-0.5">
                  <span className="text-xs font-medium text-gray-600">{stepIndex + 1}</span>
                </span>
                <span className="flex-1">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Related files */}
      {flow.files && flow.files.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-2">
            Related Files
          </h4>
          <div className="flex flex-wrap gap-2">
            {flow.files.map((file, fileIndex) => (
              <span
                key={fileIndex}
                className="inline-flex items-center px-2 py-1 rounded text-xs font-mono bg-white border border-gray-300 text-gray-700"
                title={file}
              >
                <svg className="w-3 h-3 mr-1 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                </svg>
                {file.length > 20 ? `...${file.slice(-20)}` : file}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Made with Bob
