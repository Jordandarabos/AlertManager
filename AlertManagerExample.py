import alertsManager,time

emailUsername = 'username'
emailPass = 'password'
recipients = ['recipient1@example.com','recipient2@example.com']
bccRecipients = ['bccrecipient1@example.com','bccrecipient2@example.com']

AlertsManager = alertsManager.AlertsManager(recipients,bccRecipients,emailUsername,emailPass)

AlertsManager.email.sender = "Example Sender"

for j in range (0,100):
	AlertsManager.addAlert("Digital Test {}".format(j), 0,delay=5)

AlertsManager.addAlert("Analog Test",value=10,min=5,max=10,scale=1,delay=0)

time.sleep(5)

for j in range (10,15):
	AlertsManager.updateAlert('Digital Test {}'.format(j), 1)

AlertsManager.updateAlert("Analog Test", 15)

changes = AlertsManager.checkForChanges()

print(changes)


