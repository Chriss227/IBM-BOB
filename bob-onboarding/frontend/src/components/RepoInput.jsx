import { useState } from 'react';
import { ArrowRight, GitBranch, LoaderCircle } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const GITHUB_REPOSITORY_PATTERN = /^https:\/\/github\.com\/[\w-]+\/[\w.-]+\/?$/;

export default function RepoInput({ onSubmit, loading }) {
  const { t } = useTranslation();
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const validateUrl = (value) => {
    const trimmedValue = value.trim();
    if (!trimmedValue) return t('input.required');
    if (!trimmedValue.startsWith('https://github.com/')) return t('input.githubOnly');
    if (!GITHUB_REPOSITORY_PATTERN.test(trimmedValue)) return t('input.invalid');
    return '';
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const validationError = validateUrl(url);
    if (validationError) {
      setError(validationError);
      return;
    }
    setError('');
    onSubmit(url.trim());
  };

  return (
    <section className="hero-panel" aria-labelledby="analyzer-title">
      <div className="hero-copy">
        <p className="eyebrow">{t('input.eyebrow')}</p>
        <h1 id="analyzer-title">{t('input.title')}</h1>
        <p>{t('input.description')}</p>
      </div>

      <form onSubmit={handleSubmit} className="repo-form" noValidate>
        <label htmlFor="repo-url">{t('input.label')}</label>
        <div className="repo-input-row">
          <div className="repo-input-wrap">
            <GitBranch size={18} aria-hidden="true" />
            <input
              id="repo-url"
              type="url"
              value={url}
              onChange={(event) => {
                setUrl(event.target.value);
                if (error) setError('');
              }}
              placeholder={t('input.placeholder')}
              disabled={loading}
              aria-invalid={Boolean(error)}
              aria-describedby={error ? 'repo-url-error' : undefined}
              autoComplete="url"
            />
          </div>
          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? (
              <LoaderCircle className="animate-spin" size={18} aria-hidden="true" />
            ) : (
              <ArrowRight size={18} aria-hidden="true" />
            )}
            {loading ? t('input.analyzing') : t('input.analyze')}
          </button>
        </div>
        {error ? (
          <p id="repo-url-error" className="field-error" role="alert">
            {error}
          </p>
        ) : null}
      </form>

      {loading ? (
        <div className="progress-panel" role="status" aria-live="polite">
          <div>
            <LoaderCircle className="animate-spin text-brand-blue" size={20} />
          </div>
          <div>
            <p className="font-semibold text-slate-900">{t('input.progressTitle')}</p>
            <ul>
              <li>{t('input.clone')}</li>
              <li>{t('input.architecture')}</li>
              <li>{t('input.flows')}</li>
              <li>{t('input.guide')}</li>
            </ul>
            <p className="mt-2 text-xs text-slate-500">{t('input.timing')}</p>
          </div>
        </div>
      ) : null}
    </section>
  );
}
