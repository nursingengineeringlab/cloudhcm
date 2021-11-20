# import threading

class Online_Seniors(dict):
    def __init__(self, *p_arg, **n_arg):
        dict.__init__(self, *p_arg, **n_arg)
        # self.__lock = threading.RLock()

    def __enter__(self):
        # self.__lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        pass
        # self.__lock.release()


    # def add_seniors(self, device_id):

# Global Dictionary of Online Seniors
