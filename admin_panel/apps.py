from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
    verbose_name = 'Panel Admin'

    def ready(self):
        # Safety: ensure STATIC_ROOT is never present in STATICFILES_DIRS.
        # This catches cases where other code or environment modifies settings after
        # the initial settings module execution (prevents Django E002 check).
        try:
            from django.conf import settings
            import os as _os
            sdirs = list(getattr(settings, 'STATICFILES_DIRS', []))
            sdirs = [p for p in sdirs if _os.path.abspath(str(p)) != _os.path.abspath(str(settings.STATIC_ROOT))]
            # assign back only if changed
            if sdirs != list(getattr(settings, 'STATICFILES_DIRS', [])):
                setattr(settings, 'STATICFILES_DIRS', sdirs)
        except Exception:
            # be silent on any failure to avoid breaking startup
            pass
