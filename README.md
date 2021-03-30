# API_LANDLORDS

Goal: The goal of this API is to create is a Tenant Retention system. The users can register, login , post complaints, see all complaints and see the announcements.

Before running the API we need to create the database. If the data base is already created start on 1. If the data has not been created starton 4.

How to use it:
____________________________________________________

1. Erase __pycahe__ files
2. Erase migration folder
3. Erase data.sqlite
____________________________________________________

4. Open the console:  export FLASK_APP= app.py (set if you are using window)
5. Create the database by typing: flask db init
6. Create migrations by typing: flask db migrate -m "First Database"
7. Upgrade : flask db upgrade
____________________________________________________

8. Run the applications :  python app.py
