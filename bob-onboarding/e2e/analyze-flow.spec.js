import { expect, test } from '@playwright/test';

const mockResult = {
  architecture_mermaid: 'flowchart LR\nA[Frontend] --> B[API]\nB --> C[Services]\nC --> D[Database]',
  flows: [{
    name: 'Request processing',
    description: 'How a request moves through the application.',
    steps: ['Receive request', 'Run service', 'Return response'],
    files: ['backend/main.py'],
  }],
  guide: '## 1. What does this project do?\n\nA sample repository.',
  repository_url: 'https://github.com/test/repo',
  files_analyzed: 42,
  language: 'en',
};

test.beforeEach(async ({ page }) => {
  await page.route('**/analyze', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockResult),
    });
  });
  await page.goto('/');
});

test('analyzes a repository and navigates result tabs', async ({ page }) => {
  await expect(page).toHaveTitle(/Repo Accelerate/i);
  await page.getByLabel(/GitHub repository URL/i).fill('https://github.com/test/repo');
  await page.getByRole('button', { name: /Analyze repository/i }).click();

  await expect(page.getByText(/42 files analyzed/i)).toBeVisible();
  await expect(page.getByTestId('architecture-diagram')).toBeVisible();

  await page.getByRole('tab', { name: /Key flows/i }).click();
  await expect(page.getByText('Request processing')).toBeVisible();

  await page.getByRole('tab', { name: /Onboarding guide/i }).click();
  await expect(page.getByText(/What does this project do/i)).toBeVisible();
});

test('switches to Spanish and preserves existing results', async ({ page }) => {
  await page.getByLabel(/GitHub repository URL/i).fill('https://github.com/test/repo');
  await page.getByRole('button', { name: /Analyze repository/i }).click();
  await expect(page.getByText(/42 files analyzed/i)).toBeVisible();

  await page.getByRole('button', { name: 'ES' }).click();
  await expect(page.getByRole('button', { name: /Analizar repositorio/i })).toBeVisible();
  await expect(page.getByText(/Estos resultados fueron generados en inglés/i)).toBeVisible();
});
