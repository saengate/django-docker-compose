# https://stackoverflow.com/questions/49936101/how-to-prevent-brute-force-attack-in-django-rest-using-django-rest-throttling
from collections import Counter

from rest_framework.throttling import SimpleRateThrottle
from modules.users.models import User


class UserLoginRateThrottle(SimpleRateThrottle):
    scope = 'loginAttempts'

    def get_cache_key(self, request, view):
        user = User.objects.filter(username=request.data.get('username'))
        ident = user[0].pk if user else self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        if len(self.history) >= 3:
            data = Counter(self.history)
            for _, value in data.items():
                if value == 2:
                    return self.throttle_failure()
        return self.throttle_success(request)

    def throttle_success(self, request):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        user = User.objects.filter(username=request.data.get('username'))
        if user:
            self.history.insert(0, user[0].id)
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True
