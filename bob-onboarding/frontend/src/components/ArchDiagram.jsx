import { useEffect, useRef, useState } from 'react';
import {
  CheckCircle2,
  Code2,
  Download,
  Focus,
  LoaderCircle,
  Minus,
  Plus,
  RefreshCw,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 1.8;
const ZOOM_STEP = 0.1;
const SUPPORTED_DIAGRAM = /^(flowchart|graph)\s+(LR|RL|TB|TD|BT)\b/i;
let renderSequence = 0;

export default function ArchDiagram({ mermaid: mermaidCode }) {
  const { t } = useTranslation();
  const diagramRef = useRef(null);
  const latestRenderRef = useRef(0);
  const [error, setError] = useState('');
  const [isRendering, setIsRendering] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [showCode, setShowCode] = useState(false);
  const [renderAttempt, setRenderAttempt] = useState(0);

  useEffect(() => {
    if (!mermaidCode || !diagramRef.current) return undefined;

    const currentRender = ++renderSequence;
    latestRenderRef.current = currentRender;
    let cancelled = false;

    const renderDiagram = async () => {
      setIsRendering(true);
      setError('');
      setZoom(1);

      try {
        const normalizedCode = mermaidCode.trim();
        if (!SUPPORTED_DIAGRAM.test(normalizedCode)) {
          throw new Error('Unsupported Mermaid diagram type');
        }

        const { default: mermaid } = await import('mermaid');
        mermaid.initialize({
          startOnLoad: false,
          securityLevel: 'strict',
          theme: 'base',
          flowchart: {
            htmlLabels: false,
            curve: 'basis',
            useMaxWidth: true,
          },
          themeVariables: {
            primaryColor: '#e7edff',
            primaryTextColor: '#172033',
            primaryBorderColor: '#2457e6',
            lineColor: '#64748b',
            secondaryColor: '#f8fafc',
            tertiaryColor: '#ffffff',
            fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
          },
        });

        await mermaid.parse(normalizedCode);
        const { svg } = await mermaid.render(`repo-architecture-${currentRender}`, normalizedCode);

        if (cancelled || latestRenderRef.current !== currentRender || !diagramRef.current) return;
        diagramRef.current.innerHTML = svg;
        const svgElement = diagramRef.current.querySelector('svg');
        if (svgElement) {
          svgElement.removeAttribute('height');
          svgElement.style.maxWidth = 'none';
          svgElement.style.width = '100%';
          svgElement.setAttribute('role', 'img');
          svgElement.setAttribute('aria-label', t('diagram.title'));
        }
      } catch (renderError) {
        console.error('Mermaid rendering error:', renderError);
        if (!cancelled && latestRenderRef.current === currentRender) {
          if (diagramRef.current) diagramRef.current.innerHTML = '';
          setError(t('diagram.failed'));
        }
      } finally {
        if (!cancelled && latestRenderRef.current === currentRender) {
          setIsRendering(false);
        }
      }
    };

    renderDiagram();
    return () => {
      cancelled = true;
    };
  }, [mermaidCode, renderAttempt, t]);

  if (!mermaidCode) return null;

  const updateZoom = (value) => {
    setZoom(Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, Number(value.toFixed(2)))));
  };

  const downloadSvg = () => {
    const svg = diagramRef.current?.querySelector('svg');
    if (!svg) return;
    const blob = new Blob([svg.outerHTML], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'repo-accelerate-architecture.svg';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section aria-labelledby="architecture-title">
      <div className="workspace-heading">
        <div>
          <div className="status-line">
            <span className="status-dot" />
            {error ? t('diagram.failedTitle') : t('diagram.ready')}
          </div>
          <h2 id="architecture-title">{t('diagram.title')}</h2>
          <p>{t('diagram.subtitle')}</p>
        </div>

        <div className="diagram-toolbar" aria-label={t('diagram.title')}>
          <button type="button" onClick={() => setZoom(1)} title={t('diagram.fit')}>
            <Focus size={16} />
            <span className="hidden sm:inline">{t('diagram.fit')}</span>
          </button>
          <button
            type="button"
            onClick={() => updateZoom(zoom - ZOOM_STEP)}
            disabled={zoom <= MIN_ZOOM}
            aria-label={t('diagram.zoomOut')}
          >
            <Minus size={16} />
          </button>
          <output className="zoom-output">{Math.round(zoom * 100)}%</output>
          <button
            type="button"
            onClick={() => updateZoom(zoom + ZOOM_STEP)}
            disabled={zoom >= MAX_ZOOM}
            aria-label={t('diagram.zoomIn')}
          >
            <Plus size={16} />
          </button>
          <button type="button" onClick={downloadSvg} disabled={isRendering || Boolean(error)}>
            <Download size={16} />
            <span className="hidden lg:inline">{t('diagram.download')}</span>
          </button>
          <button type="button" onClick={() => setShowCode((value) => !value)}>
            <Code2 size={16} />
            <span className="hidden lg:inline">
              {showCode ? t('diagram.hideCode') : t('diagram.viewCode')}
            </span>
          </button>
        </div>
      </div>

      <div className="blueprint-canvas">
        {isRendering ? (
          <div className="diagram-overlay" role="status">
            <LoaderCircle className="animate-spin" size={24} />
            <span>{t('diagram.rendering')}</span>
          </div>
        ) : null}

        {error ? (
          <div className="diagram-overlay diagram-error" role="alert">
            <RefreshCw size={24} />
            <strong>{t('diagram.failedTitle')}</strong>
            <span>{error}</span>
            <button type="button" onClick={() => setRenderAttempt((attempt) => attempt + 1)}>
              {t('diagram.retry')}
            </button>
          </div>
        ) : null}

        <div className="diagram-viewport">
          <div
            ref={diagramRef}
            data-testid="architecture-diagram"
            className="diagram-render"
            style={{ transform: `scale(${zoom})` }}
          />
        </div>
      </div>

      {showCode ? (
        <div className="mermaid-source">
          <div>
            <CheckCircle2 size={16} />
            Mermaid
          </div>
          <pre>
            <code>{mermaidCode}</code>
          </pre>
        </div>
      ) : null}
    </section>
  );
}
