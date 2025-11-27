import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ResumeUploader from '../components/ResumeUploader';
import JobInputForm from '../components/JobInputForm';
import ShortlistResults from '../components/ShortlistResults';
import { FiLogOut, FiCpu } from 'react-icons/fi';

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
          
          {/* Card 1: Upload Resume */}
          <div className="bg-white p-8 rounded-lg shadow-xl h-fit">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">1. Update Resume</h2>
            <p className="text-gray-600 mb-6 text-sm">
              Upload your latest resume to help our AI generate relevant interview questions for you.
            </p>
            <ResumeUploader setUploadMessage={setUploadMessage} />
            {uploadMessage && (
              <div className="mt-6 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200">
                {uploadMessage}
              </div>
            )}
          </div>

          {/* Card 2: Mock Interview (RESTORED) */}
          <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-8 rounded-lg shadow-xl text-white flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-white/20 rounded-lg">
                  <FiCpu className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold">2. AI Mock Interview</h2>
              </div>
              <p className="mb-6 opacity-90 leading-relaxed">
                Ready to practice? Our AI will generate technical questions based on the skills found in your resume.
              </p>
              <ul className="list-disc pl-5 mb-8 text-sm opacity-80 space-y-2">
                <li>Customized Question Bank</li>
                <li>Real-time AI Feedback</li>
                <li>Performance Scoring</li>
              </ul>
            </div>
            
            <button 
              onClick={() => navigate('/interview/start')} 
              className="w-full py-3.5 bg-white text-blue-700 font-bold rounded-lg hover:bg-blue-50 transition shadow-lg flex items-center justify-center gap-2"
            >
              Start Interview Now
            </button>
          </div>

        </div>
      )}
    </div>
  );
};

export default Dashboard;