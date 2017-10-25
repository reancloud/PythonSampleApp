import os

class Utility():
    @staticmethod
    def get_username_and_password():
        "gets configured username and password"
        credentials = ''
        path = os.path.expanduser('~')
        if os.path.exists(path + '/.deploy/credentials'):
            with open(path + '/.deploy/credentials', 'r') as file_obj:
                for i, line in enumerate(file_obj):
                    if i == 1:
                        credentials = line.split('=')[1].strip("\n")
                    if i == 2:
                        credentials = credentials + ":" + line.split('=')[1].strip('\n')
                return credentials
