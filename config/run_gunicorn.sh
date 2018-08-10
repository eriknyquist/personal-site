NAME="personal-site"
ME="personal-site"
DJANGODIR=/home/ubuntu/personal-site
SOCKFILE=/var/run/gunicorn.sock
USER=ubuntu 
NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=personal-site.settings
DJANGO_WSGI_MODULE=personal-site.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE} \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
