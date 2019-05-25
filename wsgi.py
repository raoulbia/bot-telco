"""
 the wsgi.py file or the alias aren't needed, Gunicorn can be pointed directly at the real module and callable,
 https://stackoverflow.com/questions/33379287/gunicorn-cant-find-app-when-name-changed-from-application
"""
# from cai_vodafone import app
#
# if __name__ == "__main__":
#     app.run()