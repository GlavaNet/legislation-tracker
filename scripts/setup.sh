#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error handling
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo -e "${RED}\"${last_command}\" command failed with exit code $?.${NC}"' EXIT

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print section header
print_section() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
}

# Initial setup
print_section "Initial Setup"

# Create necessary directories
mkdir -p backend/logs
mkdir -p backend/data
mkdir -p frontend/build
mkdir -p scripts/templates

# Check system requirements
print_section "Checking System Requirements"

REQUIRED_COMMANDS=(
    "python3"
    "node"
    "npm"
    "git"
    "sqlite3"
)

for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if ! command_exists "$cmd"; then
        echo -e "${RED}$cmd is required but not installed.${NC}"
        exit 1
    fi
done

echo -e "${GREEN}All required commands are available.${NC}"

# Create Python Package Structure
print_section "Creating Python Package Structure"

# Create all required directories if they don't exist
mkdir -p backend/app/models
mkdir -p backend/app/api
mkdir -p backend/app/scrapers
mkdir -p backend/tests

# Create __init__.py files
INIT_FILES=(
    "backend/app/__init__.py"
    "backend/app/models/__init__.py"
    "backend/app/api/__init__.py"
    "backend/app/scrapers/__init__.py"
    "backend/tests/__init__.py"
)

for init_file in "${INIT_FILES[@]}"; do
    if [ ! -f "$init_file" ]; then
        echo "Creating $init_file"
        # Add version info to root __init__.py
        if [ "$init_file" = "backend/app/__init__.py" ]; then
            cat > "$init_file" << EOF
"""
Legislation Tracker Backend
"""
__version__ = '0.1.0'
EOF
        elif [ "$init_file" = "backend/app/models/__init__.py" ]; then
            cat > "$init_file" << EOF
from .models import Legislation, LegislativeAction, LegislationType, Status, Base

__all__ = [
    'Legislation',
    'LegislativeAction',
    'LegislationType',
    'Status',
    'Base'
]
EOF
        else
            touch "$init_file"
        fi
        echo -e "${GREEN}Created $init_file${NC}"
    else
        echo -e "${YELLOW}$init_file already exists${NC}"
    fi
done

# Create models.py with model definitions
echo "Creating models.py..."
cat > "backend/app/models/models.py" << 'EOF'
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class LegislationType(str, enum.Enum):
    """Type of legislation"""
    FEDERAL = "federal"
    STATE = "state"
    EXECUTIVE = "executive"

class Status(str, enum.Enum):
    """Status of legislation"""
    ACTIVE = "active"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SIGNED = "signed"
    VETOED = "vetoed"

class LegislativeAction(Base):
    """Model for tracking legislative actions"""
    __tablename__ = "legislative_actions"

    id = Column(String, primary_key=True)
    legislation_id = Column(String, ForeignKey('legislation.id'), nullable=False)
    action_date = Column(DateTime, nullable=False)
    action_type = Column(String, nullable=False)
    description = Column(String)
    extra_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship back to the legislation
    legislation = relationship("Legislation", back_populates="actions")

    def __repr__(self):
        return f"<LegislativeAction {self.action_type} on {self.action_date}>"

