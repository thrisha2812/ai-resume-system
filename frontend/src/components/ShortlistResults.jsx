import React from 'react';
import { FiBriefcase, FiUser, FiMail } from 'react-icons/fi';
const ScoreBar = ({ score }) => {
  let bgColor = 'bg-red-500';
  if (score > 75) bgColor = 'bg-green-500';
  else if (score > 50) bgColor = 'bg-yellow-500';

  return (
    <div className="w-full bg-gray-200 rounded-full h-2.5">
      <div 
        className={`${bgColor} h-2.5 rounded-full`} 
        style={{ width: `${score}%` }}
      ></div>
    </div>
  );
};

const ShortlistResults = ({ results }) => {
  if (!results || results.length === 0) {
    return (
      <div className="mt-6 p-4 text-center bg-gray-50 rounded-lg">
        <p className="text-gray-600">No resumes found or analyzed. Uploaded resumes will be ranked here.</p>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Ranked Candidate Shortlist</h3>
      <div className="space-y-4">
        {results.map((candidate, index) => (
          <div key={index} className="p-4 border border-gray-200 rounded-lg bg-white shadow-sm">
            <div className="flex flex-col md:flex-row justify-between md:items-center mb-2">
              <h4 className="text-lg font-bold text-blue-700">{index + 1}. {candidate.name}</h4>
              <span className="flex items-center px-3 py-1 text-sm font-medium text-purple-700 bg-purple-100 rounded-full">
                    <FiBriefcase className="mr-1.5" />
                    {candidate.years_of_experience > 0 
                      ? `${candidate.years_of_experience} Years` 
                      : 'Exp: N/A'}
                  </span>
              <span className="text-sm text-gray-600">{candidate.email}</span>
            </div>
            
            <div className="flex items-center space-x-3 mb-3">
               <span className={`text-2xl font-bold ${candidate.score > 75 ? 'text-green-600' : (candidate.score > 50 ? 'text-yellow-600' : 'text-red-600')}`}>
                 {candidate.score.toFixed(1)}%
               </span>
               <ScoreBar score={candidate.score} />
            </div>

            {/* TODO (Thrisha/Kavya): Make this section look better! */}
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="font-semibold">Matched:</span>
              {candidate.matched_skills.slice(0, 5).map(skill => (
                <span key={skill} className="px-2 py-0.5 bg-green-100 text-green-800 rounded-full">{skill}</span>
              ))}
            </div>
             <div className="flex flex-wrap gap-2 text-xs mt-2">
              <span className="font-semibold">Missing:</span>
              {candidate.missing_skills.slice(0, 5).map(skill => (
                <span key={skill} className="px-2 py-0.5 bg-red-100 text-red-800 rounded-full">{skill}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ShortlistResults;