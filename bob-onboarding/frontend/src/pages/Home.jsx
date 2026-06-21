import { useCallback, useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  GitBranch,
  Languages,
  Network,
  Route,
  ScrollText,
} from 'lucide-react';
import RepoInput from '../components/RepoInput';
import ArchDiagram from '../components/ArchDiagram';
import FlowCards from '../components/FlowCards';
import GuidePanel from '../components/GuidePanel';
import { analyzeRepo, ApiError } from '../api';
import { normalizeLanguage } from '../i18n';

const TABS = [
  { id: 'architecture', icon: Network, content: (result) => <ArchDiagram mermaid={result.architecture_mermaid} /> },
  { id: 'flows', icon: Route, content: (result) => <FlowCards flows={result.flows} /> },
  { id: 'guide', icon: ScrollText, content: (result) => <GuidePanel guide={result.guide} /> },
];

function Home() {
  const { t, i18n } = useTranslation();
  const [searchParams] = useSearchParams();
  const [result, setResult] = useState(null);
  const [lastUrl, setLastUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('architecture');
  const autoAnalyzedUrlRef = useRef('');
  const language = normalizeLanguage(i18n.resolvedLanguage);

  const handleAnalyze = useCallback(async (url, requestedLanguage = language) => {
    setLoading(true);
    setError(null);
    setLastUrl(url);

    try {
      const data = await analyzeRepo(url, requestedLanguage);
      setResult(data);
      setActiveTab('architecture');
    } catch (requestError) {
      if (requestError instanceof ApiError) {
        setError({
          message: requestError.message,
          detail: requestError.detail,
          status: requestError.status,
        });
      } else {
        setError({
          message: t('errors.unexpected'),
          detail: requestError.message,
        });
      }
    } finally {
      setLoading(false);
    }
  }, [language, t]);

  useEffect(() => {
    const urlParam = searchParams.get('url');
    if (urlParam && autoAnalyzedUrlRef.current !== urlParam && !result && !loading) {
      autoAnalyzedUrlRef.current = urlParam;
      handleAnalyze(urlParam);
    }
  }, [handleAnalyze, loading, result, searchParams]);

  const resultLanguage = normalizeLanguage(result?.language);
  const languageChanged = Boolean(result && resultLanguage !== language);
  const repositoryName = result?.repository_url?.replace('https://github.com/', '').replace(/\/$/, '');
  const activePanel = TABS.find((tab) => tab.id === activeTab);

  const handleTabKeyDown = (event, currentIndex) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = currentIndex;
    if (event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % TABS.length;
    if (event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + TABS.length) % TABS.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = TABS.length - 1;
    setActiveTab(TABS[nextIndex].id);
    document.getElementById(`tab-${TABS[nextIndex].id}`)?.focus();
  };

  return (
    <main>
      <div className="app-container py-10 sm:py-14">
        <RepoInput onSubmit={handleAnalyze} loading={loading} />

        {error ? (
          <section className="error-panel" role="alert">
            <AlertCircle size={22} />
            <div>
              <h2>{t('errors.title')}</h2>
              <p>{error.message}</p>
              {error.detail && error.detail !== error.message ? (
                <p className="error-detail">
                  {t('errors.details')}: {error.detail}
                </p>
              ) : null}
              {error.status === 0 ? (
                <div className="mt-4">
                  <strong>{t('errors.troubleshooting')}</strong>
                  <ul>
                    <li>{t('errors.backend')}</li>
                    <li>{t('errors.credentials')}</li>
                    <li>{t('errors.network')}</li>
                  </ul>
                </div>
              ) : null}
            </div>
          </section>
        ) : null}

        {result ? (
          <section className="results-shell animate-fade-in" aria-labelledby="results-title">
            <header className="result-summary">
              <div className="result-identity">
                <span className="result-icon">
                  <GitBranch size={20} />
                </span>
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="success-label">
                      <CheckCircle2 size={14} />
                      {t('results.complete')}
                    </span>
                    <span className="result-meta">{t('results.files', { count: result.files_analyzed })}</span>
                  </div>
                  <h2 id="results-title">
                    <a href={result.repository_url} target="_blank" rel="noopener noreferrer">
                      {repositoryName}
                    </a>
                  </h2>
                  <p>
                    {t('results.generatedIn', {
                      language: t(`languages.${resultLanguage}`),
                    })}
                  </p>
                </div>
              </div>

              <button
                type="button"
                className="secondary-button"
                onClick={() => {
                  setResult(null);
                  setError(null);
                }}
              >
                {t('results.another')}
                <ArrowRight size={16} />
              </button>
            </header>

            {languageChanged ? (
              <div className="language-notice" role="status">
                <Languages size={18} />
                <p>
                  {t('results.languageWarning', {
                    language: t(`languages.${resultLanguage}`),
                  })}
                </p>
                <button type="button" onClick={() => handleAnalyze(lastUrl, language)} disabled={loading}>
                  {t('results.languageWarningAction', {
                    language: t(`languages.${language}`),
                  })}
                </button>
              </div>
            ) : null}

            <div className="workspace-tabs" role="tablist" aria-label={t('results.complete')}>
              {TABS.map((tab, index) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    id={`tab-${tab.id}`}
                    key={tab.id}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    aria-controls={`panel-${tab.id}`}
                    tabIndex={isActive ? 0 : -1}
                    className={isActive ? 'workspace-tab-active' : 'workspace-tab'}
                    onClick={() => setActiveTab(tab.id)}
                    onKeyDown={(event) => handleTabKeyDown(event, index)}
                  >
                    <Icon size={17} />
                    {t(`results.${tab.id}`)}
                  </button>
                );
              })}
            </div>

            <div
              id={`panel-${activeTab}`}
              role="tabpanel"
              aria-labelledby={`tab-${activeTab}`}
              className="workspace-panel"
            >
              {activePanel.content(result)}
            </div>
          </section>
        ) : null}

        <footer className="app-footer">
          <p>{t('footer.powered')}</p>
        </footer>
      </div>
    </main>
  );
}

export default Home;
