import { FileCode2, GitCommitHorizontal } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export default function FlowCards({ flows }) {
  const { t } = useTranslation();
  if (!flows?.length) return null;

  return (
    <section aria-labelledby="flows-title">
      <div className="workspace-heading">
        <div>
          <h2 id="flows-title">{t('flow.title')}</h2>
          <p>{t('flow.subtitle')}</p>
        </div>
      </div>

      <div className="flow-list">
        {flows.map((flow, index) => (
          <article className="flow-row" key={`${flow.name}-${index}`} data-testid="flow-card">
            <div className="flow-index">{String(index + 1).padStart(2, '0')}</div>
            <div className="flow-content">
              <h3>{flow.name}</h3>
              <p>{flow.description}</p>

              {flow.steps?.length ? (
                <div className="flow-section">
                  <h4>
                    <GitCommitHorizontal size={15} />
                    {t('flow.steps')}
                  </h4>
                  <ol>
                    {flow.steps.map((step, stepIndex) => (
                      <li key={`${step}-${stepIndex}`}>
                        <span>{stepIndex + 1}</span>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
              ) : null}

              {flow.files?.length ? (
                <div className="flow-section">
                  <h4>
                    <FileCode2 size={15} />
                    {t('flow.files')}
                  </h4>
                  <div className="file-list">
                    {flow.files.map((file) => (
                      <code key={file} title={file}>
                        {file}
                      </code>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
