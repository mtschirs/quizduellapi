import quizduell
import datetime

# Create a Quizduell user (alternatively login with api.login_user):
api = quizduell.QuizduellApi()
user = api.create_user('Max Mustermann', 'password')

if 'popup_mess' in user: 
    print 'Error:', user['popup_mess']
    exit()

# Instantiation of the Quizduell TV API from authenticated Quizduell API:
tv_api = quizduell.QuizduellTvApi.fromQuizduellApi(api)
state = tv_api.get_state()
print 'Next show:', datetime.datetime.fromtimestamp(state['Meta']['NextShowDate'])
