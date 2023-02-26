# githubSSO
Github SSO OAuth Authorization flow Django Django-rest-framework

To run:
### Clone repo
1. Open project.
  * Activate virtual environment:
```
.\githubssovenv\Scripts\Activate.ps1
```
Change directory to Githubsso.
  * Install requirements.
```
pip install -r .\requirements.txt
```
  * Migrate changes using below command:
```
python manage.py makemigrations
python manage.py migrate
```
2. Create superuser
```
python manage.py createsuperuser
```
  * Run
```
python manage.py runserver
```

3. Register your application on Github.
User http://localhost:8000/login/sso/getauthcode/ as Authorization callback URL.
Mark down client_id and client_secret.

4. Go to http://localhost:8000/admin/
Create OAuthserver entries inside customer options table and Oidcclient table.
In Oidcclient table
add:
```
Application_name: GithubSSO
Client_id: client_id (*from github)
Client_secret: client_secret (*from github)
Oauthserver: Github
Authorization endpoint="https://github.com/login/oauth/authorize"
Token endpoint:"https://github.com/login/oauth/access_token"
Enduserinfo endpoint: "https://api.github.com/user"
Scope: "[user:email]"
Redirect uri:"http://localhost:8000/login/sso/getauthcode/"
Response type: "code"
```
In Customer Optionss table 
```
add: key:oauthserver value:github
add: key:oauthappname value:GithubSSO (*same as Application_name from Oidcclient entry)
```
5. Go to http://localhost:8000/login/sso/1
6. Test by clicking on Login with Github button.
