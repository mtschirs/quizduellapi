import quizduell

# Create a Quizduell user (alternatively login with api.login_user):
api = quizduell.QuizduellApi()
user = api.create_user('Max Mustermann', 'password')

if 'popup_mess' in user: 
    print 'Error:', user['popup_mess']
    exit()

# Instantiation of the Quizduell TV API from authenticated Quizduell API:
# Raises "HTTP Error 404: Not Found" while show is inactive!
tv_api = quizduell.QuizduellTvApi.fromQuizduellApi(api)
tv_api.agree_agbs()