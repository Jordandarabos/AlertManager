###Alerts Manager###

##		Input current status of alerts and it will manage time alert occured,
## 		info on last alarm, whether or not a change has occured, email client
##      to report changes to, also add functionality to store to local db


import time,datetime,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AlertsManager():

	def __init__(self,recipients = '',bccRecipients = '',emailUsername = '',emailPass = ''):
		self.alerts = {}
		self.newAlerts = {}
		self.startTime = time.time()
		self.email = Email(recipients,bccRecipients,emailUsername,emailPass)

	def getDatetime(self):
		t = datetime.datetime.utcnow()
		dateTime = t.strftime("%Y-%m-%d %H:%M:%S")	

		return dateTime	

	def addAlert(self,alertName,value,min=None,max=None,scale=None,delay=0.0):
		dateTime = self.getDatetime()

		self.alerts.update({"{}".format(alertName):{"value": value,"min": min,"max": max,"scale": scale,"delay": delay,
													"time": dateTime,"lastValue" : 0, "lastValueTime" : 0, "change": 0, 
													"status" : None}})

	def updateAlert(self,alertName,value):
		dateTime = self.getDatetime()
		timeElapsed = time.time() - self.startTime
		#print("Time Elapsed", timeElapsed)

		try:
			self.alerts[alertName]["lastValue"] = self.alerts[alertName]["value"]
			self.alerts[alertName]["lastValueTime"] = self.alerts[alertName]["time"]
			self.alerts[alertName]["time"] = dateTime

			if self.alerts[alertName]["delay"] < timeElapsed:
				if self.alerts[alertName]["scale"] != None:
					self.alerts[alertName]["value"] = value * self.alerts[alertName]["scale"]
				else:
					self.alerts[alertName]["value"] = value

				if self.alerts[alertName]["value"] != self.alerts[alertName]["lastValue"]:
					self.alerts[alertName]["change"] = 3 ##indicating any Change
					self.alerts[alertName]["status"] = "Value Changed"
				else:
					self.alerts[alertName]["change"] = 0

				if self.alerts[alertName]["max"] != None:
					if self.alerts[alertName]["value"] > self.alerts[alertName]["max"]:
						self.alerts[alertName]["change"] = 1 ##indicating above max value
						self.alerts[alertName]["status"] = "Value Above Max Limit"

				if self.alerts[alertName]["min"] != None:
					if self.alerts[alertName]["value"] < self.alerts[alertName]["min"]:
						self.alerts[alertName]["change"] = 2 ##indicating below min value
						self.alerts[alertName]["status"] = "Value Below Min Limit"
			else:
				self.alerts[alertName]["value"] = value

		except Exception as e:
			print("Alert Name Does Not Exist: ",e)


	def checkForChanges(self,sendEmail=False):

		self.newAlerts = {}
		self.email.body = ""

		for key in self.alerts:
			if self.alerts[key]["change"] != 0:
				self.newAlerts.update({key:self.alerts[key]["time"]})
		#print(self.newAlerts)

		if self.newAlerts != {}:
			for j in self.newAlerts:
				self.email.body += """<tr>
						    <td align="center">{}</td>
						    <td align="center">{}</td>
						    <td align="center">{}</td>
						    <td align="center">{}</td>
						    <td align="center">{}</td>
						  </tr>
			""".format(self.alerts[j]["time"], j, self.alerts[j]["value"],self.alerts[j]["lastValue"],self.alerts[j]["status"])
			if sendEmail == True:
				self.email.sendEmail()

		self.email.body += "<br /></table>"

		return self.newAlerts


class Email(AlertsManager):

	smtpServer = 'smtp.gmail.com' #Email Server
	smtpPort = 587 #Server Port


	def __init__(self,recipients,bccRecipients,emailUsername,emailPass):
		self.emailUsername = emailUsername
		self.emailPass = emailPass
		self.recipients =  recipients #recipients
		self.bccRecipients = bccRecipients #bcc recipients
		self.sender = "Python Alerts Manager"
		self.subject = "New Alert!"
		self.bodyHead = """<head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}
						</style></head>
						<h3>You have recieved new alerts!</h3><br />
						<table style="width:80%">
						  <tr>
						    <th align="center">Date/Time</th>
						    <th align="center">Name</th> 
						    <th align="center">Current Value</th>
						    <th align="center">Previous Value</th>
						    <th align="center">Reason</th>
						  </tr>"""
		self.bodyType = "html"


	def sendEmail(self):

		with smtplib.SMTP(self.smtpServer, self.smtpPort) as s:
			s.ehlo()
			s.starttls()
			s.ehlo()
			s.login(self.emailUsername, self.emailPass)	
			#s.set_debuglevel(1)

			rcpts = self.recipients + self.bccRecipients

			msg = MIMEMultipart()
			msg.attach(MIMEText(self.bodyHead + self.body,self.bodyType))
			msg['Subject'] = "{}".format(self.subject)
			msg['From'] = '"{}"'.format(self.sender)
			msg['To'] = ", ".join(self.recipients)

			try:
				s.sendmail(self.emailUsername,rcpts,msg.as_string())
			except Exception as e:
				print("EMAIL SEND FAILURE: ", e)



