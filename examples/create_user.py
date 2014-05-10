import quizduell

api = quizduell.QuizduellApi()
user = api.create_user('Max Mustermann', 'password', 'max@mustermann.com')

if 'popup_mess' in user: 
    print 'Error:', user['popup_mess']