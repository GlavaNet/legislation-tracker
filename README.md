# Legislation Tracker

Track federal and state legislation and executive orders.

## Features
- Real-time tracking of legislation
- Advanced search capabilities
- Data visualization
- Mobile-first design

## Prerequisites
- Python 3.8+
- Node.js 14+
- SQLite3

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/glavanet/legislation-tracker.git
cd legislation-tracker
```

2. Start with Docker:
```bash
docker-compose up
```

Or manually:

Backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm start
```

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
