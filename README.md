# Legislation Tracker

A web application for tracking federal and state legislation and executive orders.

## Features

- Track federal legislation from Congress.gov
- Monitor state-level legislation
- Follow executive orders from the Federal Register
- Real-time search and filtering
- Mobile-first responsive design
- Dark mode support

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Docker and Docker Compose (optional)
- Git

## Required API Keys

Before running the application, you'll need to obtain the following API keys:

1. **Congress.gov API**
   - Register at: https://api.congress.gov/sign-up/
   - Required for federal legislation data
   - Rate limit: 1000 requests per hour

2. **State Legislature APIs** (Optional)
   - Requirements vary by state
   - Some states only offer web scraping
   - Check individual state legislature websites for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/glavanet/legislation-tracker.git
cd legislation-tracker
```

2. Set up environment files:
```bash
# Backend environment
cp backend/.env.example backend/.env

# Frontend environment
cp frontend/.env.example frontend/.env
```

3. Configure API keys in backend/.env:
```env
CONGRESS_API_KEY=your_api_key_here
NY_LEGISLATURE_API_KEY=your_optional_key_here
CA_LEGISLATURE_API_KEY=your_optional_key_here
```

4. Run the setup script:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Development

Start the development servers:

```bash
./scripts/dev.sh
```

This will start:
- Backend server at http://localhost:8000
- Frontend server at http://localhost:3000
- API documentation at http://localhost:8000/docs

## Docker Deployment

1. Build and start containers:
```bash
docker-compose up -d
```

2. Stop containers:
```bash
docker-compose down
```

## Project Structure

```
legislation-tracker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   └── scrapers/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── utils/
│   └── tests/
└── scripts/
```

## Data Sources and Rate Limits

### Congress.gov
- API key required
- 1000 requests per hour
- Tracks federal legislation

### Federal Register
- No API key required
- 1000 requests per hour
- Tracks executive orders

### State Legislatures
- Varies by state
- Some require API keys
- Some only allow web scraping
- Rate limits vary

## Configuration

### Backend Configuration

Update `backend/.env`:
```env
# Required
CONGRESS_API_KEY=your_api_key_here

# Optional
DATABASE_URL=sqlite:///./legislation.db
API_V1_STR=/api/v1
```

### Frontend Configuration

Update `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_API_VERSION=v1
```

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## API Documentation

Once running, view the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Rate Limiting and Caching

The application implements:
- API rate limiting
- Response caching
- Concurrent request limiting

Configure these in `backend/app/config.py`:
```python
RATELIMIT_STORAGE_URL = "memory://"
DEFAULT_RATE_LIMIT = "100/minute"
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Follow coding standards
4. Add tests for new features
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Security

- Never commit API keys
- Use environment variables
- Keep dependencies updated
- Follow security best practices

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Troubleshooting

### Common Issues

1. API Rate Limits
```python
# Check current usage
curl -H "X-Api-Key: your_key" https://api.congress.gov/v3/market-data/usage
```

2. Missing API Keys
```bash
# Verify environment variables
echo $CONGRESS_API_KEY
```

3. Database Migrations
```bash
# Reset database
cd backend
alembic downgrade base
alembic upgrade head
```

## Support

- GitHub Issues: Project issues and feature requests
- Documentation: Check the /docs directory
- Email: support@example.com

## Roadmap

- Additional state legislature support
- Enhanced search capabilities
- Real-time updates
- Mobile application
