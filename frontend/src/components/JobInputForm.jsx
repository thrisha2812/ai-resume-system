import React, { useState } from 'react';
import axios from 'axios';

const JobInputForm = ({ setResults, setLoading }) => {
  const [jobDescription, setJobDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      // No token needed anymore
      const res = await axios.post('http://localhost:5000/api/resume/analyze', 
        { job_description: jobDescription }
      );
      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="jd" className="block text-sm font-medium text-gray-700 mb-1">
        Paste Job Description
      </label>
      <textarea
        id="jd"
        rows="10"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        placeholder="Paste the full job description here..."
        className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      
      <div className="mt-4">
        <button 
            type="submit" 
            className="w-full px-6 py-3 font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700 transition"
        >
            Analyze & Shortlist Candidates
        </button>
      </div>
    </form>
  );
};

export default JobInputForm;