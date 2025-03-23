import React, { useState } from 'react';
import './FilterPanel.css';

function FilterPanel({ categories, onFilterChange, onClearFilters, activeFilter }) {
  const [searchTerm, setSearchTerm] = useState('');
  
  const handleCategoryClick = (category) => {
    onFilterChange('category', category);
  };
  
  const handleCompanySearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onFilterChange('company', searchTerm.trim());
    }
  };
  
  return (
    <div className="filter-panel">
      <div className="filter-section">
        <h3>Search by Company</h3>
        <form onSubmit={handleCompanySearch}>
          <div className="search-input-group">
            <input
              type="text"
              placeholder="Enter company name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-btn">Search</button>
          </div>
        </form>
      </div>
      
      <div className="filter-section">
        <h3>Filter by Category</h3>
        <ul className="category-list">
          {categories.map(category => (
            <li key={category}>
              <button 
                className={`category-btn ${activeFilter.type === 'category' && activeFilter.value === category ? 'active' : ''}`}
                onClick={() => handleCategoryClick(category)}
              >
                {category}
              </button>
            </li>
          ))}
        </ul>
      </div>
      
      {(activeFilter.type && activeFilter.value) && (
        <button onClick={onClearFilters} className="clear-filters-btn">
          Clear Filters
        </button>
      )}
    </div>
  );
}

export default FilterPanel;
