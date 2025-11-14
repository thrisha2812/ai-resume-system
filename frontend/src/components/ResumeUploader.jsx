import { useState } from 'react';
import axios from 'axios';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [parsedData, setParsedData] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file type
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(selectedFile.type)) {
        setMessage('Please upload a PDF or DOCX file');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setMessage('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    // Get token from localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('You must be logged in to upload a resume');
      return;
    }

    setLoading(true);
    setMessage('');

    const formData = new FormData();
    // IMPORTANT: Backend expects 'resume', not 'file'
    formData.append('resume', file);

    try {
      const response = await axios.post(
        'http://localhost:5000/api/resume/upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setMessage(response.data.message || 'Resume uploaded successfully!');
      setParsedData(response.data.data);
      setFile(null);
      // Reset file input
      e.target.reset();
    } catch (error) {
      console.error('Upload error:', error);
      
      if (error.response) {
        // Server responded with error
        setMessage(error.response.data.message || 'Upload failed');
      } else if (error.request) {
        // Request made but no response
        setMessage('No response from server. Please check if backend is running.');
      } else {
        // Something else happened
        setMessage('Error: ' + error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Upload Resume</h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Resume (PDF or DOCX)
            </label>
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.docx"
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100
                cursor-pointer"
            />
          </div>

          {file && (
            <div className="text-sm text-gray-600">
              Selected: <span className="font-medium">{file.name}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={!file || loading}
            className={`w-full py-2 px-4 rounded-md font-medium text-white
              ${!file || loading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
              } transition-colors duration-200`}
          >
            {loading ? 'Uploading...' : 'Upload Resume'}
          </button>
        </form>

        {message && (
          <div className={`mt-4 p-4 rounded-md ${
            message.includes('success') || message.includes('successfully')
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}>
            {message}
          </div>
        )}

        {parsedData && (
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 className="text-lg font-semibold mb-3 text-gray-800">Parsed Resume Data</h3>
            <div className="space-y-2 text-sm">
              {parsedData.name && (
                <p><span className="font-medium">Name:</span> {parsedData.name}</p>
              )}
              {parsedData.email && (
                <p><span className="font-medium">Email:</span> {parsedData.email}</p>
              )}
              {parsedData.phone && (
                <p><span className="font-medium">Phone:</span> {parsedData.phone}</p>
              )}
              {parsedData.skills && parsedData.skills.length > 0 && (
                <div>
                  <span className="font-medium">Skills:</span>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {parsedData.skills.map((skill, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResumeUploader;