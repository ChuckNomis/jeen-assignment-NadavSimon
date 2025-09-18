import React, { useState } from 'react';
import './Message.css';

const Message = ({ message }) => {
  const { type, content, timestamp, toolsUsed, contextChunks, dbResults, isError } = message;
  const [showChunks, setShowChunks] = useState(false);

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message ${type} ${isError ? 'error' : ''}`}>
      <div className="message-avatar">
        {type === 'user' ? (
          <div className="user-avatar">U</div>
        ) : (
          <div className="assistant-avatar">AI</div>
        )}
      </div>
      
      <div className="message-content">
        <div className="message-text">
          {content}
        </div>
        
        {/* Show tools used if any */}
        {toolsUsed && toolsUsed.length > 0 && (
          <div className="message-metadata">
            <div className="tools-used">
              <strong>Tools used:</strong> {toolsUsed.join(', ')}
            </div>
          </div>
        )}
        
        {/* Show context chunks if any */}
        {contextChunks && contextChunks.length > 0 && (
          <div className="message-metadata">
            <div className="context-info">
              <div className="context-header">
                <strong>Sources:</strong> Found {contextChunks.length} relevant document(s)
                <button 
                  className="toggle-chunks-btn"
                  onClick={() => setShowChunks(!showChunks)}
                >
                  {showChunks ? 'Hide Sources' : 'Show Sources'}
                </button>
              </div>
              
              {showChunks && (
                <div className="chunks-container">
                  {contextChunks.map((chunk, index) => (
                    <div key={index} className="chunk-item">
                      <div className="chunk-header">
                        <div className="chunk-title-group">
                          <span className="chunk-title">Source {index + 1}</span>
                          <span className="chunk-source">
                            {chunk.metadata?.source || 
                             chunk.source || 
                             chunk.metadata?.filename ||
                             chunk.filename ||
                             'Unknown Document'}
                          </span>
                        </div>
                        {chunk.metadata?.page && (
                          <span className="chunk-page">
                            Page {chunk.metadata.page}
                          </span>
                        )}
                      </div>
                      <div className="chunk-content">
                        {chunk.page_content || chunk.content || JSON.stringify(chunk)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Show database results if any */}
        {dbResults && dbResults.length > 0 && (
          <div className="message-metadata">
            <div className="db-info">
              <strong>Database:</strong> Found {dbResults.length} record(s)
            </div>
          </div>
        )}
        
        <div className="message-time">
          {formatTime(timestamp)}
        </div>
      </div>
    </div>
  );
};

export default Message;
