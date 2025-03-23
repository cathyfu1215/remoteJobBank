import React from 'react';
import './JobCard.css';

function JobCard({ job }) {
  return (
    <div className="job-card">
      <div className="job-card-header">
        <h2 className="job-title">{job.title}</h2>
        <span className="job-category">{job.category}</span>
      </div>
      
      <div className="job-company">
        <span className="company-name">{job.company}</span>
        {job.salary_range && job.salary_range !== "Not Specified" && (
          <span className="job-salary">{job.salary_range}</span>
        )}
      </div>
      
      <p className="job-company-about">{job.company_about}</p>
      
      <div className="job-meta">
        {job.region && (
          <div className="job-meta-item">
            <span className="meta-label">Region:</span>
            <span className="meta-value">
              {Array.isArray(job.region) ? job.region.join(', ') : job.region}
            </span>
          </div>
        )}
        
        {job.apply_before && (
          <div className="job-meta-item">
            <span className="meta-label">Apply before:</span>
            <span className="meta-value">{job.apply_before}</span>
          </div>
        )}
      </div>
      
      {job.skills && job.skills.length > 0 && (
        <div className="job-skills">
          {job.skills.map((skill, index) => (
            <span key={index} className="skill-tag">{skill}</span>
          ))}
        </div>
      )}
      
      <div className="job-actions">
        <a href={job.apply_url} target="_blank" rel="noopener noreferrer" className="apply-btn">
          Apply Now
        </a>
        <button className="view-details-btn">View Details</button>
      </div>
    </div>
  );
}

export default JobCard;
