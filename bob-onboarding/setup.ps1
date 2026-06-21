# Repo Accelerate - Quick Setup Script for Windows
# This script automates the initial setup process

Write-Host "🤖 Repo Accelerate - Setup Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Found Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Backend Setup
Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "--------------------" -ForegroundColor Cyan

Set-Location backend

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping creation..." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r ..\requirements.txt
Write-Host "✓ Python dependencies installed" -ForegroundColor Green

# Setup .env file
if (Test-Path ".env") {
    Write-Host ".env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit backend/.env and add your Google Gemini API key!" -ForegroundColor Red
    Write-Host "   GEMINI_API_KEY=your_actual_api_key_here" -ForegroundColor Yellow
}

Set-Location ..

# Frontend Setup
Write-Host ""
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "--------------------" -ForegroundColor Cyan

Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
Write-Host "✓ Node.js dependencies installed" -ForegroundColor Green

Set-Location ..

# Summary
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env and add your Google Gemini API key" -ForegroundColor White
Write-Host "2. Start the backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "3. In a new terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Open http://localhost:5173 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "For debugging in VS Code:" -ForegroundColor Yellow
Write-Host "- Press F5 and select 'Full Stack: Backend + Frontend'" -ForegroundColor White
Write-Host ""
Write-Host "📖 See DEVELOPMENT.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""

# Made with Repo Accelerate
