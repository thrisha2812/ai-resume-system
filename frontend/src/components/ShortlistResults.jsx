import React from 'react';
import { FiBriefcase, FiMail, FiCheck, FiAlertCircle, FiAlertTriangle } from 'react-icons/fi';

// --- 1. Component: Circular Progress Bar ---
const CircularScore = ({ score }) => {
  const radius = 30;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = "text-red-500";
  if (score > 75) color = "text-green-500";
  else if (score > 50) color = "text-yellow-500";

  return (
    <div className="relative flex items-center justify-center">
      <svg className="transform -rotate-90 w-20 h-20">
        <circle
          className="text-gray-200"
          strokeWidth="6"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="40"
          cy="40"
        />
        <circle
          className={`${color} transition-all duration-1000 ease-out`}
          strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="40"
          cy="40"
        />
      </svg>
      <span className={`absolute text-lg font-bold ${color}`}>
        {Math.round(score)}%
      </span>
    </div>
  );
};

// --- 2. Helper: Get Status Badge ---
const getStatusBadge = (score) => {
  if (score >= 80) {
    return <span className="px-3 py-1 text-xs font-bold text-white bg-green-600 rounded-full shadow-sm flex items-center gap-1"><FiCheck /> TOP CANDIDATE</span>;
  } else if (score >= 60) {
    return <span className="px-3 py-1 text-xs font-bold text-white bg-yellow-500 rounded-full shadow-sm">GOOD MATCH</span>;
  } else {
    return <span className="px-3 py-1 text-xs font-bold text-white bg-gray-400 rounded-full shadow-sm flex items-center gap-1"><FiAlertCircle /> LOW RELEVANCE</span>;
  }
};

const ShortlistResults = ({ results }) => {
  if (!results || results.length === 0) {
    return (
      <div className="mt-8 p-10 text-center bg-white rounded-xl border border-dashed border-gray-300 shadow-sm">
        <p className="text-gray-500 text-lg">No candidates analyzed yet.</p>
        <p className="text-sm text-gray-400 mt-1">Upload resumes and paste a JD to see results.</p>
      </div>
    );
  }

  return (
    <div className="mt-10">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-800">Ranked Candidates</h3>
        <span className="px-3 py-1 bg-blue-50 text-blue-700 text-sm font-semibold rounded-lg">
          {results.length} Found
        </span>
      </div>

      <div className="grid gap-6">
        {results.map((candidate, index) => (
          <div 
            key={index} 
            className="relative p-6 bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
          >
            {/* Rank Badge */}
            <div className="absolute top-4 left-4 w-8 h-8 flex items-center justify-center bg-gray-900 text-white font-bold rounded-full text-sm">
              #{index + 1}
            </div>

            <div className="flex flex-col md:flex-row items-center gap-6 pl-8">
              
              {/* Left: Score Circle */}
              <div className="flex-shrink-0">
                <CircularScore score={candidate.score} />
              </div>

              {/* Middle: Info */}
              <div className="flex-1 w-full">
                <div className="flex flex-wrap items-center gap-3 mb-1">
                  <h4 className="text-xl font-bold text-gray-900">{candidate.name}</h4>
                  {getStatusBadge(candidate.score)}
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-3 flex-wrap">
                  <span className="flex items-center gap-1"><FiMail className="text-blue-500"/> {candidate.email}</span>
                  <span className="flex items-center gap-1"><FiBriefcase className="text-purple-500"/> {candidate.years_of_experience} Years Exp</span>
                  
                  {/* ⚠️ MALPRACTICE ALERT (Moved here for better layout) ⚠️ */}
                  {candidate.is_suspicious && (
                    <span className="flex items-center px-3 py-1 text-xs font-bold text-red-700 bg-red-100 border border-red-300 rounded-full animate-pulse">
                      <FiAlertTriangle className="mr-1.5" />
                      SUSPICIOUS FORMATTING
                    </span>
                  )}
                </div>

                {/* Skills Grid */}
                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider mt-1">Matched:</span>
                  {candidate.matched_skills && candidate.matched_skills.length > 0 ? (
                    candidate.matched_skills.map(skill => (
                      <span key={skill} className="px-2 py-1 text-xs font-medium bg-green-50 text-green-700 border border-green-200 rounded-md">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-gray-400 italic">None</span>
                  )}
                </div>
              </div>

              {/* Right: Missing (Hidden on small screens) */}
              <div className="hidden md:block w-1/4 border-l pl-6 border-gray-100">
                <p className="text-xs font-semibold text-gray-400 uppercase mb-2">Missing Keywords</p>
                <div className="flex flex-wrap gap-1">
                  {candidate.missing_skills && candidate.missing_skills.slice(0, 5).map(skill => (
                    <span key={skill} className="px-2 py-0.5 text-[10px] font-medium bg-red-50 text-red-600 rounded-sm">
                      {skill}
                    </span>
                  ))}
                  {candidate.missing_skills.length > 5 && <span className="text-xs text-gray-400">+{candidate.missing_skills.length - 5} more</span>}
                </div>
              </div>

            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ShortlistResults;