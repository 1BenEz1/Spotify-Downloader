import os , shutil

"""
    this class configures the user that handles the bot
"""

class Con:

    user_id = ''
    user_pl = ''

    # create a directory named by the user id
    # create a file that stores the id and playlist url
    def __init__(self , user_id, user_pl):
        self.user_id = user_id
        self.user_pl = user_pl

        dir_name = f"{user_id}"
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            print('exists')

        os.chdir(dir_name)
        f = open( f"{user_id}.txt", 'w+')
        f.write(str(user_id)+'\n')
        f.write(user_pl)
        os.chdir(os.pardir)

    