import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import parsedatetime as pdt

#Returns the time that game goes on
#This is done by interpreting the HTML code of the date_time
#The file 
def getTime(column):
	time = str(column)[52:-148]
	hour = int(time[:-3]) - 5
	if (hour < 0):
		hour = hour + 24
	if (hour > 12):
		hour = hour - 12
		time = str(hour) + time[-3:] + " PM"
	else:
		time = str(hour) + time[-3:] + " AM"
	return time

#Returns the network the game can be found on
#This is done be returning the alt tag on all of the images
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

#Used for testing purposes
def printGames(games):
	for row in games:
		print(row)
		
def setMessageElements(content):
	message = '''
	<head>
	</head>
	<body>
		<table>
			{0}
		</table>
	</body>
	'''
	tr = "<tr>{0}</tr>"
	td = "<td>{0}</td>"
	subitems = [tr.format(''.join([td.format(a) for a in item])) for item in content]
	return message.format("".join(subitems))
		
def sendEmail(data):
	SUBJECT = "NCAAM Daily Schedule"
	FROMADDR = #YOUR SENDING EMAIL
	FROMPASSWORD = #YOUR SENDING EMAIL PASSWORD
	TOADDR = #YOUR RECEIVING EMAILS IN LIST FORMAT
	
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = SUBJECT
	MESSAGE['From'] = FROMADDR
	MESSAGE.preamble = '''
	Your mail reader does not support the format.
	Please visit the ESPN page <a href="http://www.espn.com/mens-college-basketball/schedule">here.</a>
	'''
	HTML_BODY = MIMEText(setMessageElements(data), 'html') #Record MIME type text/html
	MESSAGE.attach(HTML_BODY)
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(FROMADDR, FROMPASSWORD)
	
	for email in TOADDR:
		MESSAGE['To'] = email
		server.sendmail(FROMADDR, [email], MESSAGE.as_string())
		
	server.quit()

url = 'http://www.espn.com/mens-college-basketball/schedule'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "html.parser")
table = soup.find('tbody')
parser = pdt.Calendar(pdt.Constants())

count = 0
list_of_rows = []
for row in table.findAll('tr'):
	list_of_cells = []
	for column in row.findAll('td')[0:4]:
		count += 1
		if count == 3:
			text = getTime(column)
		elif count == 4:
			text = getNetwork(column)
		else:
			text = column.text.replace('&nbsp;', '')
		list_of_cells.append(text)
	list_of_rows.append(list_of_cells)
	count = 0

#printGames(list_of_rows)
sendEmail(list_of_rows)
