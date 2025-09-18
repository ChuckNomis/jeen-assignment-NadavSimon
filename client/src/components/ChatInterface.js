import React, { useState, useRef, useEffect } from 'react';
import MessageList from './MessageList';
import InputBox from './InputBox';
import { sendMessage, startNewChat, getChatHistory } from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m your AI Multi-Search Assistant. How can I help you?',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStartingNewChat, setIsStartingNewChat] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(message);
      
      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.result,
        timestamp: new Date(),
        toolsUsed: response.tools_used,
        contextChunks: response.context_chunks,
        dbResults: response.db_results
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = async () => {
    setIsStartingNewChat(true);
    try {
      await startNewChat();
      
      // Reset messages to initial state
      setMessages([
        {
          id: Date.now(),
          type: 'assistant',
          content: 'Hello! I\'m your AI Multi-Search Assistant. How can I help you?',
          timestamp: new Date()
        }
      ]);
    } catch (error) {
      console.error('Error starting new chat:', error);
      // Add error message
      const errorMessage = {
        id: Date.now(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while starting a new chat. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsStartingNewChat(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>AI Multi-Search Assistant</h1>
        <button 
          className="new-chat-button"
          onClick={handleNewChat}
          disabled={isStartingNewChat || isLoading}
          title="Start a new conversation (clears memory)"
        >
          {isStartingNewChat ? 'Starting...' : '🔄 New Chat'}
        </button>
      </div>
      
      <div className="chat-container">
        <MessageList 
          messages={messages} 
          isLoading={isLoading}
        />
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-container">
        <InputBox 
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};

export default ChatInterface;
