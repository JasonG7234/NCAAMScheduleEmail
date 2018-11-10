# NCAAMScheduleEmail
Python file that scrapes ESPN's college basketball schedule page. 

Runs in conjunction with Windows Scheduler every morning during the season at 11:00 AM.
I had to choose 11:00 AM just because sometimes the ESPN NCAAM Schedule page does not get updated with the new day's schedule until around then, so I couldn't make it any earlier which is mildly frustrating. 

Utilizes smtplib to send the email and BeautifulSoup to scrape the web page. 

If you want to be added to the email list rather than creating it yourself you can just clone/commit the branch. Leave your email in the documentation and I can add you. Check the details here for more information. https://stackoverflow.com/questions/12686545/how-to-leave-a-message-for-a-github-com-user

NEXT: 
 - Ideally, I update this project before the end of the season with the Flask framework, so that I can make the plain text emails look nice and more easily readable. 
 - I also want to fix a bug dealing with Daylight Savings time. Unless manually corrected it throws the hours off of the time of the games.
 - Fix the bug where it errors when printing out if a game is LIVE. 
