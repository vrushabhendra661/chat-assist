import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ChatService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async sendMessage(message, sessionId = 'default') {
    try {
      const response = await this.api.post('/api/chat', {
        message,
        session_id: sessionId,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async clearSession(sessionId = 'default') {
    try {
      const response = await this.api.post('/api/clear', {
        session_id: sessionId,
      });
      return response.data;
    } catch (error) {
      console.error('Error clearing session:', error);
      throw error;
    }
  }

  async getHistory(sessionId = 'default', limit = 50) {
    try {
      const response = await this.api.get(`/api/history/${sessionId}`, {
        params: { limit },
      });
      return response.data;
    } catch (error) {
      console.error('Error getting history:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await this.api.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
}

export default new ChatService();

