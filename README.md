# Health Information System

A modern, secure, and efficient health information management system built with Flask, Vue.js, and Redis.

## Features

- **Secure Authentication**: JWT-based authentication with password hashing
- **Client Management**: CRUD operations for client health records
- **Caching**: Redis-based caching for improved performance
- **RESTful API**: Clean, well-documented API endpoints
- **Modern Frontend**: Vue.js-based user interface
- **Comprehensive Testing**: Unit and integration tests

## Tech Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Redis (Caching)
- JWT (Authentication)
- pytest (Testing)

### Frontend
- Vue.js
- Vuex (State Management)
- Axios (HTTP Client)
- Vue Router
- Vuetify (UI Framework)

## Project Structure

```
health-info-sys/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── extensions.py
│   │   └── __init__.py
│   ├── tests/
│   ├── requirements.txt
│   └── config.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   ├── router/
│   │   └── App.vue
│   ├── package.json
│   └── README.md
└── README.md
```

## Setup and Installation

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_APP=app
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export REDIS_URL=redis://localhost:6379/0
```

4. Initialize database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run tests:
```bash
pytest
```

6. Start the server:
```bash
flask run
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run serve
```

## API Documentation

### Authentication

- `POST /api/v1/auth/login`: User login
- `POST /api/v1/auth/register`: User registration

### Clients

- `GET /api/v1/clients`: List all clients
- `POST /api/v1/clients`: Create new client
- `GET /api/v1/clients/<id>`: Get client details
- `PUT /api/v1/clients/<id>`: Update client
- `DELETE /api/v1/clients/<id>`: Delete client

## Testing

The project includes comprehensive test coverage:

- Unit tests for models
- API endpoint tests
- Cache functionality tests
- Integration tests

Run tests with:
```bash
pytest backend/tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 