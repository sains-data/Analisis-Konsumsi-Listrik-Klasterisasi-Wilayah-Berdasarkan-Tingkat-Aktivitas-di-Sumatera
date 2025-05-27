# Script untuk push ke GitHub
# Pastikan Git sudah terinstall terlebih dahulu
# https://git-scm.com/download/win

# Konfigurasi nama dan email (ubah dengan data Anda)
$GIT_USERNAME = "Nama Anda"
$GIT_EMAIL = "email@anda.com"
$REPO_URL = "https://github.com/sains-data/Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera.git"
$BRANCH = "main"

# Cek apakah Git terinstall
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Git tidak terinstall. Silakan install Git terlebih dahulu." -ForegroundColor Red
    Write-Host "Download dari: https://git-scm.com/download/win" -ForegroundColor Yellow
    Exit
}

# Membuat .gitignore untuk menghindari file yang tidak perlu di-push
$gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# Docker volumes dan cache
docker-volumes/
hadoop_namenode/
hadoop_datanode/
superset_db/
superset_home/
minio_data/

# System Files
.DS_Store
Thumbs.db
"@

# Fungsi untuk melakukan git push
function Push-GitRepository {
    # Set working directory ke Tubes ABD
    Set-Location "C:\Users\lenovo\Documents\Tubes ABD"
    
    Write-Host "🚀 Memulai proses push ke GitHub..." -ForegroundColor Blue
    
    # Konfigurasi git jika belum
    Write-Host "⚙️ Mengatur konfigurasi Git..." -ForegroundColor Yellow
    git config --global user.name $GIT_USERNAME
    git config --global user.email $GIT_EMAIL
    
    # Buat .gitignore
    Write-Host "📄 Membuat file .gitignore..." -ForegroundColor Yellow
    Set-Content -Path ".gitignore" -Value $gitignore
    
    # Cek apakah sudah ada git repository
    if (-not (Test-Path -Path ".git")) {
        Write-Host "📁 Initialisasi Git repository..." -ForegroundColor Yellow
        git init
    } else {
        Write-Host "📁 Git repository sudah ada" -ForegroundColor Green
    }
    
    # Cek remote
    $remote = git remote -v
    if ($remote -notcontains "origin") {
        Write-Host "🔗 Menambahkan remote origin..." -ForegroundColor Yellow
        git remote add origin $REPO_URL
    } else {
        Write-Host "🔗 Remote origin sudah ada" -ForegroundColor Green
    }
    
    # Add semua file
    Write-Host "➕ Menambahkan semua file ke staging area..." -ForegroundColor Yellow
    git add .
    
    # Commit
    Write-Host "📝 Melakukan commit..." -ForegroundColor Yellow
    git commit -m "Analisis Konsumsi Listrik: Bronze-Silver-Gold Layer dengan HDFS, Hive, Spark, dan Superset"
    
    # Pull dulu untuk menghindari konflik (optional, bisa dihapus jika repo baru)
    try {
        Write-Host "⬇️ Pull dulu dari repo remote..." -ForegroundColor Yellow
        git pull origin $BRANCH --allow-unrelated-histories
    } catch {
        Write-Host "⚠️ Branch belum ada di remote atau terjadi error pada pull" -ForegroundColor Yellow
    }
    
    # Push
    Write-Host "⬆️ Melakukan push ke GitHub..." -ForegroundColor Yellow
    git push -u origin $BRANCH
    
    Write-Host "✅ Selesai! Repository sudah di-push ke GitHub" -ForegroundColor Green
    Write-Host "🔗 $REPO_URL" -ForegroundColor Cyan
}

# Eksekusi fungsi
Push-GitRepository
