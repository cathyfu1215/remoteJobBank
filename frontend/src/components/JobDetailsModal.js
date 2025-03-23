import React from 'react';
import './JobDetailsModal.css';

function JobDetailsModal({ job, onClose }) {
  if (!job) return null;
  
  // Function to decode HTML entities and prepare HTML for rendering
  const decodeHtml = (html) => {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
  };
  
  // Prepare job description for rendering
  const renderJobDescription = () => {
    if (!job.job_description) return <p>No job description provided.</p>;
    
    // Decode HTML entities
    const decodedHtml = decodeHtml(job.job_description);
    
    return (
      <div dangerouslySetInnerHTML={{ __html: decodedHtml }} className="html-content" />
    );
  };
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        
        <div className="modal-header">
          <h2>{job.title}</h2>
          <span className="modal-category">{job.category}</span>
        </div>
        
        <div className="modal-company">
          <h3>{job.company}</h3>
          {job.salary_range && job.salary_range !== "Not Specified" && (
            <span className="modal-salary">{job.salary_range}</span>
          )}
        </div>
        
        <div className="modal-section">
          <h4>About the Company</h4>
          <p className="preserve-format">{job.company_about || "No company description provided."}</p>
        </div>
        
        <div className="modal-section">
          <h4>Job Description</h4>
          <div className="job-description">
            {renderJobDescription()}
          </div>
        </div>
        
        <div className="modal-grid">
          {job.region && (
            <div className="modal-grid-item">
              <h4>Region</h4>
              <p>{Array.isArray(job.region) ? job.region.join(', ') : job.region}</p>
            </div>
          )}
          
          {job.countries && job.countries.length > 0 && (
            <div className="modal-grid-item">
              <h4>Countries</h4>
              <p>{job.countries.join(', ')}</p>
            </div>
          )}
          
          {job.timezones && job.timezones.length > 0 && (
            <div className="modal-grid-item">
              <h4>Timezones</h4>
              <p>{job.timezones.join(', ')}</p>
            </div>
          )}
          
          {job.apply_before && (
            <div className="modal-grid-item">
              <h4>Apply Before</h4>
              <p>{job.apply_before}</p>
            </div>
          )}
          
          {job.source && (
            <div className="modal-grid-item">
              <h4>Source</h4>
              <p>{job.source}</p>
            </div>
          )}
          
          {job.url && (
            <div className="modal-grid-item">
              <h4>Original Job Posting</h4>
              <p>
                <a href={job.url} target="_blank" rel="noopener noreferrer">
                  View Original
                </a>
              </p>
            </div>
          )}
        </div>
        
        {job.skills && job.skills.length > 0 && (
          <div className="modal-section">
            <h4>Required Skills</h4>
            <div className="modal-skills">
              {job.skills.map((skill, index) => (
                <span key={index} className="modal-skill-tag">{skill}</span>
              ))}
            </div>
          </div>
        )}
        
        <div className="modal-section job-id-section">
          <p>Job ID: {job.job_id}</p>
        </div>
        
        <div className="modal-actions">
          <a 
            href={job.apply_url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="modal-apply-btn"
          >
            Apply for this Position
          </a>
        </div>
      </div>
    </div>
  );
}

export default JobDetailsModal; 