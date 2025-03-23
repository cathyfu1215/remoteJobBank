import React, { useState, useEffect } from 'react';
import JobList from './components/JobList';
import FilterPanel from './components/FilterPanel';
import Header from './components/Header';
import Pagination from './components/Pagination';
import Loading from './components/Loading';
import { fetchJobs, fetchCategories } from './services/api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const [filter, setFilter] = useState({
    type: null,
    value: null
  });

  // Fetch allowed categories when component mounts
  useEffect(() => {
    const getCategories = async () => {
      try {
        const fetchedCategories = await fetchCategories();
        setCategories(fetchedCategories);
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    };
    
    getCategories();
  }, []);

  // Fetch jobs when page changes or filter changes
  useEffect(() => {
    const getJobs = async () => {
      setLoading(true);
      try {
        let response;
        
        if (filter.type && filter.value) {
          response = await fetchJobs(currentPage, 10, filter.type, filter.value);
        } else {
          response = await fetchJobs(currentPage);
        }
        
        setJobs(response.items);
        setTotalPages(response.pages);
        setTotalJobs(response.total);
        setError(null);
      } catch (err) {
        setError('Failed to fetch jobs. Please try again later.');
        console.error('Error fetching jobs:', err);
      } finally {
        setLoading(false);
      }
    };
    
    getJobs();
  }, [currentPage, filter]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  const handleFilterChange = (type, value) => {
    setFilter({ type, value });
    setCurrentPage(1); // Reset to first page when filter changes
  };

  const clearFilters = () => {
    setFilter({ type: null, value: null });
    setCurrentPage(1);
  };

  return (
    <div className="app">
      <Header />
      
      <main className="container">
        <div className="content-wrapper">
          <FilterPanel 
            categories={categories} 
            onFilterChange={handleFilterChange}
            onClearFilters={clearFilters}
            activeFilter={filter}
          />
          
          <div className="main-content">
            {error && <div className="error-message">{error}</div>}
            
            {loading ? (
              <Loading />
            ) : (
              <>
                <div className="results-info">
                  {filter.type && filter.value ? (
                    <p>Showing results for {filter.type}: <strong>{filter.value}</strong></p>
                  ) : (
                    <p>Showing all remote jobs</p>
                  )}
                  <p>{totalJobs} jobs found</p>
                </div>
                
                {jobs.length === 0 ? (
                  <div className="no-results">
                    <h3>No jobs found</h3>
                    <p>Try adjusting your filters or search for something else.</p>
                    <button onClick={clearFilters} className="btn">Clear all filters</button>
                  </div>
                ) : (
                  <>
                    <JobList jobs={jobs} />
                    <Pagination 
                      currentPage={currentPage}
                      totalPages={totalPages}
                      onPageChange={handlePageChange}
                    />
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
