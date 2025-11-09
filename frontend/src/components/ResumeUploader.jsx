import React, { useState } from 'react';
import axios from 'axios';
import { FiUploadCloud, FiAlertCircle } from 'react-icons/fi';

const ResumeUploader = ({ setUploadMessage }) => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('No file selected');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setError('');
      setUploadMessage('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    
    setLoading(true);
    setError('');
    setUploadMessage('');

    const formData = new FormData();
    formData.append('resume', file);
    const token = localStorage.getItem('token');

    try {
      const res = await axios.post('http://localhost:5000/api/resume/upload', formData, {
        headers: {
          
          'Authorization': `Bearer ${token}`
        }
      });
      setUploadMessage(res.data.message);
      setFile(null);
      setFileName('No file selected');
    } catch (err) {
      setError(err.response?.data?.message || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label className="flex flex-col items-center justify-center w-full h-32 px-4 transition bg-white border-2 border-gray-300 border-dashed rounded-md appearance-none cursor-pointer hover:border-gray-400 focus:outline-none">
          <FiUploadCloud className="w-8 h-8 text-gray-400" />
          <span className="mt-2 text-sm text-gray-600 truncate">{fileName}</span>
          <span className="text-xs text-blue-500">Click to select a file (PDF or DOCX)</span>
          <input type="file" onChange={handleFileChange} accept=".pdf,.docx" className="hidden" />
        </label>
        
        <button 
          type="submit" 
          disabled={loading}
          className="w-full px-4 py-2 mt-4 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
        >
          {loading ? 'Uploading...' : 'Upload Resume'}
        </button>
      </form>
      {error && (
        <div className="flex items-center mt-2 text-sm text-red-600">
          <FiAlertCircle className="mr-1" /> {error}
        </div>
      )}
    </div>
  );
};

export default ResumeUploader;