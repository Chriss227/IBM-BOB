import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import { GitBranch, Languages, Network } from 'lucide-react';
import Home from './pages/Home';
import Demo from './pages/Demo';
import { normalizeLanguage } from './i18n';

function App() {
  const { t, i18n } = useTranslation();
  const language = normalizeLanguage(i18n.resolvedLanguage);

  useEffect(() => {
    document.documentElement.lang = language;
    document.title = `${t('brand.name')} — ${t('brand.tagline')}`;
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute('content', t('brand.tagline'));
  }, [language, t]);

  const navClass = ({ isActive }) =>
    `nav-link ${isActive ? 'nav-link-active' : ''}`;

  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-950">
        <nav className="app-nav" aria-label="Primary navigation">
          <div className="app-container flex min-h-16 items-center justify-between gap-4">
            <Link to="/" className="brand-lockup">
              <span className="brand-mark" aria-hidden="true">
                <Network size={20} strokeWidth={2.2} />
              </span>
              <span className="font-display text-lg font-bold tracking-tight text-slate-950">
                {t('brand.name')}
              </span>
            </Link>

            <div className="flex items-center gap-2 sm:gap-5">
              <div className="hidden items-center gap-5 sm:flex">
                <NavLink to="/" end className={navClass}>
                  {t('nav.analyzer')}
                </NavLink>
                <NavLink to="/demo" className={navClass}>
                  {t('nav.demo')}
                </NavLink>
              </div>
              <a
                href="https://github.com/Chriss227/IBM-BOB"
                target="_blank"
                rel="noopener noreferrer"
                className="nav-link hidden items-center gap-2 md:flex"
              >
                <GitBranch size={16} />
                {t('nav.github')}
              </a>

              <div className="language-switcher" aria-label={t('nav.language')}>
                <Languages size={15} aria-hidden="true" />
                {['en', 'es'].map((code) => (
                  <button
                    key={code}
                    type="button"
                    onClick={() => i18n.changeLanguage(code)}
                    className={language === code ? 'language-option-active' : 'language-option'}
                    aria-pressed={language === code}
                  >
                    {code.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/demo" element={<Demo />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
