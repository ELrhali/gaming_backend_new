#!/bin/bash

# Script de backup automatique pour Gaming Backend
# À exécuter régulièrement via cron

# Variables
BACKUP_DIR="/home/gobackma/backup"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="gobackma_gaming_db"
DB_USER="gobackma_gaming_root"
DB_PASSWORD="VotreMotDePasseSecurisé123!"

# Créer le répertoire de backup s'il n'existe pas
mkdir -p $BACKUP_DIR

# Backup de la base de données
echo "Backup de la base de données..."
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME | gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Backup des fichiers media
echo "Backup des fichiers media..."
tar -czf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz /home/gobackma/public_html/backend/media/

# Garder seulement les 7 derniers backups
echo "Nettoyage des anciens backups..."
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime +7 -delete

echo "Backup terminé avec succès!"
