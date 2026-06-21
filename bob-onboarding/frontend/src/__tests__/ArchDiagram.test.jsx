import { describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ArchDiagram from '../components/ArchDiagram';
import '../i18n';

const renderMermaid = vi.fn();
const parseMermaid = vi.fn();

vi.mock('mermaid', () => ({
  default: {
    initialize: vi.fn(),
    parse: (...args) => parseMermaid(...args),
    render: (...args) => renderMermaid(...args),
  },
}));

describe('ArchDiagram', () => {
  it('renders valid flowcharts and exposes view controls', async () => {
    parseMermaid.mockResolvedValueOnce(true);
    renderMermaid.mockResolvedValueOnce({
      svg: '<svg viewBox="0 0 100 100"><text>Frontend</text></svg>',
    });
    const user = userEvent.setup();
    render(<ArchDiagram mermaid={'flowchart LR\nA[Frontend] --> B[API]'} />);

    await waitFor(() => expect(renderMermaid).toHaveBeenCalled());
    expect(screen.getByTestId('architecture-diagram').querySelector('svg')).toBeTruthy();

    await user.click(screen.getByRole('button', { name: /view code/i }));
    expect(screen.getByText(/flowchart LR/)).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: /zoom in/i }));
    expect(screen.getByText('110%')).toBeInTheDocument();
  });

  it('rejects unsupported diagram types and offers retry', async () => {
    render(<ArchDiagram mermaid={'sequenceDiagram\nA->>B: Hello'} />);
    expect((await screen.findAllByText(/diagram could not be rendered/i)).length).toBeGreaterThan(0);
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });
});
