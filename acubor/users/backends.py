from django.contrib.auth import get_user_model


class BasicBackend:
    def get_user(self, user_id):
        try:
            try:
                return get_user_model().objects.get(pk=user_id)
            except get_user_model.DoesNotExist:
                return None
        except AttributeError:
            return None


class EmailOrUsernameBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        #We have a non-email address username we should try username
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None
        if user.check_password(password):
            return user
