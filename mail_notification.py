from email.header import decode_header
import imaplib
import time
import re
import ctypes
import urllib
import webbrowser
import getpass


class MailNotification(object):

    @staticmethod
    def send_mail_notification():
        M = imaplib.IMAP4_SSL('imap.gmail.com')
        username = 'gopinath.ravikumar@jouve.in'
        password = getpass.getpass('Password:')
        @MailNotification.retry_login_failure(3)
        def login(username, password):
            M.login(username, password)
        success = login(username, password)
        if not success:
            raise Exception('Cannot login to mail server !!!!!!!!!!')
        print 'Logged in successfully'
        while 1:
            time.sleep(120)
            # unseenCount = re.search(r"UNSEEN (\d+)", M.status("INBOX", "(UNSEEN)")[1][0]).group(1)
            print M.select()
            print M.search(None, 'UnSeen')
            print M.status("INBOX", "(UNSEEN)")
            for e_id in M.search(None, 'UnSeen')[1][0].split():
                _, response = M.fetch(e_id, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
                M.store(e_id, '-FLAGS', '\\Seen')  # Mark it as unread again
                match_found = re.search(r'From:(?P<from>.*)Subject:(?P<subject>.*)', response[0][1], re.DOTALL)
                if not match_found:
                    match_found = re.search(r'Subject:(?P<subject>.*)From:(?P<from>.*)', response[0][1], re.DOTALL)
                subject = decode_header(match_found.group('subject').rstrip('\r\n'))[0][0]
                mail_from = decode_header(match_found.group('from').rstrip('\r\n'))[0][0]
                display_content = "From: {0}\n\nSubject: {1}".format(mail_from, subject)
                return_value = ctypes.windll.user32.MessageBoxA(0,
                                                                display_content + "\n\n Click Yes to open the message",
                                                                "Mail Notification", 4)
                if return_value == 6:
                    webbrowser.open("https://mail.google.com/mail/u/0/#search/%s" % (urllib.quote_plus(subject)))
                print response[0][1]

    @staticmethod
    def retry_login_failure(max_attempt):
        def outer_wrapper(func):
            def inner_wrapper(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    return True
                except imaplib.IMAP4.error as e:
                    print "LOGIN FAILED!!!, try again... " + str(e)
                    prompt = lambda: (getpass.getpass(), getpass.getpass('Retype password:'))
                    password1, password2 = prompt()
                    while password1 != password2:
                        print 'Password not matched, try again...'
                        password1, password2 = prompt()
                    count = 1
                    while count <= max_attempt:
                        try:
                            func(args[0], password1, **kwargs)
                            return True
                        except imaplib.IMAP4.error as e:
                            print "Login failure reason: " + str(e)
                            print "Unsuccessful login attempt: " + str(count)
                            count += 1
                            password1, password2 = prompt()
                            while password1 != password2:
                                print 'Password not matched, try again...'
                                password1, password2 = prompt()
                    raise Exception('Maximum login attempts reached !!!!!') # If more number of attempts reached

            return inner_wrapper

        return outer_wrapper


MailNotification.send_mail_notification()