# githubSSO
Github SSO OAuth2 Authorization flow for Django webapp.

To run:
* Clone repo.
```
git clone #https_url_of_project
```
1. Open project.
* go inside folder githubSSO.
* Create a virtual envrironment:
```
   python -m venv /path/to/virtual/environment
   python -m venv githubssovenv
```
  * Activate virtual environment:
```
.\githubssovenv\Scripts\Activate.ps1
```
Change directory to githubsso.
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
Use http://localhost:8000/login/sso/getauthcode/ as Authorization callback URL as well as home URL. \
Application name which you provide here will be displayed to user when he tries to login with github credentials to our webapp.
\
Mark down client_id and client_secret.

4. Go to http://localhost:8000/admin/
Use superuser credentials to login.
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
In Customer Options table 
```
add: key:oauthserver value:github
add: key:oauthappname value:GithubSSO (*same as Application_name from Oidcclient entry)
```
5. Go to http://localhost:8000/login/sso/1
  \
  You will see text:
```
Hi, superusername.
Login with github button.
```

6. Test by clicking on Login with Github button.

You can see below execution of single sign on:
![Github Single Sign On with django webapp using OAuth2 and openId Connect protocol Authorization flow](example.gif)
