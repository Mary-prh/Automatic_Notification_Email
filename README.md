# Automatic_Notification_Email

There are some libraries that are used for this project: email, and smtplib, as well as the MIMEMultipart object. This object has multiple subclasses; these subclasses will be used to build our email message. 

The first function (sendEmail) is to set up the email and a connection to our email server. Then, the message content is built. 

The main function extracts the sheet id and sheet name from a googlesheet. 

The data is read by pandas dataframe as a csv file and a new indexing is created to match with the row number of the contract in the google sheets. 

The closing date object is turned to datetime and new pandas dataframe is created that only contains the contracts which are closing in four days.

This is done using pd.DateOffset that moves dates forward/backward a given number of valid dates and then it is compared with the current date.

If such contract exsists, the sendEmail function is called.
