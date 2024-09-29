# Setting up on heroku

1. Add this buildpack "https://github.com/timanovsky/subdir-heroku-buildpack.git"
   - Add "Config Vars" of `PROJECT_PATH` as "/base-server-app"
   - This will enable it to build normally
2. Add "heroku/python" buildpack; It must be **after** the subdir buildpack
3. Define the `DJANGO_SETTINGS_MODULE` file to use in "Config Vars" eg "config.settings.staging"
   - If using prod please specify the `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
4. Include a `SUPER_ADMIN_PASS` in "Config Vars". That way you can login. See "init_super_user.py" for how it works
5. Include a `DJANGO_SECRET_KEY` for the Django setup in "Config Vars". See "dev.py" for an example. Do **not** use that one.
6. The database should automatically provision. Note it does cost money by default. This will setup the `DATABASE_URL` for you.

# Post Deploy

1. You probably need to run "python manage.py init_super_user" via the heroku bash unless you change the deploy script
