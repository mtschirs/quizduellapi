import quizduell
import datetime

# Instantiation of the Quizduell TV API without credentials:
tv_api = quizduell.QuizduellTvApi()
state = tv_api.get_state()
print 'Next show:', datetime.datetime.fromtimestamp(state['Meta']['NextShowDate'])
