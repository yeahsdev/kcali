import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

// 우리가 만들 페이지 컴포넌트들을 import 합니다.
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';

function App() {
  return (
    <div>
      {/* 이 부분은 페이지 이동을 위한 임시 링크입니다. */}
      <nav>
        <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/dashboard">Dashboard</Link>
      </nav>
      <hr />

      {/* URL 경로에 따라 어떤 페이지를 보여줄지 결정하는 부분입니다. */}
      <Routes>
        <Route path="/" element={<h2>Home Page</h2>} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}

export default App;