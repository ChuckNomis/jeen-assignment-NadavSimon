# AI Multi-Search Assistant - React Client

A ChatGPT-like interface for the AI Multi-Search Assistant that connects to your FastAPI server.

## Features

- **ChatGPT-style Interface**: Clean, modern chat interface with dark theme
- **Real-time Chat**: Send messages and receive responses from your AI assistant
- **Loading States**: Visual feedback while processing requests
- **Error Handling**: Graceful error handling with user-friendly messages
- **Tool Usage Display**: Shows which tools were used (RAG search, database queries)
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-resize Input**: Text area automatically adjusts to content

## Quick Start

1. **Start the FastAPI server** (from the server directory):

   ```bash
   cd ../server
   python main.py
   ```

2. **Start the React client** (from this directory):

   ```bash
   npm start
   ```

3. **Open your browser** to `http://localhost:3000`

## Usage

- Type your question in the input box at the bottom
- Press Enter or click the send button to send your message
- The assistant will respond and show any tools used
- You can ask about:
  - AI and technology policy (uses document search)
  - User account information (uses database queries)
  - General questions (uses AI knowledge)

## Configuration

The client connects to your FastAPI server at `http://localhost:8000` by default. You can change this by modifying the `API_BASE_URL` in `src/services/api.js`.

## Project Structure

```
src/
├── components/
│   ├── ChatInterface.js    # Main chat component
│   ├── MessageList.js      # Message container
│   ├── Message.js          # Individual message component
│   ├── InputBox.js         # Message input component
│   ├── LoadingIndicator.js # Loading animation
│   └── *.css              # Component styles
├── services/
│   └── api.js             # API service for server communication
└── App.js                 # Main app component
```

## Dependencies

- React 19.1.1
- Axios for HTTP requests
- CSS modules for styling

## Development

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
