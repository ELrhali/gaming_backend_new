# Déploiement Gaming Backend

Ce document décrit comment déployer le backend Gaming.

1. Placer le fichier nginx_gaming.conf dans /etc/nginx/sites-available/gaming
2. Placer le fichier supervisor_gaming.conf dans /etc/supervisor/conf.d/gaming.conf
3. Adapter le fichier .env.gaming selon votre environnement
4. Redémarrer nginx et supervisor
5. Vérifier le fonctionnement avec verify_deployment.sh
