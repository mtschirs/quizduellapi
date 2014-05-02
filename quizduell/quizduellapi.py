import urllib
import urllib2
import json
import hmac
import hashlib
import base64
import datetime

class QuizduellApi(object):
    '''
    Inofficial interface to the Quizduell web API written in Python and
    distributed under GPLv3. Start games, answer questions, find users and
    more.
    
    Quizduell is a registered trademark of FEO Media AB, Stockholm, SE
    registered in Germany and other countries. This project is an independent
    work and is in no way affiliated with, authorized, maintained, sponsored or
    endorsed by FEO Media AB.
    '''
    
    host_name = 'qkgermany.feomedia.se'
    '''Each country uses a different host'''
        
    authorization_key = 'irETGpoJjG57rrSC'
    '''7GprrSCirEToJjG5 for iOS, irETGpoJjG57rrSC for Android'''
    
    user_agent = 'Quizduell A 1.3.2'
    
    device_type = 'a'

    timeout = 20000
    
    password_salt = 'SQ2zgOTmQc8KXmBP'
    
    '''
    Creates the API interface. Expects either an authentication cookie within
    the user supplied cookie jar or a subsequent call to
    QuizduellApi.login_user() or QuizduellApi.create_user().
    
    @param cookie_jar: Stores authentication tokens with each request made
    @type cookie_jar: cookielib.CookieJar or None
    '''
    def __init__(self, cookie_jar=None):
        self._opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(cookie_jar)
        )
    
    def create_user(self, name, password, email=None):
        '''
        Creates a new Quizduell user. The user will automatically be logged in.
        Returns the following JSON structure on success:
        {
            "logged_in": true,
            "settings": {...},
            "user": {...}
        }
        
        @type name: str
        @type password: str
        @type email: str or None
        @rtype: json.json
        '''
        data = {
            'name': unicode(name).encode('utf-8'),
            'pwd': hashlib.md5(self.password_salt + unicode(password).encode('utf-8')).hexdigest()
        }
        if email != None:
            data['email'] = unicode(email).encode('utf-8')
        
        return self._request('/users/create', data)
    
    def login_user(self, name, password):
        '''
        Authenticates an existing Quizduell user. @attention: Any user can only
        log in 10 times every 24 hours! Returns the following JSON structure on
        success:
        {
            "logged_in": true, 
            "settings": {...}, 
            "user": {...}
        }
        
        @type name: str
        @type password: str
        @rtype: json.json
        '''
        data = {
            'name': unicode(name).encode('utf-8'),
            'pwd': hashlib.md5(self.password_salt + unicode(password).encode('utf-8')).hexdigest()
        }
        return self._request('/users/login', data)
    
    def update_user(self, name, password, email=None):
        '''
        Updates an existing Quizduell user. The user will automatically be
        logged in. Returns the following JSON structure on success:
        {
            "logged_in": true,
            "settings": {...},
            "user": {...}
        }
        
        @type name: str
        @type password: str
        @type email: str or None
        @rtype: json.json
        '''
        data = {
            'name': unicode(name).encode('utf-8'),
            'pwd': hashlib.md5(self.password_salt + unicode(password).encode('utf-8')).hexdigest()
        }
        if email != None:
            data['email'] = unicode(email).encode('utf-8')
        
        return self._request('/users/update_user', data)
        
    def find_user(self, name):
        '''
        Looks for a Quizduell user with the given name. Returns the following
        JSON structure on success:
        {
            "u": {
                "avatar_code": "...", 
                "name": "...", 
                "user_id": "..."
            }
        }
        
        @type name: str
        @rtype: json.json
        '''
        data = {
            'opponent_name': unicode(name).encode('utf-8')
        }
        return self._request('/users/find_user', data)
    
    def add_friend(self, user_id):
        '''
        Adds another Quizduell user as a friend. Returns the following
        JSON structure on success:
        {
            "popup_mess": "Du bist jetzt mit ... befreundet", 
            "popup_title": "Neuer Freund"
        }
        
        @type friend_id: str
        @rtype: json.json
        '''
        data = {
            'friend_id': user_id
        }
        return self._request('/users/add_friend', data)
    
    def remove_friend(self, user_id):
        '''
        Removes a friend. Returns the following JSON structure on success:
        {
            "removed_id": "..."
        }
        
        @type friend_id: str
        @rtype: json.json
        '''
        data = {
            'friend_id': user_id
        }
        return self._request('/users/remove_friend', data)
    
    def current_user_games(self):
        '''
        Lists invited, active and finished games. Returns the following JSON
        structure on success:
        {
            "logged_in": true, 
            "settings": {...}, 
            "user": {...}
        }
        
        @rtype: json.json
        '''
        return self._request('/users/current_user_games', {})
    
    def get_game(self, game_id):
        '''
        Lists details of a game, including upcoming questions and their correct
        answers. Returns the following JSON
        structure on success:
        {
            "game": {
                "cat_choices": [...], 
                "elapsed_min": ..., 
                "game_id": ..., 
                "messages": [], 
                "opponent": {...}, 
                "opponent_answers": [...], 
                "questions": [...], 
                "state": ..., 
                "your_answers": [...], 
                "your_turn": false
            }
        }
        
        @type game_id: str
        @rtype: json.json
        '''
        return self._request('/games/' + str(game_id))
    
    def get_games(self, game_ids):
        '''
        Lists details of specified games, but without questions and answers.
        Returns the following JSON structure on success:
        {
            "games": [{
                    "cat_choices": [...], 
                    "elapsed_min": ..., 
                    "game_id": ..., 
                    "messages": [...], 
                    "opponent": {...}, 
                    "opponent_answers": [...], 
                    "state": ..., 
                    "your_answers": [...], 
                    "your_turn": ...
            }, ...]
        }

        @type game_ids: array of int or str
        @rtype: json.json
        '''
        data = {
            'gids': json.dumps([int(i) for i in game_ids])
        }
        return self._request('/games/short_games', data)
    
    def update_avatar(self, avatar_code=None):
        '''
        Change the displayed avatar. An avatar is encoded in a numerical
        string, e.g. "0010999912" consisting of concatenated two-figure values
        for each part: Skin [00-03], Eyes [00-20], Mouth [00-33], Hair [00-94],
        Accessoir [00-24]. Returns the following JSON structure on success:
        {
            "t": true
        }

        @type avatar_code: str or None
        @rtype: json.json
        '''
        data = {}
        if avatar_code != None:
            data['avatar_code'] = avatar_code
        return self._request('/users/update_avatar', data)
    
    def send_message(self, game_id, message):
        '''
        Send a message within a game. The message will be visible in all games
        against the same opponent. Returns the following JSON structure on
        success:
        {
            "m": [{
                "created_at": "..., 
                "from": ..., 
                "id": "...", 
                "text": "...", 
                "to": ...
            }]
        }

        @type game_id: int or str
        @type message: str
        @rtype: json.json
        '''
        data = {
            'game_id': str(game_id),
            'text': unicode(message).encode('utf-8')
        }
        return self._request('/games/send_message', data)
    
    def forgot_password(self, email):
        '''
        Send a mail with a password restore link. The message will be visible
        in all games against the same opponent. Returns the following JSON
        structure on success:
        {
            "popup_mess": "Eine E-Mail ... wurde an deine E-Mail gesendet", 
            "popup_title": "E-Mail gesendet"
        }
        
        @type email: email
        @rtype: json.json
        '''
        data = {
            'email': unicode(email).encode('utf-8')
        }
        return self._request('/users/forgot_pwd', data)
    
    def category_stats(self):
        '''
        Retrieves category statistics and ranking. Returns the following JSON
        structure on success:
        {
            "cat_stats": [...], 
            "n_games_lost": ..., 
            "n_games_played": ..., 
            "n_games_tied": ..., 
            "n_games_won": ..., 
            "n_perfect_games": ..., 
            "n_questions_answered": ..., 
            "n_questions_correct": ..., 
            "n_users": ..., 
            "rank": ..., 
            "rating": ...
        }
        
        @rtype: json.json
        '''
        return self._request('/stats/my_stats')
    
    def game_stats(self):
        '''
        Retrieves game statistics per opponent. Returns the following JSON
        structure on success:
        {
            "game_stats": [{
                "avatar_code": "...", 
                "n_games_lost": ..., 
                "n_games_tied": ..., 
                "n_games_won": ..., 
                "name": "...", 
                "user_id": "..."
            }, ...],
        }
        
        @rtype: json.json
        '''
        return self._request('/stats/my_game_stats')
    
    def category_list(self):
        '''
        Lists all available categories. Returns the following JSON structure on
        success:
        {
            "cats": {
                "1": "Wunder der Technik", 
                ...
            }
        }
        
        @rtype: json.json
        '''
        return self._request('/web/cats')
    
    def num_players(self):
        '''
        Lists the number of Quizduell players.
        
        @rtype: int
        '''
        return self._request('/web/num_players')
    
    def top_list_rating(self):
        '''
        Lists the top rated Quizduell players. Returns the following JSON
        structure on success:
        {
            "users": [{
                "avatar_code": "...", 
                "key": ..., 
                "name": "...", 
                "rating": ...
            }, ...]
        }
        
        @rtype: json.json
        '''
        return self._request('/users/top_list_rating')
    
    def top_list_writers(self):
        '''
        Lists the top rated Quizduell players. Returns the following JSON
        structure on success:
        {
            "users": [{
                "avatar_code": "...", 
                "n_approved_questions": ..., 
                "name": "..."
            }, ...]
        }
        
        @rtype: json.json
        '''
        return self._request('/users/top_list_writers')
    
    def start_random_game(self):
        '''
        Starts a game against a random opponent. Returns the following JSON
        structure on success:
        {
            "game": {
                "cat_choices": [...], 
                "elapsed_min": ..., 
                "game_id": ..., 
                "messages": [], 
                "opponent": {...}, 
                "opponent_answers": [...], 
                "questions": [...], 
                "state": 1, 
                "your_answers": [...], 
                "your_turn": false
            }
        }
        
        @rtype: json.json
        '''
        return self._request('/games/start_random_game')
    
    def start_game(self, user_id):
        '''
        Starts a game against a given opponent. Returns the following JSON
        structure on success:
        {
            "game": {
                "cat_choices": [...], 
                "elapsed_min": ..., 
                "game_id": ..., 
                "messages": [], 
                "opponent": {...}, 
                "opponent_answers": [...], 
                "questions": [...], 
                "state": 1, 
                "your_answers": [...], 
                "your_turn": false
            }
        }
        
        @type opponent_id: str
        @rtype: json.json
        '''
        data = {
            'opponent_id': user_id
        }
        return self._request('/games/create_game', data)
    
    def give_up(self, game_id):
        '''
        Gives up a game. Returns the following JSON structure on success:
        {
            "game": {...}, 
            "popup": {
                "popup_mess": "Du hast gegen ... aufgegeben\n\nRating: -24", 
                "popup_title": "Spiel beendet"
            }
        }
        
        @type game_id: int or str
        @rtype: json.json
        '''
        data = {
            'game_id': str(game_id)
        }
        return self._request('/games/give_up', data)
    
    def add_blocked(self, user_id):
        '''
        Puts another Quizduell user on the blocked list. Returns the following
        JSON structure on success:
        {
            "blocked": [{
                "avatar_code": "...", 
                "name": "...", 
                "user_id": "..."
            }, ...]
        }
        
        @type user_id: str
        @rtype: json.json
        '''
        data = {
            'blocked_id': user_id
        }
        return self._request('/users/add_blocked', data)
    
    def remove_blocked(self, user_id):
        '''
        Removes another Quizduell user from the blocked list. Returns the
        following JSON structure on success:
        {
            "blocked": [...]
        }
        
        @type user_id: str
        @rtype: json.json
        '''
        data = {
            'blocked_id': user_id
        }
        return self._request('/users/remove_blocked', data)
    
    def accept_game(self, game_id):
        '''
        Accept a game invitation. Returns the following JSON structure on
        success:
        {
            "t": true
        }
        
        @type game_id: int or str
        @rtype: json.json
        '''
        data = {
            'accept': '1',
            'game_id': str(game_id)
        }
        return self._request('/games/accept', data)
    
    def decline_game(self, game_id):
        '''
        Decline a game invitation. Returns the following JSON structure on
        success:
        {
            "t": true
        }
        
        @type game_id: int or str
        @rtype: json.json
        '''
        data = {
            'accept': '0',
            'game_id': str(game_id)
        }
        return self._request('/games/accept', data)
    
    def upload_round_answers(self, game_id, answers, category_id):
        '''
        Upload answers and the chosen category to an active game. The number of
        answers depends on the game state and is 3 for the first player in the
        first round and the last player in the last round, otherwise 6.
        Returns the following JSON structure on success:
        {
          "game": {
            "your_answers": [...],
            "state": ...,
            "elapsed_min": ...,
            "your_turn": false,
            "game_id": ...,
            "cat_choices": [...],
            "opponent_answers": [...],
            "messages": [...],
            "opponent": {...}
          }
        }
        
        @type game_id: int or str
        
        @param answers: 3 or 6 values in {0,1,2,3} with 0 being correct
        @type answers: array of int or str
        
        @param category_id: value in {0,1,2}
        @type category_id: int or str
        
        @rtype: json.json
        '''
        data = {
            'game_id': str(game_id),
            'answers': json.dumps([int(i) for i in answers]),
            'cat_choice': str(category_id)
        }
        return self._request('/games/upload_round_answers', data)   
    
    @classmethod
    def _get_authorization_code(cls, url, client_date, post_params=None):
        msg = 'https://' + cls.host_name + url + client_date
        if post_params:
            msg += ''.join(sorted(post_params.values()))
        
        dig = hmac.new(cls.authorization_key, msg=msg, digestmod=hashlib.sha256)
        return base64.b64encode(dig.digest()).decode()
        
    def _request(self, url, post_params=None):
        client_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._opener.addheaders = [
           ('dt', self.device_type),
           ('authorization', self._get_authorization_code(url, client_date, post_params)),
           ('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8'),
           ('User-Agent', self.user_agent),
           ('clientdate', client_date)
        ]
        
        if post_params != None:
            encoded_params = urllib.urlencode(post_params)
            self._opener.addheaders.append(('Content-Length', str(len(encoded_params)))) 
        else:
            encoded_params = None
        
        response = self._opener.open('https://' + self.host_name + url, data=encoded_params, timeout=self.timeout)
        return json.loads(response.read())