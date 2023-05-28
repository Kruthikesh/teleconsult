def create_admin(sender, **kwargs):
    from apps.user.models import BaseUser

    try:
        print("Checking if admin user details exists")
        user = BaseUser.objects.filter(email="admin@doctorapp.com", is_admin=True)
        if user:
            print("Admin user already exists")
            return

        BaseUser.objects.create_superuser(
            email="admin@doctorapp.com",
            password="admin",
            # is_email_verified=True,
            # is_active=True,
            # is_admin=True,
        )

        print("Ådmin user created")
        return
    except Exception as e:
        print("Exception occurred while checking/creating the admin")
        print(e)
        return