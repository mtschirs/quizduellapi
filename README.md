#Quizduell API
Inofficial interface to the Quizduell web API written in Python and distributed under GPLv3. Start games, answer questions, read user statistics and more.

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
####Demo
[This bot for Quizduell](http://quizgamebot.appspot.com) is based on this project. It automatically sends and answers game requests, writes messages and plays on beginner, advanced and expert level.

####Credits
Thanks to the blogger and commenters on [easysurfer.me](http://easysurfer.me/wordpress/?p=761) for their insights!

####Disclaimer
Quizduell is a registered trademark of FEO Media AB, Stockholm, SE registered in Germany and other countries. This project is an independent work and is in no way affiliated with, authorized, maintained, sponsored or endorsed by FEO Media AB.
