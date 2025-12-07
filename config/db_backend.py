"""
Custom MySQL backend pour contourner la vérification de version MariaDB
"""
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper


class DatabaseWrapper(MySQLDatabaseWrapper):
    """Wrapper qui désactive la vérification de version MariaDB"""
    
    def check_database_version_supported(self):
        """Désactiver la vérification de version pour MariaDB 10.4"""
        pass
