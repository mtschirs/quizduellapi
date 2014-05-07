#Quizduell API
Inofficial interface to the Quizduell web API written in Python and distributed under GPLv3. Start games, write messages, find users and more.

####Example 1 - Find User
The following code authenticates a Quizduell user and performs a username lookup for 'peter':
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
stats = api.find_user('peter')
```
Return values are in JSON:
```python
{
  "u": {
    "avatar_code": null, 
    "facebook_id": "1000...", 
    "name": "Peter", 
    "user_id": "5455..."
  }
}

```
####Example 2 - Top Ten
The following code retrieves a list of Quizduell users with the highest ranking:
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
rating = api.top_list_rating()
```

####Credits
Thanks to the blogger and commenters on [easysurfer.me](http://easysurfer.me/wordpress/?p=761) for their insights!

####Disclaimer
Quizduell is a registered trademark of FEO Media AB, Stockholm, SE registered in Germany and other countries. This project is an independent work and is in no way affiliated with, authorized, maintained, sponsored or endorsed by FEO Media AB.
