# Nagaram - Civic Issue & Agriculture Platform

Nagaram is a full-stack Flask web application designed for civic issue reporting, community engagement, and agricultural advisory services.

## 🚀 Key Features

- **Civic Issue Management**: Citizen issue reporting, status tracking, NGO assignment, and volunteer coordination.
- **Agriculture Portal**: Advisory services for farmers, crop health guidance, scheme updates, market information, and weather insights.
- **Multi-Role Portals**: Tailored interfaces for Citizens, Farmers, NGOs, Volunteers, Experts, and Admins.
- **Responsive Web UI**: Built with modern HTML5, CSS3, and dynamic dashboard components.

## 📁 Project Structure

```text
nagaram/
├── api/                    # Vercel serverless deployment entrypoints
├── app/
│   ├── routes/             # Flask Blueprint routes (auth, citizen, farmer, ngo, volunteer, etc.)
│   ├── services/           # Business logic & services (issues, crops, market, weather, schemes)
│   ├── static/             # CSS styling, JavaScript scripts, and static images
│   ├── templates/          # HTML Jinja2 templates organized by user role
│   ├── utils/              # Helper functions and custom decorators
│   ├── __init__.py         # Flask app factory
│   └── models.py           # Database schemas
├── tests/                  # Unit and integration tests
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore configuration
├── config.py               # Application configuration settings
├── requirements.txt        # Python package dependencies
├── run.py                  # Entrypoint to run the development server
└── vercel.json             # Deployment settings for Vercel
```

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
```

### 5. Run the Application
```bash
python run.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

## 📦 What NOT to Upload to GitHub
- **`venv/`** (Virtual environment - contains thousands of installed library files)
- **`nagaram_dev.db`** (Local SQLite database)
- **`__pycache__/`** (Compiled Python bytecode)
- **`.env`** (Contains sensitive keys & secrets)

All of these are automatically ignored using the included `.gitignore` file.
