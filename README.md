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

```
####Example 3 - Time till next show
The following code displays the time until the next Quizduell TV show (Germany only):
```python
tv_api = quizduell.QuizduellTvApi(user_id)
state = tv_api.get_state()
print 'Next show:', datetime.fromtimestamp(state['Meta']['NextShowDate']).strftime("%d.%m.%Y %H:%M:%S")

```

####Demo
[This bot for Quizduell](http://quizgamebot.appspot.com) is based on this project. It automatically sends and answers game requests, writes messages and plays on beginner, advanced and expert level.

####Credits
Thanks to the blogger and commenters on [easysurfer.me](http://easysurfer.me/wordpress/?p=761) for their insights!

####Disclaimer
This python module was build relying exclusively on publicly available information of the Quizduell application and without making use of any systematic or automatic data collection, including data scraping, data mining, data extraction, data harvesting or data traffic sniffing.

Quizduell is a registered trademark of FEO Media AB, Stockholm, SE registered in Germany and other countries. This project is an independent work and is in no way affiliated with, authorized, maintained, sponsored or endorsed by FEO Media AB.
