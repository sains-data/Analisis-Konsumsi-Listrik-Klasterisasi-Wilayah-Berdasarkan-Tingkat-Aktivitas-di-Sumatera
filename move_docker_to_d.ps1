# Script untuk memindahkan lokasi data Docker ke drive D
# Harus dijalankan sebagai Administrator

# Stop Docker service
Write-Host "Stopping Docker services..." -ForegroundColor Yellow
Stop-Service *docker*

# Membuat direktori baru untuk data Docker di drive D jika belum ada
$newDockerPath = "D:\DockerDesktop\Data"
if (-Not (Test-Path -Path $newDockerPath)) {
    Write-Host "Creating new Docker data directory at $newDockerPath" -ForegroundColor Blue
    New-Item -ItemType Directory -Path $newDockerPath -Force
}

# Ambil lokasi default direktori data Docker
$defaultDockerPath = "$env:ProgramData\Docker"
Write-Host "Default Docker data path: $defaultDockerPath" -ForegroundColor Cyan

# Salin docker settings ke lokasi baru jika belum ada
if (-Not (Test-Path -Path "$newDockerPath\config\daemon.json")) {
    Write-Host "Creating Docker config directory structure..." -ForegroundColor Blue
    New-Item -ItemType Directory -Path "$newDockerPath\config" -Force
    
    # Buat atau update daemon.json dengan data-root baru
    $daemonConfig = @{
        "data-root" = "$newDockerPath";
        "registry-mirrors" = @();
    } | ConvertTo-Json

    Set-Content -Path "$newDockerPath\config\daemon.json" -Value $daemonConfig
}

# Salin file daemon.json ke lokasi default config untuk Docker
Write-Host "Updating Docker daemon configuration..." -ForegroundColor Blue
if (-Not (Test-Path -Path "$defaultDockerPath\config")) {
    New-Item -ItemType Directory -Path "$defaultDockerPath\config" -Force
}

$daemonConfig = @{
    "data-root" = "$newDockerPath";
    "registry-mirrors" = @();
} | ConvertTo-Json

Set-Content -Path "$defaultDockerPath\config\daemon.json" -Value $daemonConfig

Write-Host "Docker data directory configured to: $newDockerPath" -ForegroundColor Green
Write-Host "Please restart Docker Desktop manually." -ForegroundColor Yellow
Write-Host ""
Write-Host "PENTING: Setelah Docker restart, verifikasi perubahan dengan menjalankan:" -ForegroundColor Magenta
Write-Host "docker info | Select-String 'Docker Root Dir'" -ForegroundColor White
