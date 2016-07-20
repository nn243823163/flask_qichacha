# from app import creat_app
from app import creat_app
#qichacha
app = creat_app()

if __name__ ==  '__main__':

    while True:
        try:

            app.run()
        except Exception as e:
            print 'eeeee'+str(e)