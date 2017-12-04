# chat_client.py

import sys
import socket
import select
import threading
import logging
logging.basicConfig(level=logging.DEBUG,
                      format='[%(levelname)s] (%(threadName)-9s) %(message)s',)
def chat_client():
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((socket.gethostname(), 9009))

    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] '); sys.stdout.flush()
    # while 1:
    #     socket_list = [s]
    #     try:
    #
    #         # Get the list sockets which are readable
    #         print 'in select blk'
    #         ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
    #         print 'ready to read', ready_to_read
    #         ready_to_read.append(sys.stdin)
    #
    #         for sock in ready_to_read:
    #             if sock == s:
    #                 print ready_to_read
    #                 # incoming message from remote server, s
    #                 data = sock.recv(4096)
    #                 print 'after client recv'
    #                 if not data:
    #                     print '\nDisconnected from chat server'
    #                     sys.exit()
    #                 else:
    #                     # print data
    #                     sys.stdout.write(data)
    #                     sys.stdout.write('[Me] ');
    #                     sys.stdout.flush()
    #
    #             else:
    #                 # user entered a message
    #                 msg = sys.stdin.readline()
    #                 s.send(msg)
    #                 sys.stdout.write('[Me] ');
    #                 sys.stdout.flush()
    #     except Exception as e:
    #         # print "sock ", sock
    #         print e
    def check_message():
        while 1:
            socket_list = [s]
            try:

                # Get the list sockets which are readable
                print 'in select blk'
                ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

                logging.debug('ready to read %s' % ready_to_read)
                ready_to_read.append(sys.stdin)

                for sock in ready_to_read:
                    if sock == s:
                        print ready_to_read
                        # incoming message from remote server, s
                        data = sock.recv(4096)
                        print 'after client recv'
                        if not data :
                            print '\nDisconnected from chat server'
                            sys.exit()
                        else :
                            #print data
                            sys.stdout.write(data)
                            sys.stdout.write('[Me] '); sys.stdout.flush()

                    # else :
                    #     # user entered a message
                    #     logging.debug("WAITING FOR I/P")
                    #     msg = sys.stdin.readline()
                    #     s.send(msg)
                    #     sys.stdout.write('[Me] '); sys.stdout.flush()
            except Exception as e:
                # print "sock ", sock
                print e
    def send_message():
        while 1:
            logging.debug("WAITING FOR I/P")
            msg = sys.stdin.readline()
            s.send(msg)
            sys.stdout.write('[Me] ')
            sys.stdout.flush()
    thread1 = threading.Thread(target=check_message)
    thread2 = threading.Thread(target=send_message)
    # thread1.setDaemon(True)
    # thread2.setDaemon(True)
    thread1.start()
    thread2.start()

if __name__ == "__main__":

    sys.exit(chat_client())