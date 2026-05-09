import { useState } from 'react';
import api from '../services/api';

function ChatbotPage() {
  const chatbotEnabled = import.meta.env.VITE_ENABLE_CHATBOT !== 'false';
  const [message, setMessage] = useState('How can I improve in probability?');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!chatbotEnabled) {
    return (
      <div className="card">
        <div className="page-header">
          <h2 className="page-title">Tutor Chatbot</h2>
          <p className="page-subtitle">
            Chatbot is disabled in this deployment profile. Other AI modules remain fully available.
          </p>
        </div>
        <div className="success">Use recommendations, planner, prediction, and adaptive modules for viva demo flow.</div>
      </div>
    );
  }

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setError('');
    try {
      const userMessage = { role: 'user', text: message };
      setChat((prev) => [...prev, userMessage]);

      const { data } = await api.post('/chatbot/', {
        message,
        student_context: { goal: 'improve weak topics', pace: 'moderate' },
      });

      setChat((prev) => [...prev, { role: 'assistant', text: data.reply }]);
      setMessage('');
    } catch (err) {
      setError(err.userMessage || 'Unable to send message right now.');
      setChat((prev) => [
        ...prev,
        { role: 'assistant', text: 'Tutor is temporarily unavailable. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="page-header">
        <h2 className="page-title">Tutor Chatbot</h2>
        <p className="page-subtitle">Ask questions and get concise, practical study guidance.</p>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="card chat-box">
        {chat.map((item, index) => (
          <p className="chat-line" key={`${item.role}-${index}`}>
            <span className={`bubble ${item.role === 'user' ? 'user' : 'assistant'}`}>
              <strong>{item.role === 'user' ? 'You' : 'Tutor'}:</strong> {item.text}
            </span>
          </p>
        ))}
        {chat.length === 0 && <p className="empty-state">Start a conversation with your tutor.</p>}
      </div>

      <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={4} />
      <button className="btn-primary" onClick={sendMessage} disabled={loading}>
        {loading ? 'Thinking...' : 'Send'}
      </button>
    </div>
  );
}

export default ChatbotPage;
