import { useState } from 'react';
import { Check, Clipboard, Info } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useTranslation } from 'react-i18next';

export default function GuidePanel({ guide }) {
  const { t } = useTranslation();
  const [copied, setCopied] = useState(false);
  if (!guide) return null;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(guide);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section aria-labelledby="guide-title">
      <div className="workspace-heading">
        <div>
          <h2 id="guide-title">{t('guide.title')}</h2>
          <p>{t('guide.subtitle')}</p>
        </div>
        <button type="button" className="secondary-button" onClick={handleCopy}>
          {copied ? <Check size={16} /> : <Clipboard size={16} />}
          {copied ? t('guide.copied') : t('guide.copy')}
        </button>
      </div>

      <div className="guide-layout">
        <div className="markdown-body">
          <ReactMarkdown>{guide}</ReactMarkdown>
        </div>
        <aside className="guide-note">
          <Info size={18} />
          <p>{t('guide.note')}</p>
        </aside>
      </div>
    </section>
  );
}
