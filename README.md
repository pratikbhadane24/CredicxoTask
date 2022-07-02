# Approach to the Problem

## 1. Firstly, we initialize the selenium webdriver.

## 2. Then, we navigate to a working url of the website we want to scrape. And then we locate the corresponding elements.

## 3. Finally, we extract the data from the elements and return it using a function.

## 4. We repeat this process for all the elements we want to scrape. Thus we download the excel file.

### NOTE: We could have used the gspread library to do this but we don't have the API creds for OAuth to access to the Google Sheet.

## 5. We structure our recevied data and write it in JSON and inseert it in the MongoDB.