class Legislation(Base):
    """Model for legislation data"""
    __tablename__ = "legislation"

    id = Column(String, primary_key=True)
    type = Column(SQLEnum(LegislationType), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String)
    status = Column(SQLEnum(Status))
    introduced_date = Column(DateTime)
    last_action_date = Column(DateTime)
    source_url = Column(String)
    extra_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationship to actions
    actions = relationship("LegislativeAction", back_populates="legislation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Legislation(id={self.id}, type={self.type}, title={self.title})>"

    @property
    def current_status(self) -> str:
        """Get the current status of the legislation"""
        return self.status.value if self.status else "unknown"

    @property
    def days_since_introduction(self) -> int:
        """Calculate days since introduction"""
        if not self.introduced_date:
            return 0
        delta = func.now() - self.introduced_date
        return delta.days

    @property
    def days_since_last_action(self) -> int:
        """Calculate days since last action"""
        if not self.last_action_date:
            return 0
        delta = func.now() - self.last_action_date
        return delta.days

    def add_action(self, action_type: str, description: str, extra_data: dict = None) -> LegislativeAction:
        """Add a new action to this legislation"""
        from uuid import uuid4
        
        action = LegislativeAction(
            id=str(uuid4()),
            legislation_id=self.id,
            action_type=action_type,
            description=description,
            extra_data=extra_data or {},
            action_date=func.now()
        )
        self.actions.append(action)
        self.last_action_date = action.action_date
        return action

    def update_status(self, new_status: Status) -> None:
        """Update the status and record it as an action"""
        old_status = self.status
        self.status = new_status
        
        if old_status != new_status:
            self.add_action(
                action_type="status_change",
                description=f"Status changed from {old_status} to {new_status}",
                extra_data={"old_status": old_status, "new_status": new_status}
            )
EOF

# Backend setup
print_section "Setting up Backend"

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create env.py template
print_section "Creating Alembic Configuration"

# Create env.py template if it doesn't exist
if [ ! -f "../scripts/templates/env.py" ]; then
    echo "Creating Alembic env.py template..."
    cat > "../scripts/templates/env.py" << 'EOF'
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add the app directory to the Python path
current_path = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(app_path)

from app.models import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << EOF
# Database settings
DATABASE_URL=sqlite:///./legislation.db

# API settings
API_V1_STR=/api/v1
PROJECT_NAME="Legislation Tracker"

# API Keys
CONGRESS_API_KEY=
NY_LEGISLATURE_API_KEY=
CA_LEGISLATURE_API_KEY=

# External API URLs
CONGRESS_API_BASE_URL=https://api.congress.gov/v3

# Rate limiting
RATELIMIT_STORAGE_URL=memory://
DEFAULT_RATE_LIMIT=100/minute

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
EOF
    echo -e "${GREEN}Created .env file. Please update it with your configurations.${NC}"
fi

print_section "Cleaning Up Database Files"

# Remove old database and migration files
if [ -f "legislation.db" ]; then
    echo "Removing old database..."
    rm legislation.db
fi

if [ -d "migrations" ]; then
    echo "Removing old migrations..."
    rm -rf migrations
fi

if [ -f "alembic.ini" ]; then
    echo "Removing old alembic config..."
    rm -f alembic.ini
fi

print_section "Initializing Database"

# Initialize Alembic if not already initialized
if [ ! -f "alembic.ini" ]; then
    echo "Initializing Alembic..."
    alembic init migrations
    
    # Configure alembic.ini
    sed -i 's|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = sqlite:///./legislation.db|' alembic.ini
    
    # Copy our env.py template
    cp ../scripts/templates/env.py migrations/env.py
fi

# Create initial migration
echo "Creating initial migration..."
alembic revision --autogenerate -m "initial"

# Run migrations
echo "Running migrations..."
alembic upgrade head

cd ..

# Frontend setup
print_section "Setting up Frontend"

cd frontend

# Install Node.js dependencies
if [ -f "package-lock.json" ]; then
    echo "Installing from package-lock.json..."
    npm ci
else
    echo "Installing dependencies..."
    npm install --ignore-scripts
fi

# Install and initialize husky if we're in a git repository
if [ -d "../.git" ]; then
    echo "Installing husky..."
    npm install husky --save-dev
    npx husky install
fi

# Create frontend environment file
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo "VITE_API_URL=http://localhost:8000" > .env
    echo "VITE_API_VERSION=v1" >> .env
    echo -e "${GREEN}Created frontend .env file.${NC}"
fi

cd ..

# Git hooks setup
print_section "Setting up Git Hooks"

# Create git hooks directory if it doesn't exist
mkdir -p .git/hooks

# Install pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Run backend tests
cd backend
source venv/bin/activate
python -m pytest
if [ $? -ne 0 ]; then
    echo "Backend tests failed. Commit aborted."
    exit 1
fi

# Run frontend tests
cd ../frontend
npm test -- --watchAll=false
if [ $? -ne 0 ]; then
    echo "Frontend tests failed. Commit aborted."
    exit 1
fi

# Run linting
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Commit aborted."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit

# Final setup steps
print_section "Setup Complete"

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "\nTo start the development servers:"
echo -e "1. Backend: ${YELLOW}cd backend && source venv/bin/activate && uvicorn app.main:app --reload${NC}"
echo -e "2. Frontend: ${YELLOW}cd frontend && npm start${NC}"
echo -e "\nImportant Notes:"
echo -e "1. Update ${YELLOW}backend/.env${NC} with your API keys:"
echo -e "   - CONGRESS_API_KEY (required)"
echo -e "   - NY_LEGISLATURE_API_KEY (optional)"
echo -e "   - CA_LEGISLATURE_API_KEY (optional)"
echo -e "2. You can also use ${YELLOW}./scripts/dev.sh${NC} to start both servers"

# Print API registration information
print_section "API Registration Information"
echo -e "To get your API keys, register at:"
echo -e "1. Congress.gov API: ${YELLOW}https://api.congress.gov/sign-up/${NC}"
echo -e "2. State Legislature APIs vary by state. Check individual state websites."

# Remove error handling trap
trap - EXIT

exit 0
