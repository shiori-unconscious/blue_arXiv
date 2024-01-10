rm db.sqlite3 
rm -r login/migrations
rm -r mainpage/migrations
python manage.py makemigrations login
python manage.py makemigrations mainpage
python manage.py migrate