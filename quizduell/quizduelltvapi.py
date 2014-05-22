import urllib
import urllib2
import json

class QuizduellTvApi(object):
    '''
    Inofficial interface to the Quizduell TV App web API written in Python and
    distributed under GPLv3.
    
    Quizduell is a registered trademark of FEO Media AB, Stockholm, SE
    registered in Germany and other countries. This project is an independent
    work and is in no way affiliated with, authorized, maintained, sponsored or
    endorsed by FEO Media AB.
    '''
    
    host_name = 'quizduell.mobilemassresponse.de'
    ''' Also try tvqd-gcx.appspot.com. API endpoint '''
    
    app_request = 'grandc3ntr1xrul3z'
    ''' HTTP CORS header token '''
    
    timeout = 20000
    
    def __init__(self, user_id='0', tv_auth_token='0'):
        '''
        Creates the TV API interface. The user identified by the supplied user
        id must have a TV profile created by a call to
        QuizduellApi.create_tv_user() and a personal TV auth token.
        
        @param user_id: Quizduell user id
        @type user_id: str
        
        @param tv_auth_token: TV auth token returned by
                              QuizduellApi.create_tv_user()
        @type tv_auth_token: str
        ''' 
        self._user_id = user_id
        self._tv_auth_token = tv_auth_token
        self._opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0)
        )

    @classmethod
    def fromQuizduellApi(cls, quizduell_api):
        '''
        Creates the TV API interface from an authenticated quizduell API 
        instance.
        
        @param quizduell_api: authenticated Quizduell API instance (logged in)
        @type quizduell_api: QuizduellApi
        '''
        tv_user = quizduell_api.create_tv_user()
        return cls(tv_user['user']['user_id'], tv_user['user']['tt'])
    
    def agree_agbs(self, agree=True):
        '''
        Agrees to the AGB of the TV application.
        Returns the following JSON structure on success:
        {
            "FeoUser": {
                "AgreedAgbs": true, 
                "AvatarString": "...", 
                "IsRegistered": ..., 
                "Nick": "...", 
                "Uid": "...", 
                "Updated": ...
            }, 
            "Status": 200
        }
        '''
        return self._request('/feousers/agbs/' + self._user_id + ('/true' if agree else '/false'), method='POST')
    
    def get_rankings(self):
        '''
        Retrieves the TV user ranking.
        Returns the following JSON structure on success:
        {
            "Count": ..., 
            "MyPoints": ..., 
            "MyRank": ..., 
            "RankedUsers": [...], 
            "Status": 200
        }
        '''
        return self._request('/users/myranking/' + self._user_id)
    
    def get_profile(self):
        '''
        Retrieves the TV user profile.
        Returns the following JSON structure on success:
        {
            "FeoUser": {
                "AgreedAgbs": ..., 
                "AvatarString": "...", 
                "IsRegistered": ..., 
                "Nick": "...", 
                "Sex": "...", 
                "Uid": "...", 
                "Updated": ..., 
                "Zip": "..."
            }, 
            "Status": 200
        }
        '''
        return self._request('/users/profiles/' + self._user_id)
    
    def set_avatar_and_nick(self, nick, avatar_code=''):
        '''
        Has no impact on the Quizduell nick and avatar and will automatically
        be reverted on startup of the Quizduell TV app.
        Returns the following JSON structure on success:
        {
            "FeoUser": {
                "AgreedAgbs": ..., 
                "AvatarString": "...", 
                "IsRegistered": ..., 
                "Nick": "...", 
                "Sex": "...", 
                "Uid": "...", 
                "Updated": ..., 
                "Zip": "..."
            }, 
            "Status": 200, 
            "UserProfile": { ... }
        }
        '''
        data = {
            'AvatarString': avatar_code,
            'Nick': unicode(nick).encode('utf-8')
        }
        return self._request('/users/' + self._user_id + '/avatarandnick', 'POST', data)
    
    def send_response(self, question_id, answer_id):
        return self._request('/users/' + self._user_id + '/response/' + question_id + '/' + answer_id)

    def select_category(self, category_id):
        return self._request('/users/' + self._user_id + '/category/' + category_id)
    
    def get_state(self):
        '''
        Retrieves the current state of the TV quiz (countdown / running...).
        Doesn't require a valid user-id or TV-authtoken.
        Returns e.g. the following JSON structure:
        {
            "Interval": 2, 
            "Meta": {
                "NextShowDate": 1491850020
            }, 
            "ShowId": "1", 
            "State": "show.countdown", 
            "Status": 200
        }
        '''
        return self._request('/states/' + self._user_id)
    
    def _request(self, url, method='GET', data=None, urlencode=True):
    
        request = urllib2.Request('https://' + self.host_name + url)
        request.add_header('x-app-request', self.app_request)
        request.add_header('x-tv-authtoken', self._tv_auth_token)
        
        if method == 'POST':
            if data:
                request.add_data(urllib.urlencode(data) if urlencode else data)
                request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
                request.add_header('Content-Length', str(len(request.data)))
            else:
                request.add_header('Content-Length', 0)
        
        request.get_method = lambda: method
        response = self._opener.open(request, timeout=self.timeout)
        return json.loads(response.read())