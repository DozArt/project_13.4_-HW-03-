# project_5.8.1_-HW-03-
        Key project from SkillFactory
        Project name - News portal
        test user with author's rights
        mail: new_user@test.com
        pass: pass12345
        and for http://127.0.0.1:8000/admin/ - admin admin

# install
        venv\scripts\activate
        pip install django
        pip install django-filter
        pip install allauth
        pip install django-allauth
        pip install django_apscheduler
        pip install celery
        pip install redis
        pip install -U "celery[redis]"
        
# RUN
# Open terminal and input:
        cd NewsPaper
        python manage.py runserver

    local address - http://127.0.0.1:8000/

# navigation menu caching for 30 seconds
        All posts
        News
        Articles
        Subscriptions 🕭
        Search🔍︎
# urls.news_list caching for 60 seconds

# urls.one_news caching for 5 minutes