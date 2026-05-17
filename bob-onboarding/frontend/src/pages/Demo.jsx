import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Demo = () => {
  const [selectedRepo, setSelectedRepo] = useState(null);

  const demoRepos = [
    {
      id: 1,
      name: 'FastAPI',
      url: 'https://github.com/tiangolo/fastapi',
      description: 'Modern, fast web framework for building APIs with Python',
      language: 'Python',
      stars: '70k+',
      complexity: 'Medium',
      analysisTime: '45s',
      highlights: [
        'Clean architecture with dependency injection',
        'Async/await patterns throughout',
        'Comprehensive test coverage'
      ]
    },
    {
      id: 2,
      name: 'Express.js',
      url: 'https://github.com/expressjs/express',
      description: 'Fast, unopinionated, minimalist web framework for Node.js',
      language: 'JavaScript',
      stars: '63k+',
      complexity: 'Low',
      analysisTime: '30s',
      highlights: [
        'Middleware-based architecture',
        'Simple routing system',
        'Extensive ecosystem'
      ]
    },
    {
      id: 3,
      name: 'Flask',
      url: 'https://github.com/pallets/flask',
      description: 'Lightweight WSGI web application framework',
      language: 'Python',
      stars: '66k+',
      complexity: 'Low',
      analysisTime: '35s',
      highlights: [
        'Microframework design',
        'Jinja2 templating',
        'Built-in development server'
      ]
    },
    {
      id: 4,
      name: 'Django',
      url: 'https://github.com/django/django',
      description: 'High-level Python web framework',
      language: 'Python',
      stars: '76k+',
      complexity: 'High',
      analysisTime: '90s',
      highlights: [
        'Full-featured ORM',
        'Admin interface',
        'Security features built-in'
      ]
    }
  ];

  const features = [
    {
      icon: '🏗️',
      title: 'Architecture Visualization',
      description: 'Automatic generation of Mermaid diagrams showing system structure and component relationships',
      demo: 'See how Bob identifies modules, services, and their dependencies'
    },
    {
      icon: '🔄',
      title: 'Key Flow Analysis',
      description: 'Identifies the 3 most important workflows in your codebase with step-by-step breakdowns',
      demo: 'Watch Bob trace request flows, data pipelines, and business logic'
    },
    {
      icon: '📚',
      title: 'Onboarding Guide',
      description: 'Complete markdown guide with setup instructions, important files, and contribution tips',
      demo: 'Get a personalized guide tailored to the repository structure'
    },
    {
      icon: '⚡',
      title: 'Lightning Fast',
      description: 'Analysis completes in 30-90 seconds depending on repository size',
      demo: 'No more spending days understanding a new codebase'
    }
  ];

  const useCases = [
    {
      title: 'New Team Members',
      description: 'Reduce onboarding time from days to minutes',
      icon: '👥'
    },
    {
      title: 'Code Reviews',
      description: 'Quickly understand PR context and impact',
      icon: '🔍'
    },
    {
      title: 'Technical Debt',
      description: 'Identify architectural patterns and improvement areas',
      icon: '🛠️'
    },
    {
      title: 'Documentation',
      description: 'Auto-generate up-to-date architecture docs',
      icon: '📖'
    }
  ];

  const steps = [
    {
      number: '1',
      title: 'Paste GitHub URL',
      description: 'Enter any public GitHub repository URL',
      icon: '🔗'
    },
    {
      number: '2',
      title: 'Bob Analyzes',
      description: 'AI reads and understands the codebase',
      icon: '🤖'
    },
    {
      number: '3',
      title: 'Get Insights',
      description: 'Receive architecture, flows, and guide',
      icon: '📊'
    },
    {
      number: '4',
      title: 'Start Coding',
      description: 'Jump into development immediately',
      icon: '💻'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 opacity-10"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              🤖 Bob Onboarding Accelerator
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Understand any GitHub repository in under 5 minutes using IBM Bob AI
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/"
                className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
              >
                Try Live Demo →
              </Link>
              <a
                href="https://github.com/yourusername/bob-onboarding"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-4 bg-white text-gray-800 rounded-lg font-semibold hover:bg-gray-50 transition-colors shadow-lg hover:shadow-xl border-2 border-gray-200"
              >
                View on GitHub
              </a>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600">30-90s</div>
              <div className="text-gray-600 mt-2">Analysis Time</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600">3</div>
              <div className="text-gray-600 mt-2">Key Flows</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600">100%</div>
              <div className="text-gray-600 mt-2">Automated</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-orange-600">5min</div>
              <div className="text-gray-600 mt-2">To Understand</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
          Powerful Features
        </h2>
        <p className="text-xl text-gray-600 text-center mb-12 max-w-2xl mx-auto">
          Everything you need to understand a codebase quickly
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100"
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 mb-4">{feature.description}</p>
              <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
                <p className="text-sm text-blue-900 font-medium">
                  {feature.demo}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Demo Repositories */}
      <div className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
            Try These Sample Repositories
          </h2>
          <p className="text-xl text-gray-600 text-center mb-12">
            Click any repository to see Bob in action
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            {demoRepos.map((repo) => (
              <div
                key={repo.id}
                className={`bg-white rounded-xl p-6 border-2 transition-all cursor-pointer ${
                  selectedRepo?.id === repo.id
                    ? 'border-blue-500 shadow-xl'
                    : 'border-gray-200 hover:border-blue-300 shadow-lg hover:shadow-xl'
                }`}
                onClick={() => setSelectedRepo(repo)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {repo.name}
                    </h3>
                    <p className="text-gray-600 text-sm">{repo.description}</p>
                  </div>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    {repo.language}
                  </span>
                </div>

                <div className="flex gap-4 mb-4 text-sm text-gray-600">
                  <span>⭐ {repo.stars}</span>
                  <span>📊 {repo.complexity}</span>
                  <span>⏱️ {repo.analysisTime}</span>
                </div>

                <div className="space-y-2">
                  {repo.highlights.map((highlight, idx) => (
                    <div key={idx} className="flex items-start gap-2">
                      <span className="text-green-500 mt-1">✓</span>
                      <span className="text-sm text-gray-700">{highlight}</span>
                    </div>
                  ))}
                </div>

                <Link
                  to={`/?url=${encodeURIComponent(repo.url)}`}
                  className="mt-4 block w-full text-center px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Analyze This Repository →
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Use Cases */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
          Perfect For
        </h2>
        <p className="text-xl text-gray-600 text-center mb-12">
          Multiple scenarios where fast codebase understanding matters
        </p>

        <div className="grid md:grid-cols-4 gap-6">
          {useCases.map((useCase, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow text-center border border-gray-100"
            >
              <div className="text-5xl mb-4">{useCase.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {useCase.title}
              </h3>
              <p className="text-gray-600 text-sm">{useCase.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-white mb-12">
            How It Works
          </h2>

          <div className="grid md:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                <div className="bg-white rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <span className="text-4xl">{step.icon}</span>
                </div>
                <div className="bg-white bg-opacity-20 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">{step.number}</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
                <p className="text-blue-100">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-center shadow-2xl">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Accelerate Your Onboarding?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Start analyzing repositories now and save hours of onboarding time
          </p>
          <Link
            to="/"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
          >
            Get Started Free →
          </Link>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-400 mb-4">
              Built with ❤️ for the IBM Bob Hackathon
            </p>
            <div className="flex justify-center gap-6">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                Documentation
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                GitHub
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                API
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Demo;

// Made with Bob
