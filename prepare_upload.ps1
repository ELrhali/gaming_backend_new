# Script PowerShell pour préparer et transférer les fichiers vers Nidohost
# Usage: .\prepare_upload.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Préparation Upload vers Nidohost - Backend  " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$BackendDir = "C:\Users\MSI\Desktop\gaming\gaming_backend"
$ExportDir = "C:\Users\MSI\Desktop\gaming_export"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Créer le répertoire d'export
Write-Host "[1/5] Création du répertoire d'export..." -ForegroundColor Yellow
if (Test-Path $ExportDir) {
    Remove-Item $ExportDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ExportDir | Out-Null
Write-Host "  ✓ Répertoire créé: $ExportDir" -ForegroundColor Green

# Export de la base de données
Write-Host ""
Write-Host "[2/5] Export de la base de données MySQL..." -ForegroundColor Yellow
$DbBackupFile = "$ExportDir\gaming_db_backup_$Timestamp.sql"

# Vérifier si MySQL est disponible
$mysqlDump = Get-Command mysqldump -ErrorAction SilentlyContinue
if ($mysqlDump) {
    Write-Host "  Entrez le mot de passe MySQL root:" -ForegroundColor Cyan
    mysqldump -u root -p gaming_db > $DbBackupFile
    
    if (Test-Path $DbBackupFile) {
        $dbSize = (Get-Item $DbBackupFile).Length / 1MB
        Write-Host "  ✓ Base de données exportée: $([math]::Round($dbSize, 2)) MB" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Échec de l'export de la base de données" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ mysqldump non trouvé. Installez MySQL ou exportez manuellement." -ForegroundColor Red
}

# Compression des fichiers media
Write-Host ""
Write-Host "[3/5] Compression des fichiers media..." -ForegroundColor Yellow
$MediaSource = "$BackendDir\media"
$MediaZip = "$ExportDir\media_$Timestamp.zip"

if (Test-Path $MediaSource) {
    Compress-Archive -Path "$MediaSource\*" -DestinationPath $MediaZip -CompressionLevel Optimal
    
    if (Test-Path $MediaZip) {
        $mediaSize = (Get-Item $MediaZip).Length / 1MB
        Write-Host "  ✓ Fichiers media compressés: $([math]::Round($mediaSize, 2)) MB" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Échec de la compression des fichiers media" -ForegroundColor Red
    }
} else {
    Write-Host "  ! Aucun dossier media trouvé" -ForegroundColor Yellow
}

# Créer un fichier d'instructions
Write-Host ""
Write-Host "[4/5] Création du fichier d'instructions..." -ForegroundColor Yellow

$Instructions = @"
========================================================
  INSTRUCTIONS DE TRANSFERT - gaming BACKEND
========================================================

Date: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")

📦 FICHIERS À TRANSFÉRER:
--------------------------
1. gaming_db_backup_$Timestamp.sql  → Base de données
2. media_$Timestamp.zip             → Fichiers media

🔐 INFORMATIONS SERVEUR:
--------------------------
IP:       178.63.126.247
Username: gobackma
Password: 3`$lL_L3J~UU*

📋 ÉTAPES SUR LE SERVEUR:
--------------------------

1. CONNEXION SSH:
   ssh gobackma@178.63.126.247

2. IMPORT BASE DE DONNÉES:
   cd /home/gobackma
   mysql -u gobackma_gaming_user -p gobackma_gaming_db < gaming_db_backup_$Timestamp.sql
   rm gaming_db_backup_$Timestamp.sql

3. EXTRACTION MEDIA:
   mkdir -p /home/gobackma/public_html/backend/media
   unzip media_$Timestamp.zip -d /home/gobackma/public_html/backend/media/
   rm media_$Timestamp.zip
   chmod -R 755 /home/gobackma/public_html/backend/media

4. REDÉMARRAGE:
   sudo supervisorctl restart gaming

🌐 MÉTHODES DE TRANSFERT:
--------------------------

Option A - WinSCP (Recommandé):
1. Télécharger: https://winscp.net/
2. Protocole: SFTP
3. Hôte: 178.63.126.247
4. Port: 22
5. Nom d'utilisateur: gobackma
6. Mot de passe: 3`$lL_L3J~UU*

Option B - FileZilla:
1. Télécharger: https://filezilla-project.org/
2. Protocole: SFTP
3. Hôte: sftp://178.63.126.247
4. Utilisateur: gobackma
5. Mot de passe: 3`$lL_L3J~UU*
6. Port: 22

Option C - SCP (PowerShell):
scp gaming_db_backup_$Timestamp.sql gobackma@178.63.126.247:/home/gobackma/
scp media_$Timestamp.zip gobackma@178.63.126.247:/home/gobackma/

📝 NOTES:
--------------------------
- Les fichiers sont dans: $ExportDir
- Utilisez WinSCP ou FileZilla pour un transfert facile
- Suivez le guide complet: DEPLOIEMENT_NIDOHOST.md
- Guide rapide: GUIDE_RAPIDE.md

========================================================
"@

$InstructionsFile = "$ExportDir\INSTRUCTIONS.txt"
$Instructions | Out-File -FilePath $InstructionsFile -Encoding UTF8
Write-Host "  ✓ Fichier d'instructions créé" -ForegroundColor Green

# Résumé
Write-Host ""
Write-Host "[5/5] Résumé des fichiers créés:" -ForegroundColor Yellow
Write-Host "  📁 Répertoire: $ExportDir" -ForegroundColor White
Get-ChildItem $ExportDir | ForEach-Object {
    $size = $_.Length / 1MB
    Write-Host "     - $($_.Name) ($([math]::Round($size, 2)) MB)" -ForegroundColor White
}

# Ouvrir le répertoire d'export
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ✓ Préparation terminée avec succès!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Ouvrez le dossier: $ExportDir" -ForegroundColor White
Write-Host "  2. Lisez: INSTRUCTIONS.txt" -ForegroundColor White
Write-Host "  3. Utilisez WinSCP ou FileZilla pour transférer" -ForegroundColor White
Write-Host "  4. Suivez les instructions sur le serveur" -ForegroundColor White
Write-Host ""

# Ouvrir l'explorateur
Write-Host "Ouverture du dossier..." -ForegroundColor Yellow
Start-Process explorer.exe $ExportDir

# Ouvrir le fichier d'instructions
Start-Process notepad.exe $InstructionsFile

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
