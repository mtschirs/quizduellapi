import quizduell

# Create a Quizduell user and his associated TV profile:
api = quizduell.QuizduellApi()
user = api.create_user('Max Mustermann', 'password')
api.create_tv_user()

# Instantiation of the TV Api requires the user id of the Quidzuell user:
tv_api = quizduell.QuizduellTvApi(user['user']['user_id'])
tv_api.agree_agbs()
tv_api.post_profile('Max', 'Mustermann', 'max@mustermann.com', 'DE')
tv_api.upload_profile_image('path/to/image.jpg')