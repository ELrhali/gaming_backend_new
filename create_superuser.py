from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@goback.ma', 'admin123')
    print("✓ Superutilisateur créé:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: admin@goback.ma")
else:
    print("✓ Superutilisateur 'admin' existe déjà")
