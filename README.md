# NCAAMScheduleEmail
## Python file that scrapes ESPN's college basketball schedule page. 

### Description
Utilizes BeautifulSoup to scrape thee ESPN college basketball schedule page, organizes it into an HTML table, and sends it via smtplib. 

### Latest Commit
Bug fix for when Scheduler runs when game is currently going on. Previously, the file would not be able to read the LIVE score because it was looking for a numeric value. 

### FAQ
> How can I get added to the list?
If you want to be added to the email list rather than creating one for yourself there are two options.
1. You can email me at[JasonG7234@gmail.com](mailto:JasonG7234@gmail.com).
2. You can just clone/commit the branch. Leave your email in the documentation and I can add you. Check the details [here](https://stackoverflow.com/questions/12686545/how-to-leave-a-message-for-a-github-com-user) for more information. 
Hopefully down the line I can link to a Google Form to be filled out. 

> Can I help with the project?
Of course! I can always use help. Probably best bet is to reach me by email, but pull requests work too. 

> This is the greatest project ever where can I learn more about you/hire you/pay you obscene amounts of money?
Wow I really appreciate the kind words! You can find out more about me on my website [here](http://jasongomes.me) and my Venmo is @Jason-Gomes ;-)

### To Do: 
 - Ideally, I update this project before the end of the season with the Flask framework, so that I can make the plain text emails look nice and more easily readable. 
 - I also want to fix a bug dealing with Daylight Savings time. Unless manually corrected it throws the hours off of the time of the games.
 - Add support for multiple sports. 
 - Include database for each email and settings stored with each. So if I add support for CBB, NBA, and MLB games and someone only wants to receive CBB and NBA, give them the option.
 - Add option for scores postgame.
 - Finally, potentially down the line add some sort of reddit integration. For one, it would be cool to add links to post game threads for sporting games. 
