#Quizduell API
Inofficial interface to the Quizduell web API written in Python and distributed under GPLv3. Start games, write messages, find users and more.

####Demo
[This bot for Quizduell](http://quizgamebot.appspot.com) is based on this project. It automatically sends and answers game requests, writes messages and plays on beginner, advanced and expert level.

####Example 1 - Statistics
The following code authenticates a Quizduell user and retrieves some statistics:
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
stats = api.category_stats()
```
Return values are in JSON:
```python
{
  "cat_stats": [{"cat_name": "Wunder der Technik", "percent": 0.74}, ...],
  "n_perfect_games": 1, 
  "n_games_lost": 0, 
  ...
}
```

####Example 2 - Avatar
The following code changes the user's avatar to a skin colored avatar wearing a crown:
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
api.update_avatar('0010999912')
```

####Example 3 - Find User
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

####Example 4 - Top Ten
The following code retrieves a list of Quizduell users with the highest ranking:
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
rating = api.top_list_rating()
```

####Example 5 - Time till next show
The following code displays the time until the next Quizduell TV show (Germany only):
```python
api = quizduell.QuizduellApi()
api.login_user('name', 'password')
tv_api = quizduell.QuizduellTvApi.fromQuizduellApi(api)
state = tv_api.get_state()
print 'Next show:', datetime.datetime.fromtimestamp(state['Meta']['NextShowDate'])
```

####Credits
Thanks to the blogger and commenters on [easysurfer.me](http://easysurfer.me/wordpress/?p=761) for their insights!

####Disclaimer
This python module was build relying exclusively on publicly available information of the Quizduell application and without making use of any systematic or automatic data collection, including data scraping, data mining, data extraction, data harvesting or data traffic sniffing.

Quizduell is a registered trademark of FEO Media AB, Stockholm, SE registered in Germany and other countries. This project is an independent work and is in no way affiliated with, authorized, maintained, sponsored or endorsed by FEO Media AB.
