# Node.js Installation Checker
# Run this after installing Node.js to verify everything works

Write-Host "🔍 Checking Node.js Installation..." -ForegroundColor Cyan
Write-Host ""

# Check Node.js
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "✅ Node.js installed: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Node.js not found" -ForegroundColor Red
        Write-Host "   Please install from: https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
    Write-Host "   Please install from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>$null
    if ($npmVersion) {
        Write-Host "✅ npm installed: $npmVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ npm not found" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ npm not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 All prerequisites installed!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Next steps:" -ForegroundColor Cyan
Write-Host "   1. cd 'D:\clinic multi tennant SaaS'" -ForegroundColor White
Write-Host "   2. npm create vite@latest frontend -- --template react" -ForegroundColor White
Write-Host "   3. cd frontend" -ForegroundColor White
Write-Host "   4. npm install" -ForegroundColor White
Write-Host "   5. npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "⚡ Using Vite (10x faster than Create React App!)" -ForegroundColor Yellow
Write-Host ""

