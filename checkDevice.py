import sys 
import imaplib 
import os
import time


# your IMAP mail server
mail = imaplib.IMAP4_SSL('imap.gmail.com')

USER = 'YOUR EMAIL ID'
PASS = 'YOUR EMAIL PASSWORD'
MAC = 'DEVICE MAC ID TO LOOK FOR'

try:
	mail.login(USER, PASS)# getpass.getpass())
	#mail.select("Inbox")
except imaplib.IMAP4.error:
	print "LOGIN FAILED!!"

while True:

	try:
		mail.select("Inbox")
		rv, [data] = mail.search(None,'(SUBJECT "Reply little Pi")')
		if data:
			print "received"
			# replace with different network parameters if applicable
			sca = os.system('nmap -sn 192.168.1.1-255 | grep "%s"'%MAC)
			print sca
			if sca != 256:
				print "found"
				os.system('./pushbullet.sh "Connected"')
			else:
				print "nope!"
				os.system('./pushbullet.sh "Not Connected"')
		# Deleting the request message
		data = ','.join(data.split(' '))
       		rv, data2 = mail.fetch(data, '(FLAGS)')
	        rv, data2 = mail.store(data, '+FLAGS', r'(\DELETED)')
       		rv, data2 = mail.fetch(data, '(FLAGS)')
	        rv, data2 = mail.expunge()
      		print "cleaning up..."
		del sca
	except:
		#print "nothing"
		time.sleep(5)
