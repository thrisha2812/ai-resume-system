import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ResumeUploader from '../components/ResumeUploader';
import JobInputForm from '../components/JobInputForm';
import ShortlistResults from '../components/ShortlistResults';
// We are ignoring MockInterviewStart for now
import { FiLogOut } from 'react-icons/fi';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    } else {
      navigate('/'); // Not logged in
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    navigate('/');
  };

  if (!user) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Welcome, {user.name}</h1>
        <button
          onClick={handleLogout}
          className="flex items-center px-4 py-2 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 transition"
        >
          <FiLogOut className="mr-2" />
          Logout
        </button>
      </header>
      
      {user.role === 'recruiter' ? (
        // --- Recruiter View ---
        <div className="bg-white p-6 rounded-lg shadow-xl">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">Recruiter Dashboard: Resume Shortlister</h2>
          <JobInputForm setResults={setResults} setLoading={setLoading} />
          {loading && <p className="mt-4 text-center text-blue-600">Analyzing resumes... this may take a moment.</p>}
          {results && <ShortlistResults results={results} />}
        </div>
      ) : (
        // --- Candidate View ---
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-xl">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Upload Your Resume</h2>
            <p className="text-sm text-gray-600 mb-4">Upload your latest resume (PDF or DOCX) to be parsed by our system.</p>
            <ResumeUploader setUploadMessage={setUploadMessage} />
            {uploadMessage && <p className="mt-4 text-sm text-green-600">{uploadMessage}</p>}
          </div>
          <div className="bg-white p-6 rounded-lg shadow-xl">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Mock Interview</h2>
            <p className="text-gray-600">The mock interview module is under construction.</p>
            {/* MockInterviewStart component will go here */}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;