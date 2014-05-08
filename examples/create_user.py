import quizduell

api = quizduell.QuizduellApi()
result = api.create_user('Max Mustermann', 'max@mustermann.com', 'password')

if 'popup_mess' in result: 
    print 'Error:', result['popup_mess']