/**
 * Agentic AI Landscape Tracker - Frontend Application
 */

class AITracker {
    constructor() {
        this.entries = [];
        this.filteredEntries = [];
        this.sources = new Set();
        this.categories = new Set();
        
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.setupFilters();
        this.setupSearch();
        this.render();
    }
    
    async loadData() {
        try {
            const response = await fetch('../data/entries.json');
            const data = await response.json();
            
            this.entries = data.entries || [];
            this.filteredEntries = [...this.entries];
            
            // Extract unique sources and categories
            this.entries.forEach(entry => {
                if (entry.source) this.sources.add(entry.source);
                if (entry.category) this.categories.add(entry.category);
            });
            
            // Update last updated timestamp
            if (data.last_updated) {
                const lastUpdated = document.getElementById('last-updated');
                const date = new Date(data.last_updated);
                lastUpdated.textContent = `Last updated: ${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
            }
        } catch (error) {
            console.error('Failed to load data:', error);
            this.showError('Failed to load updates. Please try again later.');
        }
    }
    
    setupFilters() {
        const sourceFilter = document.getElementById('source-filter');
        const categoryFilter = document.getElementById('category-filter');
        
        // Populate source filter
        this.sources.forEach(source => {
            const option = document.createElement('option');
            option.value = source;
            option.textContent = source;
            sourceFilter.appendChild(option);
        });
        
        // Populate category filter
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
        
        // Add event listeners
        sourceFilter.addEventListener('change', () => this.applyFilters());
        categoryFilter.addEventListener('change', () => this.applyFilters());
    }
    
    setupSearch() {
        const searchInput = document.getElementById('search-input');
        let debounceTimer;
        
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => this.applyFilters(), 300);
        });
    }
    
    applyFilters() {
        const sourceValue = document.getElementById('source-filter').value;
        const categoryValue = document.getElementById('category-filter').value;
        const searchValue = document.getElementById('search-input').value.toLowerCase();
        
        this.filteredEntries = this.entries.filter(entry => {
            // Source filter
            if (sourceValue !== 'all' && entry.source !== sourceValue) {
                return false;
            }
            
            // Category filter
            if (categoryValue !== 'all' && entry.category !== categoryValue) {
                return false;
            }
            
            // Search filter
            if (searchValue) {
                const searchableText = [
                    entry.title,
                    entry.summary,
                    entry.source,
                    ...(entry.tags || [])
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchValue)) {
                    return false;
                }
            }
            
            return true;
        });
        
        this.render();
    }
    
    render() {
        const timeline = document.getElementById('timeline');
        
        if (this.filteredEntries.length === 0) {
            timeline.innerHTML = `
                <div class="empty-state">
                    <h3>No updates found</h3>
                    <p>Try adjusting your filters or check back later.</p>
                </div>
            `;
            return;
        }
        
        timeline.innerHTML = this.filteredEntries.map(entry => this.renderEntry(entry)).join('');
    }
    
    renderEntry(entry) {
        const date = entry.date ? this.formatDate(entry.date) : 'Date unknown';
        const tags = (entry.tags || []).map(tag => `<span class="tag">${this.escapeHtml(tag)}</span>`).join('');
        
        return `
            <article class="entry-card" data-source="${this.escapeHtml(entry.source)}">
                <header class="entry-header">
                    <h2 class="entry-title">
                        <a href="${this.escapeHtml(entry.url)}" target="_blank" rel="noopener">
                            ${this.escapeHtml(entry.title)}
                        </a>
                    </h2>
                </header>
                <div class="entry-meta">
                    <span class="entry-source">${this.escapeHtml(entry.source)}</span>
                    <span class="entry-date">${date}</span>
                    <span class="entry-category">${this.escapeHtml(entry.category || 'Other')}</span>
                </div>
                <p class="entry-summary">${this.escapeHtml(entry.summary || 'No summary available.')}</p>
                ${tags ? `<div class="entry-tags">${tags}</div>` : ''}
            </article>
        `;
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        
        return date.toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showError(message) {
        const timeline = document.getElementById('timeline');
        timeline.innerHTML = `
            <div class="empty-state">
                <h3>Error</h3>
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new AITracker();
});
