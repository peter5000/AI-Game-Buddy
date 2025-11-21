# AI Game Buddy

An intelligent gaming companion that provides real-time chat assistance and game analysis for multiplayer games. Built with FastAPI backend and supports various games including Chess, Tic-Tac-Toe, and Ultimate Tic-Tac-Toe.

## ✨ Features

- **Real-time Chat**: WebSocket-based chat system with AI-powered responses
- **Multi-Game Support**: Chess, Tic-Tac-Toe, Ultimate Tic-Tac-Toe
- **Room Management**: Create and join game rooms with multiple players
- **AI Integration**: Azure OpenAI integration for intelligent game assistance
- **User Management**: Account creation and authentication system
- **Real-time Updates**: Live game state synchronization across all players
- **Presence System**: Track online/offline status of players
- **Game Event Publishing**: Broadcast game moves and events to all room members

## 🏗️ Architecture

### Backend (FastAPI)
- **API Layer**: RESTful endpoints for game management, rooms, and user accounts
- **WebSocket Layer**: Real-time communication for chat and game updates
- **Services Layer**: 
  - AI Service (Azure OpenAI integration)
  - Game Service (multiple game engines)
  - Chat Service (message handling and AI responses)
  - Room Service (room management and player coordination)
  - User Service (authentication and user management)
  - Presence Service (online status tracking)
- **Storage**: Azure Cosmos DB, Azure Blob Storage, Redis for caching
- **Monitoring**: Azure Application Insights with OpenTelemetry

### Frontend
- Basic HTML/CSS/JavaScript interface
- WebSocket client for real-time communication

## 🎮 Supported Games

### Chess
- Full chess implementation using `python-chess`
- UCI move notation support
- Complete game state tracking
- Move history and validation

### Tic-Tac-Toe
- Classic 3x3 grid gameplay
- Turn-based mechanics
- Win condition detection

### Ultimate Tic-Tac-Toe
- 3x3 grid of Tic-Tac-Toe boards
- Advanced rule implementation
- Strategic gameplay mechanics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional)
- Azure account (for cloud services)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/AI-Game-Buddy.git
   cd AI-Game-Buddy
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_ENDPOINT=your_azure_openai_endpoint
   OPENAI_API_KEY=your_azure_openai_key
   COSMOS_DB_URL=your_cosmos_db_url
   COSMOS_DB_KEY=your_cosmos_db_key
   BLOB_STORAGE_CONNECTION_STRING=your_blob_storage_connection_string
   REDIS_URL=your_redis_url
   APPLICATIONINSIGHTS_CONNECTION_STRING=your_app_insights_connection_string
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Deployment

```bash
cd backend
docker-compose up --build
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `POST /accounts` - Create user account
- `GET /rooms` - List available rooms
- `POST /rooms` - Create a new room
- `POST /rooms/{room_id}/join` - Join a room
- `POST /games/{game_type}/start` - Start a new game
- `POST /games/{game_id}/move` - Make a game move

### WebSocket Endpoints
- `WS /ws/chat/{room_id}` - Real-time chat and game updates

## 🎯 Usage Examples

### Starting a Chess Game
```python
# Create a room
POST /rooms
{
  "name": "Chess Room",
  "game_type": "chess",
  "max_players": 2
}

# Join the room
POST /rooms/{room_id}/join

# Start the game
POST /games/chess/start
{
  "room_id": "room_id_here"
}

# Make a move
POST /games/{game_id}/move
{
  "move": "e2e4"
}
```

### Chat Integration
Connect to the WebSocket endpoint and send messages:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/room_id');
ws.send(JSON.stringify({
  "type": "chat_message",
  "content": "What's the best opening move in chess?"
}));
```

## 🛠️ Development

### Project Structure
```
AI-Game-Buddy/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration management
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── routers/             # API route handlers
│   │   │   ├── accounts_router.py
│   │   │   ├── chat_router.py
│   │   │   ├── game_router.py
│   │   │   └── room_router.py
│   │   └── services/            # Business logic services
│   │       ├── ai_service.py
│   │       ├── chat_service.py
│   │       ├── game_service.py
│   │       ├── room_service.py
│   │       └── games/           # Game implementations
│   │           ├── chess_game.py
│   │           ├── ttt.py
│   │           └── uttt/
│   ├── requirements.txt
│   └── docker-compose.yaml
└── frontend/
    ├── index.html
    ├── css/
    └── js/
```

### Adding New Games
1. Implement the game logic in `services/games/`
2. Extend the `GameSystem` interface
3. Define game-specific state and action models
4. Add routing in `game_router.py`

### Running Tests
```bash
# Add your test framework here
pytest  # (when tests are implemented)
```

## 🌐 Deployment

### Azure Container Apps
The project includes configuration for Azure Container Apps deployment:

1. **Build and push to Azure Container Registry**
   ```bash
   az acr build --registry myaigamingfriendregistry --image ai-game-buddy .
   ```

2. **Deploy to Container Apps**
   ```bash
   az containerapp update \
     --name myaigamingfriendcontainerjj \
     --resource-group my-ai-gaming-friend \
     --image myaigamingfriendregistry.azurecr.io/ai-game-buddy:latest
   ```

## 📄 License

This project is licensed under the [LICENSE](LICENSE) file in the repository.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests (when test framework is set up)
5. Submit a pull request

## 🔍 Troubleshooting

### Common Issues
- **WebSocket connection fails**: Check that the server is running and the WebSocket endpoint is correct
- **AI responses not working**: Verify Azure OpenAI credentials are properly configured
- **Game state not syncing**: Ensure Redis is running and properly configured

### Debug Mode
Run the application with debug logging:
```bash
uvicorn app.main:app --reload --log-level debug
```

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the application logs for detailed error messages
- Verify all environment variables are properly set
