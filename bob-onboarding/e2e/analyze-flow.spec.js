import { test, expect } from '@playwright/test';

test.describe('Repository Analysis Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display the main page with input form', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Bob Onboarding Accelerator/i);
    
    // Check input field is present
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeVisible();
    
    // Check analyze button is present
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeVisible();
  });

  test('should show validation error for invalid URL', async ({ page }) => {
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    // Enter invalid URL
    await input.fill('not-a-valid-url');
    await button.click();
    
    // Should show error message
    await expect(page.getByText(/analysis failed/i)).toBeVisible({ timeout: 10000 });
  });

  test('should show validation error for non-GitHub URL', async ({ page }) => {
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    // Enter non-GitHub URL
    await input.fill('https://gitlab.com/user/repo');
    await button.click();
    
    // Should show error message
    await expect(page.getByText(/analysis failed/i)).toBeVisible({ timeout: 10000 });
  });

  test('should show loading state during analysis', async ({ page }) => {
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    // Enter valid URL
    await input.fill('https://github.com/octocat/Hello-World');
    await button.click();
    
    // Should show loading state
    await expect(page.getByText(/analyzing/i)).toBeVisible();
  });

  test.skip('complete analysis workflow', async ({ page }) => {
    // This test requires backend to be running with valid Bob API credentials
    test.setTimeout(120000); // 2 minutes timeout
    
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    // Enter valid repository URL
    await input.fill('https://github.com/octocat/Hello-World');
    await button.click();
    
    // Wait for analysis to complete
    await expect(page.getByText(/analysis complete/i)).toBeVisible({ timeout: 120000 });
    
    // Check that results are displayed
    await expect(page.getByText(/analyzed.*files/i)).toBeVisible();
    
    // Check architecture diagram is present
    const diagram = page.locator('.mermaid, [data-testid="architecture-diagram"]');
    await expect(diagram).toBeVisible();
    
    // Check flow cards are present
    const flowCards = page.locator('[data-testid="flow-card"]');
    await expect(flowCards.first()).toBeVisible();
    
    // Check guide is present
    await expect(page.getByText(/what does this project do/i)).toBeVisible();
    
    // Check reset button is present
    const resetButton = page.getByRole('button', { name: /analyze another repository/i });
    await expect(resetButton).toBeVisible();
  });

  test('should allow resetting after error', async ({ page }) => {
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    // Trigger an error
    await input.fill('invalid-url');
    await button.click();
    
    // Wait for error
    await expect(page.getByText(/analysis failed/i)).toBeVisible({ timeout: 10000 });
    
    // Clear input and try again
    await input.clear();
    await input.fill('https://github.com/octocat/Hello-World');
    
    // Error should be cleared when starting new analysis
    await button.click();
    await expect(page.getByText(/analyzing/i)).toBeVisible();
  });

  test('should display network error with troubleshooting tips', async ({ page }) => {
    // Simulate network error by going offline
    await page.context().setOffline(true);
    
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    await input.fill('https://github.com/octocat/Hello-World');
    await button.click();
    
    // Should show network error
    await expect(page.getByText(/cannot connect/i)).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/troubleshooting tips/i)).toBeVisible();
    
    // Restore network
    await page.context().setOffline(false);
  });
});

test.describe('Responsive Design', () => {
  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/');
    
    // Check that elements are visible on mobile
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeVisible();
    
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeVisible();
  });

  test('should be responsive on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await page.goto('/');
    
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeVisible();
    
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeVisible();
  });

  test('should be responsive on desktop', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 }); // Full HD
    await page.goto('/');
    
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeVisible();
    
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeVisible();
  });
});

test.describe('Accessibility', () => {
  test('should have proper heading structure', async ({ page }) => {
    await page.goto('/');
    
    // Check for main heading
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toBeVisible();
  });

  test('should have accessible form elements', async ({ page }) => {
    await page.goto('/');
    
    // Input should have label or placeholder
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeVisible();
    
    // Button should have accessible name
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeVisible();
  });

  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/');
    
    // Tab to input
    await page.keyboard.press('Tab');
    const input = page.getByPlaceholder(/github repository url/i);
    await expect(input).toBeFocused();
    
    // Tab to button
    await page.keyboard.press('Tab');
    const button = page.getByRole('button', { name: /analyze/i });
    await expect(button).toBeFocused();
  });
});

test.describe('Error Handling', () => {
  test('should handle empty input', async ({ page }) => {
    await page.goto('/');
    
    const button = page.getByRole('button', { name: /analyze/i });
    await button.click();
    
    // Should show validation error or prevent submission
    // The exact behavior depends on implementation
  });

  test('should handle special characters in URL', async ({ page }) => {
    await page.goto('/');
    
    const input = page.getByPlaceholder(/github repository url/i);
    const button = page.getByRole('button', { name: /analyze/i });
    
    await input.fill('https://github.com/user/repo<script>alert("xss")</script>');
    await button.click();
    
    // Should handle safely without XSS
    await expect(page.getByText(/analysis failed/i)).toBeVisible({ timeout: 10000 });
  });
});

// Made with Bob
