# # just to prevent from auto sign in in django admin

# from importlib import import_module  # Add this line
# from django.contrib.auth import get_user_model
# from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.conf import settings  # Add this line


# class AdminSessionMiddleware(AuthenticationMiddleware):
#     def process_request(self, request):
#         # Check if the request is for the admin site
#         if request.path.startswith("/admin/"):
#             # Use a different session key prefix for the admin site
#             request.session = self._create_session()
#         super().process_request(request)

#     def _create_session(self):
#         engine = import_module(settings.SESSION_ENGINE)
#         return engine.SessionStore()
