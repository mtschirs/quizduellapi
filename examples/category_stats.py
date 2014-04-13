import quizduell
import cookielib
import json
import os

# Load authenticated session from file to prevent unnecessary logins:
cookie_jar = cookielib.MozillaCookieJar('cookie_file')
api = quizduell.QuizduellApi(cookie_jar)

if os.access(cookie_jar.filename, os.F_OK):
    cookie_jar.load()
else:
    api.login_user('name', 'password')

api = quizduell.QuizduellApi(cookie_jar)
result = api.category_stats()

if 'access' in result:
    # Session timed out, re-login:
    api.login_user('name', 'password')
    result = api.category_stats()

# Store authenticated session in file:
cookie_jar.save()

print json.dumps(result, sort_keys=True, indent=4)


