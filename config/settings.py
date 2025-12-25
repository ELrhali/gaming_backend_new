"""
Django settings for Goback project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# PyMySQL setup pour remplacer mysqlclient
import pymysql
pymysql.install_as_MySQLdb()
# Forcer la version pour éviter l'erreur de version
pymysql.version_info = (2, 2, 1, "final", 0)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production-k8$x9@3n#v&2h5j')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'


# Configuration stricte pour la production
ALLOWED_HOSTS = [
    "api.gobag.ma",
    "www.api.gobag.ma",
    "localhost",
    "127.0.0.1",
    "192.168.3.55",
]



# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Doit être avant django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    
    # Custom apps
    'shop',
    'orders',
    'admin_panel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS doit être avant CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'config.db_backend',  # Utiliser notre backend personnalisé
        'NAME': os.getenv('DB_NAME', 'goback_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Casablanca'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))

# Seulement inclure le dossier static s'il existe
_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

# Media files (uploads)
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://goback-frontend-11uj.vercel.app",
    "https://www.gobag.ma",
    "http://192.168.3.55:3000",
    "https://gobag.ma",
    "https://www.gobag.ma",
]

# ALLOWED_HOSTS : uniquement les domaines backend
ALLOWED_HOSTS = [
    "api.gobag.ma",
    "www.api.gobag.ma",
    "localhost",
    "127.0.0.1",
    "192.168.3.55",
]
CORS_ALLOW_ALL_ORIGINS = False


# CSRF settings pour api.gobag.ma
CSRF_TRUSTED_ORIGINS = ['https://api.gobag.ma']

# Configuration pour proxy inverse (reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True


# Cookies sécurisés en production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Login URLs
LOGIN_URL = '/admin-panel/login/'
LOGIN_REDIRECT_URL = '/admin-panel/dashboard/'
LOGOUT_REDIRECT_URL = '/admin-panel/login/'

# Jazzmin settings - Interface admin moderne et claire
JAZZMIN_SETTINGS = {
    # Titres et branding
    "site_title": "Goback Admin",
    "site_header": "Administration de Goback",
    "site_brand": "Goback Admin",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bienvenue dans le panneau d'administration",
    "copyright": "Goback © 2025",
    "search_model": ["shop.Product", "shop.Category", "shop.Brand", "orders.Order"],
    
    # Top Menu
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Voir le site", "url": "https://gobag.ma", "new_window": True},
        {"model": "auth.User"},
        {"app": "shop"},
    ],
    
    # User Menu
    "usermenu_links": [
        {"name": "Voir le site", "url": "https://gobag.ma", "new_window": True},
        {"model": "auth.user", "icon": "fas fa-user"},
    ],
    
    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Ordre des apps dans le menu
    "order_with_respect_to": ["shop", "orders", "auth", "admin_panel"],
    
    # Icônes FontAwesome pour chaque section
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        "shop": "fas fa-store",
        "shop.Product": "fas fa-gamepad",
        "shop.Category": "fas fa-folder",
        "shop.SubCategory": "fas fa-folder-open",
        "shop.Brand": "fas fa-trademark",
        "shop.Collection": "fas fa-layer-group",
        "shop.ProductModel": "fas fa-cube",
        "shop.HeroSlide": "fas fa-images",
        
        "orders": "fas fa-shopping-cart",
        "orders.Order": "fas fa-shopping-cart",
        "orders.OrderItem": "fas fa-list",
        "orders.Customer": "fas fa-user-circle",
        "orders.Shipping": "fas fa-truck",
    },
    
    # Labels personnalisés pour les apps
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Liens personnalisés dans le menu
    "custom_links": {
        "shop": [{
            "name": "Statistiques Produits",
            "url": "admin:shop_product_changelist",
            "icon": "fas fa-chart-bar",
        }]
    },
    
    # Options de formulaire
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "shop.product": "horizontal_tabs",
    },
    
    # Langue
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    # Tailles de texte
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    
    # Couleurs du thème
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    
    # Barre de navigation
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    
    # Sidebar (menu latéral)
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    
    # Thèmes
    "theme": "flatly",
    "dark_mode_theme": "cyborg",
    
    # Button classes
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    
    # Actions
    "actions_sticky_top": True,
    
    # Custom CSS
    "custom_css": "admin/css/custom_admin.css",
}
