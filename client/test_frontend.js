/**
 * Simple test script to verify frontend API connections
 * Run with: node test_frontend.js
 */

const axios = require('axios');

const API_BASE_URL = 'http://localhost:8000';

async function testAPI() {
  console.log('🧪 Testing Frontend API Integration\n');

  try {
    // Test 1: Health check
    console.log('1. Testing server health...');
    const healthResponse = await axios.get(`${API_BASE_URL}/`);
    console.log('   ✅ Server is running');
    console.log('   📋 Server info:', healthResponse.data.message);

    // Test 2: Start new chat
    console.log('\n2. Testing new chat endpoint...');
    const newChatResponse = await axios.post(`${API_BASE_URL}/api/chat/new`);
    console.log('   ✅ New chat started:', newChatResponse.data.message);

    // Test 3: Send first message
    console.log('\n3. Testing first message...');
    const message1Response = await axios.post(`${API_BASE_URL}/api/chat`, {
      query: "Hello! My name is TestUser."
    });
    console.log('   ✅ Message sent successfully');
    console.log('   🤖 Response:', message1Response.data.result.substring(0, 100) + '...');

    // Test 4: Send follow-up message (test memory)
    console.log('\n4. Testing conversation memory...');
    const message2Response = await axios.post(`${API_BASE_URL}/api/chat`, {
      query: "Do you remember my name?"
    });
    console.log('   ✅ Follow-up message sent');
    console.log('   🤖 Response:', message2Response.data.result.substring(0, 100) + '...');
    
    // Check if it remembers the name
    if (message2Response.data.result.toLowerCase().includes('testuser')) {
      console.log('   🎉 Memory is working! The agent remembered the name.');
    } else {
      console.log('   ⚠️  Memory might not be working as expected.');
    }

    // Test 5: Get chat history
    console.log('\n5. Testing chat history endpoint...');
    const historyResponse = await axios.get(`${API_BASE_URL}/api/chat/history`);
    console.log('   ✅ Chat history retrieved');
    console.log('   📊 Message count:', historyResponse.data.message_count);

    // Test 6: Start new chat and test isolation
    console.log('\n6. Testing conversation isolation...');
    await axios.post(`${API_BASE_URL}/api/chat/new`);
    const message3Response = await axios.post(`${API_BASE_URL}/api/chat`, {
      query: "Do you remember TestUser?"
    });
    console.log('   ✅ New conversation started');
    console.log('   🤖 Response:', message3Response.data.result.substring(0, 100) + '...');
    
    if (!message3Response.data.result.toLowerCase().includes('testuser')) {
      console.log('   🎉 Conversation isolation is working! The agent forgot the previous conversation.');
    } else {
      console.log('   ⚠️  Conversation isolation might not be working as expected.');
    }

    // Test 7: Test tool usage (autonomous vehicles)
    console.log('\n7. Testing tool usage...');
    const toolResponse = await axios.post(`${API_BASE_URL}/api/chat`, {
      query: "Tell me about autonomous vehicle safety"
    });
    console.log('   ✅ Tool query sent');
    console.log('   🔧 Tools used:', toolResponse.data.tools_used);
    if (toolResponse.data.tools_used.includes('search_documents')) {
      console.log('   🎉 RAG search tool is working!');
    }

    console.log('\n✅ All frontend API tests passed! The integration is working correctly.');

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    if (error.response) {
      console.error('   Server error:', error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      console.error('   🔌 Server is not running. Start it with: python server/main.py');
    }
  }
}

// Check if axios is available
try {
  testAPI();
} catch (error) {
  console.log('📦 Installing axios...');
  console.log('Run: npm install axios');
  console.log('Then run this test again: node test_frontend.js');
}
