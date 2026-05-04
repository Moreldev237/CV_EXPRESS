import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import components
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import VerifyOTP from './components/VerifyOTP';
import Dashboard from './components/Dashboard';
import CVBuilder from './components/CVBuilder';
import CoverLetterBuilder from './components/CoverLetterBuilder';
import Profile from './components/Profile';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-otp" element={<VerifyOTP />} />
          <Route
            path="/dashboard"
            element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
          />
          <Route
            path="/cv-builder"
            element={<ProtectedRoute><CVBuilder /></ProtectedRoute>}
          />
          <Route
            path="/cover-letter-builder"
            element={<ProtectedRoute><CoverLetterBuilder /></ProtectedRoute>}
          />
          <Route
            path="/profile"
            element={<ProtectedRoute><Profile /></ProtectedRoute>}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
