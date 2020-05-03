#!/bin/sh

if [ ! -f .initialized ]; then                                                                                                                                                                                    
    echo "Initializing container"                                                                                                                                                                                 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata customers busstations buses tripstops triproutes trips                                                                                                                                                                                  
    touch .initialized                                                                                                                                                                                            
fi                                                                                                                                                                                                                

exec "$@"