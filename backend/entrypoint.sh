#!/bin/sh
set -e

wait_for_mariadb() {
    maxcounter=60  # seconds
    DB_HOST=$(python manage.py shell \
        -c 'from django.conf import settings; print(settings.DATABASES["default"]["HOST"])')
    DB_USER=$(python manage.py shell \
        -c 'from django.conf import settings; print(settings.DATABASES["default"]["USER"])')
    DB_PASSWORD=$(python manage.py shell \
        -c 'from django.conf import settings; print(settings.DATABASES["default"]["PASSWORD"])')

    counter=1
    while ! mysql --protocol TCP -h${DB_HOST} -u${DB_USER} --password="${DB_PASSWORD}" -e "show databases;" > /dev/null 2>&1; do
        sleep 1
        counter=`expr $counter + 1`
        if [ $counter -gt $maxcounter ]; then
            >&2 echo "ERROR: we have unsucesfully waited >$maxcounter seconds for MySQL :-("
            exit 1
        fi;
    done
    echo ".. the database is now ready to accept connections (waited for $counter seconds) :-)\n"
}

# TODO: databases should also be up-and-running when using 'run --rm' cmd
if [ "$1" = 'uwsgi' ]; then
    echo "\nI'm waiting for the database to accept connections.."
    wait_for_mariadb
fi

if [ ! -d log ]; then
    mkdir log
fi

# 1. Each container migrates its default database.
echo "\nGenerating migrations, then migrating my default database"
python manage.py migrate
python manage.py compilemessages -x venv
python manage.py collectstatic --noinput -i node_modules -i gulpfile.js -i package.json -i package-lock.json

# To kill 404
sed -i -e 's/\/\*# sourceMappingURL=bootstrap.min.css.map \*\///g' \
    /mancelot/static/rest_framework/css/bootstrap.min.css
exec "$@"
