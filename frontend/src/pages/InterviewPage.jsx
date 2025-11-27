import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FiCpu, FiUser, FiSend, FiArrowRight, FiCheckCircle } from 'react-icons/fi';

const InterviewPage = () => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [finished, setFinished] = useState(false);
  const navigate = useNavigate();

  // 1. Load Questions on Start
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        // No Auth needed (Public API)
        const res = await axios.get('http://localhost:5000/api/interview/start');
        setQuestions(res.data.questions);
        setLoading(false);
      } catch (err) {
        alert("Could not start interview. Make sure Backend is running.");
        navigate('/dashboard');
      }
    };
    fetchQuestions();
  }, [navigate]);

  // 2. Submit Answer
  const handleSubmit = async () => {
    if (!userAnswer.trim()) return;

    try {
      const currentQ = questions[currentIndex];
      const res = await axios.post('http://localhost:5000/api/interview/submit', {
        user_answer: userAnswer,
        ideal_answer: currentQ.ideal_answer
      });
      setFeedback(res.data); // { score: 85.5, feedback: "Good job..." }
    } catch (err) {
      console.error(err);
      alert("Error submitting answer.");
    }
  };

  // 3. Next Question
  const handleNext = () => {
    setFeedback(null);
    setUserAnswer('');
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setFinished(true);
    }
  };

  if (loading) return <div className="flex h-screen items-center justify-center text-xl">🤖 AI is preparing your interview...</div>;

  // 4. Summary Screen (End of Interview)
  if (finished) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="bg-white p-10 rounded-xl shadow-xl text-center max-w-lg">
          <FiCheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Interview Complete!</h2>
          <p className="text-gray-600 mb-6">You have completed the AI technical round.</p>
          <button onClick={() => navigate('/dashboard')} className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex];

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg overflow-hidden">
        
        {/* Header */}
        <div className="bg-blue-600 p-6 text-white flex justify-between items-center">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <FiCpu /> AI Interview
          </h2>
          <span className="bg-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
            Question {currentIndex + 1} / {questions.length}
          </span>
        </div>

        {/* Question Area */}
        <div className="p-8">
          <div className="mb-6">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wide">
              {currentQ.type} Question • {currentQ.skill}
            </span>
            <h3 className="text-2xl font-bold text-gray-800 mt-2 leading-snug">
              {currentQ.question}
            </h3>
          </div>

          {/* Answer Area (Hide if feedback exists) */}
          {!feedback ? (
            <div className="animate-fade-in">
              <textarea
                className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none text-lg"
                placeholder="Type your answer here..."
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
              ></textarea>
              <button
                onClick={handleSubmit}
                className="mt-4 w-full bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2 transition"
              >
                <FiSend /> Submit Answer
              </button>
            </div>
          ) : (
            /* Feedback Area (Show after submit) */
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <span className="text-gray-500 font-medium">AI Evaluation</span>
                <span className={`text-2xl font-bold ${feedback.score > 70 ? 'text-green-600' : 'text-orange-500'}`}>
                  {feedback.score}% Score
                </span>
              </div>
              
              <p className="text-gray-700 mb-4">{feedback.feedback}</p>
              
              {/* Show Ideal Answer if score is low */}
              {feedback.score < 70 && (
                <div className="mb-6 bg-yellow-50 p-3 rounded border-l-4 border-yellow-400">
                  <p className="text-xs text-yellow-800 font-bold uppercase mb-1">Suggested Answer:</p>
                  <p className="text-sm text-gray-700 italic">"{currentQ.ideal_answer}"</p>
                </div>
              )}

              <button
                onClick={handleNext}
                className="w-full bg-gray-900 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-800 flex items-center justify-center gap-2 transition"
              >
                Next Question <FiArrowRight />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InterviewPage;