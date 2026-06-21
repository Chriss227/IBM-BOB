import { useState } from 'react';
import {
  ArrowRight, BookOpen, Boxes, Check, Clock3, CodeXml, FileCode2,
  GitBranch, Network, Route, SearchCode, ShieldCheck, Sparkles,
  Users, Wrench, Zap,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

const DEMO_REPOS = [
  {
    id: 1, name: 'FastAPI', url: 'https://github.com/tiangolo/fastapi',
    description: 'fastApiDescription', language: 'Python', stars: '70k+',
    complexity: 'medium', analysisTime: '45s',
    highlights: ['fastApiHighlight1', 'fastApiHighlight2', 'fastApiHighlight3'],
  },
  {
    id: 2, name: 'Express.js', url: 'https://github.com/expressjs/express',
    description: 'expressDescription', language: 'JavaScript', stars: '63k+',
    complexity: 'low', analysisTime: '30s',
    highlights: ['expressHighlight1', 'expressHighlight2', 'expressHighlight3'],
  },
  {
    id: 3, name: 'Flask', url: 'https://github.com/pallets/flask',
    description: 'flaskDescription', language: 'Python', stars: '66k+',
    complexity: 'low', analysisTime: '35s',
    highlights: ['flaskHighlight1', 'flaskHighlight2', 'flaskHighlight3'],
  },
  {
    id: 4, name: 'Django', url: 'https://github.com/django/django',
    description: 'djangoDescription', language: 'Python', stars: '76k+',
    complexity: 'high', analysisTime: '90s',
    highlights: ['djangoHighlight1', 'djangoHighlight2', 'djangoHighlight3'],
  },
];

const FEATURES = [
  { icon: Network, title: 'architectureTitle', body: 'architectureBody', note: 'architectureNote' },
  { icon: Route, title: 'flowsTitle', body: 'flowsBody', note: 'flowsNote' },
  { icon: BookOpen, title: 'guideTitle', body: 'guideBody', note: 'guideNote' },
  { icon: Zap, title: 'speedTitle', body: 'speedBody', note: 'speedNote' },
];

const USE_CASES = [
  { icon: Users, title: 'teamTitle', body: 'teamBody' },
  { icon: SearchCode, title: 'reviewsTitle', body: 'reviewsBody' },
  { icon: Wrench, title: 'debtTitle', body: 'debtBody' },
  { icon: FileCode2, title: 'documentationTitle', body: 'documentationBody' },
];

const STEPS = [
  { icon: GitBranch, title: 'step1Title', body: 'step1Body' },
  { icon: CodeXml, title: 'step2Title', body: 'step2Body' },
  { icon: Boxes, title: 'step3Title', body: 'step3Body' },
  { icon: Sparkles, title: 'step4Title', body: 'step4Body' },
];

function SectionHeading({ title, body }) {
  return (
    <header className="mx-auto mb-12 max-w-2xl text-center">
      <h2 className="font-display text-3xl font-bold text-slate-950 sm:text-4xl">{title}</h2>
      <p className="mt-4 text-lg leading-7 text-slate-600">{body}</p>
    </header>
  );
}

export default function Demo() {
  const { t } = useTranslation();
  const [selectedRepo, setSelectedRepo] = useState(null);
  const copy = (key) => t(`demoFull.${key}`);

  return (
    <main className="overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <section className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 opacity-[0.08]" />
        <div className="app-container relative py-16 text-center sm:py-20">
          <div className="mx-auto mb-6 grid h-16 w-16 place-items-center rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 text-white shadow-xl">
            <Network size={32} />
          </div>
          <h1 className="font-display text-4xl font-extrabold tracking-tight text-slate-950 sm:text-6xl">
            Repo Accelerate
          </h1>
          <p className="mx-auto mt-5 max-w-3xl text-lg leading-8 text-slate-600 sm:text-2xl">
            {copy('heroBody')}
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link to="/" className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-8 py-4 font-semibold text-white shadow-lg transition hover:bg-blue-700 hover:shadow-xl">
              {copy('try')} <ArrowRight size={18} />
            </Link>
            <a href="https://github.com/Chriss227/IBM-BOB" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 rounded-lg border-2 border-slate-200 bg-white px-8 py-4 font-semibold text-slate-800 shadow-lg transition hover:bg-slate-50 hover:shadow-xl">
              <GitBranch size={18} /> {t('demo.viewGithub')}
            </a>
          </div>
          <dl className="mt-16 grid grid-cols-2 gap-8 md:grid-cols-4">
            {[['30–90s', 'analysisTime'], ['3', 'keyFlows'], ['100%', 'automated'], ['5 min', 'toUnderstand']].map(([value, label], index) => (
              <div key={label}>
                <dt className="text-sm font-medium text-slate-600">{copy(label)}</dt>
                <dd className={`mt-1 text-4xl font-extrabold ${index % 2 ? 'text-purple-600' : 'text-blue-600'}`}>{value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <section className="app-container py-16 sm:py-20">
        <SectionHeading title={copy('featuresTitle')} body={copy('featuresSubtitle')} />
        <div className="grid gap-8 md:grid-cols-2">
          {FEATURES.map(({ icon: Icon, title, body, note }) => (
            <article key={title} className="rounded-xl border border-slate-100 bg-white p-8 shadow-lg transition hover:-translate-y-1 hover:shadow-xl">
              <div className="mb-5 grid h-12 w-12 place-items-center rounded-xl bg-blue-50 text-blue-600"><Icon size={25} /></div>
              <h3 className="font-display text-2xl font-bold text-slate-950">{copy(title)}</h3>
              <p className="mt-3 leading-7 text-slate-600">{copy(body)}</p>
              <p className="mt-5 rounded-lg border-l-4 border-blue-500 bg-blue-50 p-4 text-sm font-medium text-blue-950">{copy(note)}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="app-container">
          <SectionHeading title={copy('reposTitle')} body={copy('reposSubtitle')} />
          <div className="grid gap-6 md:grid-cols-2">
            {DEMO_REPOS.map((repo) => {
              const selected = selectedRepo === repo.id;
              return (
                <article key={repo.id} className={`rounded-xl border-2 bg-white p-6 shadow-lg transition ${selected ? 'border-blue-500 shadow-xl' : 'border-slate-200 hover:border-blue-300 hover:shadow-xl'}`}>
                  <button type="button" onClick={() => setSelectedRepo(repo.id)} aria-pressed={selected} className="w-full text-left">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="font-display text-2xl font-bold text-slate-950">{repo.name}</h3>
                        <p className="mt-2 text-sm leading-6 text-slate-600">{copy(`repos.${repo.description}`)}</p>
                      </div>
                      <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-800">{repo.language}</span>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-4 text-sm text-slate-600">
                      <span className="inline-flex items-center gap-1"><Sparkles size={15} />{repo.stars}</span>
                      <span className="inline-flex items-center gap-1"><ShieldCheck size={15} />{copy(`repos.${repo.complexity}`)}</span>
                      <span className="inline-flex items-center gap-1"><Clock3 size={15} />{repo.analysisTime}</span>
                    </div>
                    <ul className="mt-4 space-y-2">
                      {repo.highlights.map((key) => (
                        <li key={key} className="flex items-start gap-2 text-sm text-slate-700">
                          <Check size={16} className="mt-0.5 shrink-0 text-emerald-500" /> {copy(`repos.${key}`)}
                        </li>
                      ))}
                    </ul>
                  </button>
                  <Link to={`/?url=${encodeURIComponent(repo.url)}`} className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 font-semibold text-white transition hover:bg-blue-700">
                    {copy('analyzeRepo')} <ArrowRight size={17} />
                  </Link>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="app-container py-16 sm:py-20">
        <SectionHeading title={copy('useCasesTitle')} body={copy('useCasesSubtitle')} />
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {USE_CASES.map(({ icon: Icon, title, body }) => (
            <article key={title} className="rounded-xl border border-slate-100 bg-white p-6 text-center shadow-lg">
              <Icon size={38} className="mx-auto text-purple-600" />
              <h3 className="mt-4 font-display text-xl font-bold text-slate-950">{copy(title)}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{copy(body)}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-gradient-to-r from-blue-600 to-purple-600 py-16 sm:py-20">
        <div className="app-container">
          <h2 className="text-center font-display text-4xl font-bold text-white">{copy('processTitle')}</h2>
          <ol className="mt-12 grid gap-8 md:grid-cols-4">
            {STEPS.map(({ icon: Icon, title, body }, index) => (
              <li key={title} className="text-center">
                <div className="mx-auto grid h-20 w-20 place-items-center rounded-full bg-white text-purple-600 shadow-lg"><Icon size={34} /></div>
                <span className="mx-auto mt-4 grid h-12 w-12 place-items-center rounded-full bg-white/20 text-2xl font-bold text-white">{index + 1}</span>
                <h3 className="mt-4 text-xl font-bold text-white">{copy(title)}</h3>
                <p className="mt-2 leading-6 text-blue-100">{copy(body)}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="app-container py-16 sm:py-20">
        <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 p-8 text-center shadow-2xl sm:p-12">
          <h2 className="font-display text-3xl font-bold text-white sm:text-4xl">{copy('ctaTitle')}</h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-blue-100">{copy('ctaBody')}</p>
          <Link to="/" className="mt-8 inline-flex items-center gap-2 rounded-lg bg-white px-8 py-4 font-semibold text-blue-600 shadow-lg transition hover:bg-slate-100">
            {copy('ctaAction')} <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      <footer className="bg-slate-950 py-12 text-center text-slate-400">
        <div className="app-container">
          <p>{copy('footer')}</p>
          <div className="mt-5 flex justify-center gap-6 text-sm">
            <Link to="/" className="transition hover:text-white">{t('nav.analyzer')}</Link>
            <a href="https://github.com/Chriss227/IBM-BOB" target="_blank" rel="noopener noreferrer" className="transition hover:text-white">{t('nav.github')}</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
