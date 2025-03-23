import React, { useState } from 'react';
import JobDetailsModal from './JobDetailsModal';
import './JobCard.css';

function JobCard({ job }) {
  const [showModal, setShowModal] = useState(false);
  
  const openModal = () => {
    setShowModal(true);
    document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
  };
  
  const closeModal = () => {
    setShowModal(false);
    document.body.style.overflow = ''; // Re-enable scrolling
  };
  
  return (
    <>
      <div className="job-card">
        <div className="job-card-header">
          <h2 className="job-title">{job.title}</h2>
          <span className="job-category">{job.category}</span>
        </div>
        
        <div className="job-company">
          <span className="company-name">{job.company}</span>
        </div>
        
        <div className="job-details">
          {/* Region */}
          <div className="job-detail-item">
            <span className="detail-label">Region:</span>
            <span className="detail-value">
              {Array.isArray(job.region) ? job.region.join(', ') : job.region}
            </span>
          </div>
          
          {/* Apply before date */}
          <div className="job-detail-item">
            <span className="detail-label">Apply before:</span>
            <span className="detail-value">{job.apply_before}</span>
          </div>
          
          {/* Salary - only shown if not empty or "Not Specified" */}
          {job.salary_range && job.salary_range !== "Not Specified" && (
            <div className="job-detail-item">
              <span className="detail-label">Salary:</span>
              <span className="detail-value salary">{job.salary_range}</span>
            </div>
          )}
        </div>
        
        <div className="job-actions">
          <a href={job.apply_url} target="_blank" rel="noopener noreferrer" className="apply-btn">
            Apply Now
          </a>
          <button className="view-details-btn" onClick={openModal}>View Details</button>
        </div>
      </div>
      
      {showModal && <JobDetailsModal job={job} onClose={closeModal} />}
    </>
  );
}

export default JobCard;
