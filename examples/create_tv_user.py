import quizduell

api = quizduell.QuizduellApi()

# Create a Quizduell user and his associated TV user (name must be unused):
api.create_user('Max MustermannQQ', 'password')

# Instantiation of the Quizduell TV API from authenticated Quizduell API:
tv_api = quizduell.QuizduellTvApi.fromQuizduellApi(api)
tv_api.agree_agbs()
tv_api.post_profile('Max', 'Mustermann', 'max@mustermann.com', 'DE')
tv_api.upload_profile_image('path/to/image.jpg')