## linkedin-email-scraper-selenium

Selenium based scraper to gather email addresses, your connections
share with you, but are (unfortunately) not exported in the data package, LinkedIn let's you download. 

### Information

Follow the documentation on how to set up an API Key
for Google Spreadsheets, adjust the filename,
username, password and Spreadsheet name.

Import a recent Connections.csv file in Google Spreadsheets from your LinkedIn Account.


### Running:

Touch a file named `credentials.py` and enter

```
username = ''
password = ''
```

and run the container with

docker-compose

    ```
    docker-compose up --build
    ```
    

### Disclaimer

This is a Proof of Concept. 

This violates Linkedins TOS.

Only for educational purposes!

