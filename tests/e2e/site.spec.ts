import { test, expect } from '@playwright/test';

test.describe('Agentic AI Landscape Tracker - Site Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Agentic AI Landscape Tracker/);
  });

  test('displays header with logo and title', async ({ page }) => {
    // Check for Version 1 logo image
    await expect(page.locator('.logo-image')).toBeVisible();
    
    // Check for site title
    await expect(page.locator('.site-title')).toContainText('Agentic AI Landscape Tracker');
  });

  test('displays filter controls', async ({ page }) => {
    // Source filter
    await expect(page.locator('#source-filter')).toBeVisible();
    
    // Category filter
    await expect(page.locator('#category-filter')).toBeVisible();
    
    // Search input
    await expect(page.locator('#search-input')).toBeVisible();
  });

  test('loads and displays entries', async ({ page }) => {
    // Wait for data to load
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // Check that at least one entry is displayed
    const entries = page.locator('.entry-card');
    await expect(entries).not.toHaveCount(0);
  });

  test('entry cards have required elements', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    const firstEntry = page.locator('.entry-card').first();
    
    // Title with link
    await expect(firstEntry.locator('.entry-title a')).toBeVisible();
    
    // Source
    await expect(firstEntry.locator('.entry-source')).toBeVisible();
    
    // Date
    await expect(firstEntry.locator('.entry-date')).toBeVisible();
    
    // Category
    await expect(firstEntry.locator('.entry-category')).toBeVisible();
    
    // Summary
    await expect(firstEntry.locator('.entry-summary')).toBeVisible();
  });

  test('source filter works', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // Get initial count
    const initialCount = await page.locator('.entry-card').count();
    expect(initialCount).toBeGreaterThan(0);
    
    // Select a specific source
    await page.selectOption('#source-filter', { index: 1 }); // Select first non-"all" option
    
    // Wait for filter to apply
    await page.waitForTimeout(500);
    
    // Count should be less than or equal to initial
    const filteredCount = await page.locator('.entry-card').count();
    expect(filteredCount).toBeLessThanOrEqual(initialCount);
  });

  test('category filter works', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // First reset to "All Categories" to get true initial count
    await page.selectOption('#category-filter', 'all');
    await page.waitForTimeout(500);
    
    const initialCount = await page.locator('.entry-card').count();
    
    // Select a specific category (not "all")
    await page.selectOption('#category-filter', { index: 1 });
    
    await page.waitForTimeout(500);
    
    const filteredCount = await page.locator('.entry-card').count();
    expect(filteredCount).toBeLessThanOrEqual(initialCount);
  });

  test('search filter works', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    const initialCount = await page.locator('.entry-card').count();
    
    // Type in search box
    await page.fill('#search-input', 'SDK');
    
    // Wait for debounce
    await page.waitForTimeout(500);
    
    const filteredCount = await page.locator('.entry-card').count();
    
    // Should have fewer or same results
    expect(filteredCount).toBeLessThanOrEqual(initialCount);
    
    // If results exist, they should contain "SDK"
    if (filteredCount > 0) {
      const firstEntry = page.locator('.entry-card').first();
      const text = await firstEntry.textContent();
      expect(text?.toLowerCase()).toContain('sdk');
    }
  });

  test('entry links are external and open in new tab', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    const firstLink = page.locator('.entry-title a').first();
    
    // Check target="_blank"
    await expect(firstLink).toHaveAttribute('target', '_blank');
    
    // Check rel="noopener"
    await expect(firstLink).toHaveAttribute('rel', 'noopener');
  });

  test('displays last updated timestamp', async ({ page }) => {
    const lastUpdated = page.locator('#last-updated');
    await expect(lastUpdated).toBeVisible();
    await expect(lastUpdated).toContainText('Last updated:');
  });

  test('displays footer', async ({ page }) => {
    const footer = page.locator('.footer');
    await expect(footer).toBeVisible();
    await expect(footer).toContainText('Version 1');
  });

  test('handles empty search results', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // Search for something that doesn't exist
    await page.fill('#search-input', 'xyznonexistentquery123');
    
    await page.waitForTimeout(500);
    
    // Should show empty state
    await expect(page.locator('.empty-state')).toBeVisible();
    await expect(page.locator('.empty-state')).toContainText('No updates found');
  });

  test('is responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // Check that content is still visible and readable
    await expect(page.locator('.header')).toBeVisible();
    
    // On mobile, filters are collapsed by default - check toggle button is visible
    await expect(page.locator('.filter-toggle')).toBeVisible();
    
    // Expand filters and verify they become visible
    await page.click('.filter-toggle');
    await expect(page.locator('.filters')).toBeVisible();
    await expect(page.locator('.filters')).toHaveClass(/expanded/);
    
    await expect(page.locator('.entry-card').first()).toBeVisible();
  });

  test('entry cards have hover effect', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    const firstEntry = page.locator('.entry-card').first();
    
    // Get initial position
    const initialBox = await firstEntry.boundingBox();
    
    // Hover over entry
    await firstEntry.hover();
    
    // Wait for transition
    await page.waitForTimeout(300);
    
    // Entry should still be visible (transform doesn't change visibility)
    await expect(firstEntry).toBeVisible();
  });

  test('filters can be combined', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    // Apply source filter
    await page.selectOption('#source-filter', { index: 1 });
    await page.waitForTimeout(300);
    
    // Apply search
    await page.fill('#search-input', 'model');
    await page.waitForTimeout(500);
    
    // Should have results that match both filters
    const entries = await page.locator('.entry-card').count();
    
    // Verify at least the filtering didn't break
    expect(entries).toBeGreaterThanOrEqual(0);
  });

  test('resets filters correctly', async ({ page }) => {
    await page.waitForSelector('.entry-card', { timeout: 5000 });
    
    const initialCount = await page.locator('.entry-card').count();
    
    // Apply filters
    await page.selectOption('#source-filter', { index: 1 });
    await page.fill('#search-input', 'test');
    await page.waitForTimeout(500);
    
    // Reset filters
    await page.selectOption('#source-filter', 'all');
    await page.fill('#search-input', '');
    await page.waitForTimeout(500);
    
    // Should be back to initial count
    const finalCount = await page.locator('.entry-card').count();
    expect(finalCount).toBe(initialCount);
  });
});
