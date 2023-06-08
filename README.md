# NYC GOV Tennis Reservation

This project automates the reservation of NYC tennis courts by utilizing Selenium and driver interaction

## Table of Contents
- [Installation](#installation)
- [Constaints](#constraints)
- [Usage](#usage)
- [Notes](#notes)

## Installation

- Install Python via https://www.python.org/getit/
- Run the following command in the terminal\
```pip install -r requirements.txt```

## Constraints
There are a couple constraints the program has. Keep these in mind when using.
- Depending on how low the monitor frequencies are, the webpage may temperarily block you for making too many requests
- Assumes all players have permits. Singles will auto choose 2 and double will auto choose 4
- Assumes the address used to fill in reservation details is the same as billing address for CC info
- Only compatible with locations you can book a week in advance. Thankfully it accounts for all except the Central Park location


## Usage
1. Edit the parameters.txt file to fill out your information and preferences.
- place = Link to reservation webpage
- date = Date in only this format YYYY-MM-DD
- timeslot = Timeslot in this format HR:00 p.m. or HR:00 a.m.  Important to indicate periods in a.m. or p.m. 
- date_monitor_freq = # of seconds you want the webpage to reload 
- timeslot_monitor_freq = # of seconds you want monitor webpage to check if timeslot is available
- play_type = Choose between singles/doubles
- name = Full first and last name
- email = Email address
- address = Address 1
- apt = Apt ***optional***
- city = City name
- zipcode = Zip Code
- phone_number = 10 digit phone number
- ccnum = 16 digit CC number
- expdate = Expiration date in MM/YY format
- cvv = 3-4 digit CVV 


Example parameters should be in the file for you to model after

2. Navigate to the directory with this project using cd *next folder* <br>
For example if the next directory is called project folder:<br> 
```cd project_folder ```<br>
Or you can also use tab after cd to tab through all your folders<br>
```cd ``` <br>
You can go back to the previous folder by:<br>
```cd .. ```<br>


3. Launch the program with:<br>
```python tennisreservation.py ```<br><br>
The program will load the reservation webpage and check whether if the date exists in the webpage. If it doesn't exist, it will keep monitoring the webpage with the frequency indicated in date_monitor_freq. If the date does exist, but the timeslot doesn't work, it'll monitor the webpage with the timeslot monitor frequency until it works. If there is a reservation slot, it will proceed to autofill your details and make the reservation.


## Notes
Occasionally you will run into chromedriver mismatch to your selenium package. Follow the instructions in this link to update your webdriver
https://www.programsbuzz.com/article/how-update-chrome-driver-selenium <br>

If you want the browser to not appear when running the program, go into the tennisreservation.py file and add # before line 58 which should be ```options.add_argument('--headless')```. Vice versa for if you want to see the browser

If you are wanting to reserve doubles and there is a reservation slot, but there isn't also a reservaion slot for the hour after the available slot, you cannot reserve doubles. Doubles require a two hour window for the reservation and this program keeps that in account. 