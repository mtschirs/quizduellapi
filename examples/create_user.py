import quizduell

api = quizduell.QuizduellApi()
result = api.create_user('name', 'name@email.com', 'password')

if 'popup_mess' in result: 
    print 'Error:', result['popup_mess']