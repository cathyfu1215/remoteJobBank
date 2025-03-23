import React from 'react';
import './Loading.css';

function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p>Loading jobs...</p>
    </div>
  );
}

export default Loading;
