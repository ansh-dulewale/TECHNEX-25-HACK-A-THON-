import React, { useState } from 'react';
import axios from 'axios';
import './styles.css';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    // Convert FileList to array and set to state
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    // Ensure exactly 4 files are selected
    if (selectedFiles.length !== 4) {
      alert('Please upload exactly 4 videos.');
      return;
    }

    const formData = new FormData();
    // Append all selected files to FormData
    selectedFiles.forEach(file => formData.append('videos', file));

    try {
      // Use only the environment variable for the backend URL
      const BACKEND_URL = ${"https://traffic-backend.onrender.com/upload"};
      if (!BACKEND_URL) {
        throw new Error('Backend URL is not configured. Please set REACT_APP_BACKEND_URL.');
      }
      const response = await axios.post(`${BACKEND_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
      console.log('Response from backend:', response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error uploading files:', error);
      setResult({ error: 'Failed to process videos. Please try again or check the backend.' });
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">🚗 AI-Based Traffic Management</h1>
      <hr className="w-full border-gray-300 mb-6" />

      <div className="w-full max-w-4xl flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-1/2">
          <section id="hero" className="hero bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 className="text-2xl font-semibold text-green-600 mb-2">🚦 Optimize Traffic Flow with AI 🤖</h2>
            <p className="text-gray-700">Enhance your city's traffic management with our smart adaptive system. Our technology optimizes traffic light timings based on real-time data to reduce congestion and improve traffic flow.</p>
          </section>
          <section id="upload" className="upload bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold text-blue-600 mb-2">📹 Upload Your Traffic Videos</h2>
            <p className="text-gray-700 mb-4">Select 4 videos showing different roads at an intersection. Our system will analyze these videos to provide optimized traffic light timings for smoother traffic flow.</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input 
                type="file" 
                multiple 
                accept="video/*" 
                onChange={handleFileChange} 
                className="w-full p-2 border border-gray-300 rounded-md"
              />
              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                Run Model {loading && '...'}
              </button>
            </form>
          </section>
        </div>

        <section id="result" className="result w-full md:w-1/2 bg-white p-6 rounded-lg shadow-md">
          {!loading && !result && (
            <p className="text-gray-500 text-center">Optimization results will show here <br /><span className="text-green-500">🚦🚦🚦🚦</span></p>
          )}
          {loading && <p className="text-blue-500 text-center">Processing videos, it may take a few minutes...</p>}
          {result && !result.error && (
            <>
              <h2 className="text-2xl font-semibold text-green-600 mb-4">✅ Optimization Results</h2>
              <p className="text-gray-700 mb-4">Your traffic light timings have been optimized. Here are the recommended green times for each direction:</p>
              <ul className="list-disc pl-5 space-y-2">
                <li className="text-gray-800">🚦 North: <span id="north-time" className="font-bold text-blue-600">{result.north || 'N/A'}</span> seconds</li>
                <li className="text-gray-800">🚦 South: <span id="south-time" className="font-bold text-blue-600">{result.south || 'N/A'}</span> seconds</li>
                <li className="text-gray-800">🚦 West: <span id="west-time" className="font-bold text-blue-600">{result.west || 'N/A'}</span> seconds</li>
                <li className="text-gray-800">🚦 East: <span id="east-time" className="font-bold text-blue-600">{result.east || 'N/A'}</span> seconds</li>
              </ul>
            </>
          )}
          {result && result.error && (
            <div className="text-red-600 text-center">
              <h2 className="text-2xl font-semibold mb-2">❌ Error</h2>
              <p>{result.error}</p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;
