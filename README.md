# githubSSO
Github SSO OAuth Authorization flow Django Django-rest-framework

To run:
## Fork this repo.
### Clone repo.
1. Open project.
1.1 Activate virtual environment:
```
.\githubssovenv\Scripts\Activate.ps1
```
1.2 Install requirements.
```
pip install -r ./requirements.txt
```
1.3 Migrate changes using below command:
```
python manage.py makemigrations
python manage.py migrate
```
2. Create superuser
```
python manage.py createsuperuser
```
2.1 Run
```
python manage.py runserver
```
3. Go to http://localhost:8000/admin/
Create OAuthserver entries inside customer options table and Oidcclientdetails table.
4. Go to http://localhost:8000/login/sso/1
Test by clicking on Login with Github button.
