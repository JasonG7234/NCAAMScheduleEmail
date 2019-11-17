import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import parsedatetime as pdt
import unidecode
import datetime

dict = {'JasonG7234@gmail.com':['Rutgers', 'Seton Hall', 'Duke'], 'tjgomes@aol.com':['Rutgers', 'Seton Hall']}

#Returns the time that game goes on
#This is done by interpreting the HTML code of the date_time
#The file 
def getTime(column):
	time = str(column)[52:-148]
	#If ran when game is ON time will appear as blank
	if (time != ''):
		hour = int(time[:-3]) - 5 #If DST change this to 4
		if (hour < 0): #Normalize hour to 24 hour clock
			hour = hour + 24

		if (hour > 12): # Now parse time
			hour = hour - 12
			time = str(hour) + time[-3:] + " PM"
		elif (hour == 12):
			time = str(hour) + time[-3:] + " PM"
		else:
			time = str(hour) + time[-3:] + " AM"
	return time

#Returns the network the game can be found on
#This is done be returning the alt tag on all of the images
def getNetwork(column):
	columnIMG = column.find('img')
	if (not columnIMG):
		return column.text
	else:
		return columnIMG.get('alt')

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
	FROMADDR = "variousemaillists@gmail.com"
	FROMPASSWORD = "SuperSecretPassword!1996" 
	TOADDR = list(dict.keys())
	
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

url = 'http://www.espn.com/mens-college-basketball/schedule/_/date/' + datetime.datetime.today().strftime('%Y%m%d') + '/group/50'
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
		else: #team name
			text = column.text.replace('&nbsp;', '')
			text = text.rsplit(' ', 1)[0]
		list_of_cells.append(unidecode.unidecode(text))
	list_of_rows.append(list_of_cells)
	count = 0

#printGames(list_of_rows)
sendEmail(list_of_rows)


