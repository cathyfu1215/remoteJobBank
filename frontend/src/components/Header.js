import React from 'react';
import ThemeToggle from './ThemeToggle';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <h1>Remote Job Bank</h1>
        </div>
        <div className="header-right">
          <p>Find your next remote job</p>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}

export default Header;
