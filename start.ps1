# DetectAI - Start both servers
Write-Host "Starting DetectAI..." -ForegroundColor Cyan

# Backend
Write-Host "Starting FastAPI backend on http://localhost:8000" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 2

# Frontend
Write-Host "Starting Next.js frontend on http://localhost:3000" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "DetectAI running:" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "  API docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Add your Anthropic API key to backend/.env to enable the Humanizer" -ForegroundColor Magenta
