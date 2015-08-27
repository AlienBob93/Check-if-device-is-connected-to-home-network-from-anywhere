import sys 
import imaplib 
import subprocess as OS
import time


# your IMAP mail server
mail = imaplib.IMAP4_SSL('imap.gmail.com')

USER = 'YOUR EMAIL ID'
PASS = 'YOUR EMAIL PASSWORD'
MAC_1 = 'DEVICE MAC ID TO LOOK FOR'
MAC_2 = 'DEVICE MAC ID TO LOOK FOR'
# Add more MAC IDs 

try:
	mail.login(USER, PASS)
except imaplib.IMAP4.error:
	print "LOGIN FAILED!!"

while True:

	try:
		mail.select("Inbox")
		rv, [data] = mail.search(None,'(SUBJECT "Reply little Pi")')
		if data:
			print "received"
			# replace with different network parameters if applicable
			sca = OS.check_output(['nmap','-sn','10.0.0.1-255'])
			print sca
			if sca:
				if MAC_1 in sca:
                                        print "XXX is home"
                                        OS.call(['./pushbullet.sh','XXX is home'])
                                if MAC_2 in sca:
                                        print "XXX is home"
                                        OS.call(['./pushbullet.sh','XXX is home'])
                                # Add more if necessary        
                                if not MAC_1 in sca and not MAC_2 in sca:  
					print "No one is around :("
	                               	OS.call(['./pushbullet.sh','No one is around :('])
		# Deleting the request message
		data = ','.join(data.split(' '))
       		rv, data2 = mail.fetch(data, '(FLAGS)')
	        rv, data2 = mail.store(data, '+FLAGS', r'(\DELETED)')
       		rv, data2 = mail.fetch(data, '(FLAGS)')
	        rv, data2 = mail.expunge()
      		print "cleaning up..."
		del sca
	except:
		#wait for 5 seconds
		time.sleep(5)
