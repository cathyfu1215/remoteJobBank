import React from 'react';
import JobCard from './JobCard';
import './JobList.css';

function JobList({ jobs }) {
  return (
    <div className="job-list">
      {jobs.map(job => (
        <JobCard key={job.job_id} job={job} />
      ))}
    </div>
  );
}

export default JobList;
