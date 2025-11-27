import React, { useState, useEffect } from 'react';
import { FiBriefcase, FiMail, FiCheck, FiAlertCircle, FiAlertTriangle, FiFilter, FiArrowDown } from 'react-icons/fi';

// --- 1. Circular Progress Component (Keep as is) ---
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
        <circle className="text-gray-200" strokeWidth="6" stroke="currentColor" fill="transparent" r={radius} cx="40" cy="40" />
        <circle className={`${color} transition-all duration-1000 ease-out`} strokeWidth="6" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" stroke="currentColor" fill="transparent" r={radius} cx="40" cy="40" />
      </svg>
      <span className={`absolute text-lg font-bold ${color}`}>{Math.round(score)}%</span>
    </div>
  );
};

const getStatusBadge = (score) => {
  if (score >= 80) return <span className="px-3 py-1 text-xs font-bold text-white bg-green-600 rounded-full shadow-sm flex items-center gap-1"><FiCheck /> TOP CANDIDATE</span>;
  else if (score >= 60) return <span className="px-3 py-1 text-xs font-bold text-white bg-yellow-500 rounded-full shadow-sm">GOOD MATCH</span>;
  else return <span className="px-3 py-1 text-xs font-bold text-white bg-gray-400 rounded-full shadow-sm flex items-center gap-1"><FiAlertCircle /> LOW RELEVANCE</span>;
};

const ShortlistResults = ({ results }) => {
  const [filteredResults, setFilteredResults] = useState(results);
  const [minScore, setMinScore] = useState(0);
  const [minExp, setMinExp] = useState(0);
  const [sortBy, setSortBy] = useState('score'); // 'score' or 'exp'

  // --- FILTERING LOGIC ---
  useEffect(() => {
    if (!results) return;

    let processed = results.filter(c => 
      c.score >= minScore && 
      c.years_of_experience >= minExp
    );

    if (sortBy === 'score') {
      processed.sort((a, b) => b.score - a.score);
    } else if (sortBy === 'exp') {
      processed.sort((a, b) => b.years_of_experience - a.years_of_experience);
    }

    setFilteredResults(processed);
  }, [results, minScore, minExp, sortBy]);

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
      <div className="flex flex-col md:flex-row items-center justify-between mb-6 gap-4">
        <h3 className="text-2xl font-bold text-gray-800">
          Shortlist <span className="text-sm font-normal text-gray-500 ml-2">({filteredResults.length} visible)</span>
        </h3>
        
        {/* --- FILTER CONTROL BAR --- */}
        <div className="flex flex-wrap gap-3 bg-gray-50 p-2 rounded-lg border border-gray-200">
          
          {/* Score Filter */}
          <div className="flex items-center gap-2 px-3 border-r border-gray-300">
            <span className="text-xs font-bold text-gray-500 uppercase">Min Score:</span>
            <input 
              type="range" min="0" max="90" step="10" 
              value={minScore} onChange={(e) => setMinScore(Number(e.target.value))}
              className="w-24 accent-blue-600 cursor-pointer"
            />
            <span className="text-sm font-bold text-blue-600">{minScore}%</span>
          </div>

          {/* Experience Filter */}
          <div className="flex items-center gap-2 px-3 border-r border-gray-300">
            <span className="text-xs font-bold text-gray-500 uppercase">Min Exp:</span>
            <select 
              value={minExp} onChange={(e) => setMinExp(Number(e.target.value))}
              className="text-sm bg-white border border-gray-300 rounded px-1 py-0.5 focus:outline-none"
            >
              <option value="0">Any</option>
              <option value="1">1+ Yrs</option>
              <option value="3">3+ Yrs</option>
              <option value="5">5+ Yrs</option>
            </select>
          </div>

          {/* Sort Dropdown */}
          <div className="flex items-center gap-2 px-3">
            <span className="text-xs font-bold text-gray-500 uppercase"><FiFilter className="inline mr-1"/>Sort By:</span>
            <select 
              value={sortBy} onChange={(e) => setSortBy(e.target.value)}
              className="text-sm font-semibold text-gray-700 bg-transparent focus:outline-none cursor-pointer"
            >
              <option value="score">Highest Score</option>
              <option value="exp">Most Experience</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid gap-6">
        {filteredResults.map((candidate, index) => (
          <div key={index} className="relative p-6 bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            
            {/* Rank Badge (Based on filtered list) */}
            <div className="absolute top-4 left-4 w-8 h-8 flex items-center justify-center bg-gray-900 text-white font-bold rounded-full text-sm">
              #{index + 1}
            </div>

            <div className="flex flex-col md:flex-row items-center gap-6 pl-8">
              <div className="flex-shrink-0"><CircularScore score={candidate.score} /></div>

              <div className="flex-1 w-full">
                <div className="flex flex-wrap items-center gap-3 mb-1">
                  <h4 className="text-xl font-bold text-gray-900">{candidate.name}</h4>
                  {getStatusBadge(candidate.score)}
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-3 flex-wrap">
                  <span className="flex items-center gap-1"><FiMail className="text-blue-500"/> {candidate.email}</span>
                  <span className="flex items-center gap-1"><FiBriefcase className="text-purple-500"/> {candidate.years_of_experience} Years Exp</span>
                  
                  {candidate.is_suspicious && (
                    <span className="flex items-center px-3 py-1 text-xs font-bold text-red-700 bg-red-100 border border-red-300 rounded-full animate-pulse">
                      <FiAlertTriangle className="mr-1.5" /> SUSPICIOUS FORMATTING
                    </span>
                  )}
                </div>

                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider mt-1">Matched:</span>
                  {candidate.matched_skills && candidate.matched_skills.length > 0 ? (
                    candidate.matched_skills.map(skill => (
                      <span key={skill} className="px-2 py-1 text-xs font-medium bg-green-50 text-green-700 border border-green-200 rounded-md">{skill}</span>
                    ))
                  ) : <span className="text-xs text-gray-400 italic">None</span>}
                </div>
              </div>

              <div className="hidden md:block w-1/4 border-l pl-6 border-gray-100">
                <p className="text-xs font-semibold text-gray-400 uppercase mb-2">Missing Keywords</p>
                <div className="flex flex-wrap gap-1">
                  {candidate.missing_skills && candidate.missing_skills.slice(0, 5).map(skill => (
                    <span key={skill} className="px-2 py-0.5 text-[10px] font-medium bg-red-50 text-red-600 rounded-sm">{skill}</span>
                  ))}
                  {candidate.missing_skills.length > 5 && <span className="text-xs text-gray-400">+{candidate.missing_skills.length - 5} more</span>}
                </div>
              </div>
            </div>
          </div>
        ))}
        {filteredResults.length === 0 && (
          <div className="text-center py-10 text-gray-400">No candidates match your filters.</div>
        )}
      </div>
    </div>
  );
};

export default ShortlistResults;