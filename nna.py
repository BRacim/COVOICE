# import threading
# import time


# def run():
#     global stop_threads
#     global t
#     global t2
#     print('P2 wainting 40')

#     time.sleep(5)
#     stop_threads = True
#     while True:
#         print('thread running')
#         if stop_threads:
#             print(t2.isAlive())
#             if t2.isAlive():
#                 t2.join()
#             break


# def nassim():
#     print("fin running")
#     global stop_threads
#     stop_threads = True


# def runt():
#     global t
#     print("P1")
#     t = threading.Timer(60.0, nassim)
#     t.start()


# t = None
# stop_threads = False
# t1 = threading.Thread(target=run)
# t1.start()
# t2 = threading.Thread(target=runt)
# t2.start()
# t1.join()
# print(t2.isAlive())
# t2.join()
# print('thread killed')
