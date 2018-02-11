import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import parsedatetime as pdt

def getTime(column):
	time = str(column)[52:-148] #Get the time from the HTML code, formatted incorrectly
	hour = int(time[:-3]) - 5 #Return the hour of the time to be fixed
	if (hour < 0):
		hour = hour + 24
	if (hour >= 12):
		hour = hour - 12
		time = str(hour) + time[-3:] + " PM"
	else:
		time = str(hour) + time[-3:] + " AM"
	return time

def getNetwork(column):
	network = str(column.contents)[1:-1]
	if (len(network) == 0): #The game isn't being streamed live
		return "N/A"
	elif (len(network) >= 4 and len(network) <= 8): #The network is listed in plain text and not an image
		return network[1:-1]
	else:
		network = network.split("alt=",1)[1]
		if (network[5] == '3'): #ESPN3 has different tag documentation
			network = network[1:-97]
		elif (network[5] == '"'): #ESPN & SECN have only 4 letters
			network = network[1:-389] 
		else: #ESPN2 & ESPNU
			network = network[1:-388]
		return network

def getTeamName(column):
	text = column.text.replace('&nbsp;', '')
	text = text.rsplit(' ', 1)[0]
	return text
	
#Used solely for testing purposes
def printGames(games):
	for row in games:
		print(row)
		
def setMessageElements(games):
	msg = ""
	count = 0
	for row in games:
		for data in row:
			count += 1
			msg += data
			if (count == 1):
				msg += " @ "
			elif (count != 4):
				msg += " - "
		count = 0
		msg += "\n--------------------------\n"
	return msg
		
		
def sendEmail(data):
	FROMADDR = "variousemaillists@gmail.com"
	LOGIN    = FROMADDR
	PASSWORD = "SuperSecretPassword!1996"
	TOADDRS  = ["JasonG7234@gmail.com", "r.torino97@gmail.com"]
	SUBJECT  = "NCAAM Daily Schedule"

	msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
		% (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
		
	msg += setMessageElements(data)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	#server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.login(LOGIN, PASSWORD)
	server.sendmail(FROMADDR, TOADDRS, msg)
	server.quit()


url = 'http://www.espn.com/mens-college-basketball/schedule'
#url = 'http://www.espn.com/mens-college-basketball/schedule/_/date/20180306/group/50'
#Used solely for testing purposes ^
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "html.parser")
table = soup.find('tbody')
parser = pdt.Calendar(pdt.Constants())

columnNum = 0
list_of_rows = []
for row in table.findAll('tr'):
	list_of_cells = []
	for column in row.findAll('td')[0:4]:
		columnNum += 1
		if columnNum == 3:
			text = getTime(column)
		elif columnNum == 4:
			text = getNetwork(column)
		else:
			text = getTeamName(column)
		list_of_cells.append(text)
	list_of_rows.append(list_of_cells)
	columnNum = 0

#printGames(list_of_rows)
sendEmail(list_of_rows)

