# Script d'initialisation du projet PC Store
# PowerShell Script

Write-Host "=== Initialisation du projet PC Store ===" -ForegroundColor Green
Write-Host ""

# Vérifier Python
Write-Host "Vérification de Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel
Write-Host ""
Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
python -m venv venv

# Activer l'environnement virtuel
Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Installer les dépendances
Write-Host ""
Write-Host "Installation des dépendances..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Créer les dossiers nécessaires
Write-Host ""
Write-Host "Création des dossiers média et statique..." -ForegroundColor Yellow
$folders = @(
    "media",
    "media\categories",
    "media\subcategories",
    "media\products",
    "media\products\gallery",
    "media\collections",
    "static",
    "staticfiles"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "  ✓ Créé: $folder" -ForegroundColor Green
    } else {
        Write-Host "  - Existe déjà: $folder" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=== Configuration de la base de données ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Avant de continuer, assurez-vous que:" -ForegroundColor Yellow
Write-Host "  1. MySQL est installé et en cours d'exécution" -ForegroundColor White
Write-Host "  2. Vous avez créé la base de données 'pc_store_db'" -ForegroundColor White
Write-Host "  3. Vous avez configuré les identifiants dans config/settings.py" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Voulez-vous continuer avec les migrations? (O/N)"
if ($continue -eq "O" -or $continue -eq "o") {
    Write-Host ""
    Write-Host "Création des migrations..." -ForegroundColor Yellow
    python manage.py makemigrations
    
    Write-Host ""
    Write-Host "Application des migrations..." -ForegroundColor Yellow
    python manage.py migrate
    
    Write-Host ""
    Write-Host "Création du superutilisateur..." -ForegroundColor Yellow
    Write-Host "Entrez les informations pour le compte admin:" -ForegroundColor Cyan
    python manage.py createsuperuser
    
    Write-Host ""
    Write-Host "=== Installation terminée avec succès! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour démarrer le serveur:" -ForegroundColor Cyan
    Write-Host "  python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Write-Host "Interface admin accessible à:" -ForegroundColor Cyan
    Write-Host "  http://127.0.0.1:8000/admin-panel/login/" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Installation des dépendances terminée." -ForegroundColor Green
    Write-Host "Complétez la configuration de la base de données puis exécutez:" -ForegroundColor Yellow
    Write-Host "  python manage.py makemigrations" -ForegroundColor White
    Write-Host "  python manage.py migrate" -ForegroundColor White
    Write-Host "  python manage.py createsuperuser" -ForegroundColor White
    Write-Host "  python manage.py runserver" -ForegroundColor White
    Write-Host ""
}
