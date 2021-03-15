import time
import pandas
import csv
import requests
import autoit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
# replace with a csv file name e.g. example.csv
file_name = "your file name goes here"
# these will be the headers for your file columns
header = ("Total Recommendations", "Job", "Name", "Number")
# initial test data for csv file
data = [
    (0, "Test", "Tester", "12345678")
]
job = ""
name = ""
number = ""


# used to initialize and now append new inputs into file
def writer(header, data, file_name):
    with open(file_name, "a", newline="") as csvfile:
        rec = csv.writer(csvfile)
        for x in data:
            rec.writerow(x)


# checks to see if a person is already in csv file if yes it will add 1 to their recommendations
def check(job, name, number, file_name):
    job = job.lower()
    name = name.lower()
    with open(file_name, "r+", newline="") as file:
        readData = [row for row in csv.DictReader(file)]
        df = pandas.read_csv(file_name)
        print(len(df.index))
        for rows in range(len(df.index)):
            if job == readData[rows]["Job"] and name == readData[rows]["Name"]:
                df.loc[rows, "Total Recommendations"] +=1
                df.to_csv(file_name, index=False)
                return True


# will check sheet to see if person is on it if not will append them to sheet
def update(job, name, number, file_name):

    fields = [
        (0, job, name, number)
    ]
    with open(file_name, "r+", newline="") as file:
        writer(header, fields, file_name)


# displays specific job results
def results(file_name, job):
    string = ""
    with open(file_name, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row['Job'] == job]
        for row in rows:
            result = dict(row)
            string += str(result) + "\n"
    if string == "":
        string = "Doesn't look like there are any recommendations for that job."
    string = string.replace("'", "")
    string = string.replace("}", "")
    string = string.replace("{", "")
    input_box.send_keys(string + Keys.ENTER)
    time.sleep(10)


# sends photos or videos that are saved to computer (must be of an acceptable format for whatsapp web.)
def send_photo(file_path):
    file_path = file_path.replace("/", "\\")
    attach_button = driver.find_element_by_xpath('//div[@title="Attach"]')

    attach_button.click()
    time.sleep(1)
    photo_button = driver.find_element_by_xpath('//span[@data-testid="attach-image"]')
    photo_button.click()
    time.sleep(1)

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", file_path)
    autoit.control_click("Open","Button1")
    time.sleep(1)

    send_button = driver.find_element_by_xpath('//div[@class="SncVf _3doiV"]')
    send_button.click()
    print("Couldn't send file")

driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 20)

# replace with name of friend or group you are using the bot with
target = 'Targets Name'
string = ""
x_arg = '//div[@class="_2_1wd copyable-text selectable-text"][@dir="ltr"][@data-tab="3"]'
group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
time.sleep(1)
group_title.click()
group_title.send_keys(target +  Keys.ENTER)
inp_xpath = '//div[@class="_2_1wd copyable-text selectable-text"][@dir="ltr"][@data-tab="6"]'
input_box = wait.until(EC.presence_of_element_located((
    By.XPATH, inp_xpath)))


# The bot will continue running until you decide to stop it
while True:

    last_message = driver.find_elements_by_xpath('//span[@dir="ltr"][@class="_3-8er selectable-text copyable-text"]//span')[-2].text
    new_message = driver.find_elements_by_xpath('//span[@dir="ltr"][@class="_3-8er selectable-text copyable-text"]//span')[-1].text

    if last_message != new_message:
        if "!plumber" in new_message.lower():
            results(file_name,"plumber")

        elif "!recommend" in new_message.lower():
            string = "To recommend someone for future lookup please use the following format without the space between"\
                    + "! and rec"
            input_box.send_keys(string + Keys.ENTER)
            string = "! rec '1job' '2name' '3number'. for example ! rec 1architect 2John Doe 312345678."
            time.sleep(1)
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)
        elif "!rec" in new_message.lower():
            up = new_message.split()
            full_job = []
            for word in range(1, len(up)):
                if up[word][0] == "1":
                    job = up[word][1:].lower()
                    print(up[word])

                elif up[word].isalpha() and up[-4][0] != "1" and len(full_job) != 2:
                    job += " " + up[word].lower()
                    print(up[word])
                    print(job)
                    full_job = job.split()
                elif up[word][0] == "2":
                    name = up[word][1:].lower()
                    print(up[word])

                elif up[word].isalpha() and len(full_job) == 2:
                    name += " " + up[word].lower()
                    print(up[word])
                    print(name)

                elif up[word][0] == "3":
                    number = up[word][1:].lower()
                    print(up[word])

            if not check(job, name, number, file_name):
                update(job, name, number, file_name)
            string = "Successfully added/recommended."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!alarm" in new_message.lower():
            string = "BEEP BEEP BEEP IT'S TIME FOR THAT THING"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!bowling" in new_message.lower():
            string = "Looks like we're on a roll now hehe get it because in bowling you roll the ball. no ok."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!suggestion" in new_message.lower():
            string = "Hold on let me get my notepad ya just give me one sec ............."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!mathtutor" in new_message.lower():
            results(file_name, "math tutor")

        elif "!insult" in new_message.lower():
            r= requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
            if r.status_code == 200:
                data = r.json()
                insult = f'{data["insult"]}'
                string = insult
            else:
                string = "Sorry that feature isn't  working at this time"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(10)

        elif "!kanye" in new_message.lower():
            r = requests.get('https://api.kanye.rest/')
            if r.status_code == 200:
                data = r.json()
                kanye = f'{data["quote"]}'
                string = kanye
            else:
                string = "Sorry that feature isn't  working at this time"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!advice" in new_message.lower():
            r = requests.get('https://api.adviceslip.com/advice')
            if r.status_code == 200:
                data = r.json()
                advice = f'{data["slip"]["advice"]}'
                string = advice
            else:
                string = "Sorry that feature isn't  working at this time"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!number" in new_message.lower():
            number = new_message.split()
            new_num = number[-1]
            if new_num.isnumeric():
                r = requests.get('http://numbersapi.com/' + new_num)
                if r.status_code == 200:
                    string = r.text
            else:
                string = "Sorry that feature isn't  working at this time"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!cardealer" in new_message.lower():
            results(file_name, "car dealer")

        elif "!electrician" in new_message.lower():
            results(file_name, "electrician")

        elif "!handyman" in new_message.lower():
            results(file_name, "handyman")

        elif "!dentist" in new_message.lower():
            results(file_name, "dentist")

        elif "!pediatrician" in new_message.lower():
            results(file_name, "pediatrician")

        elif "!travelagent" in new_message.lower():
            results(file_name, "travel agent")

        elif "!info" in new_message.lower():
            string = "This bot was created for fun by Steven Baum if you'd like to add a job results command please "\
            + "contact me. If you would like to be removed from the job database just let me know and I will do so. "\
            + "Also this bot will most likely break the moment whatsapp does anything stupid which happens very often."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!hi" in new_message.lower():
            string = "Hi there."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)

        elif "!commands" in new_message.lower():
            string = "All commands at this moment are the  following just remove the space after the ! to execute them."\
                     + " ! plumber, ! electrician, ! cardealer, ! travelagent, ! pediatrician, " \
                     + "! dentist, ! handyman, ! mathtutor, ! recommend, ! rec, ! info."\
                     + "The following commands are meant for fun."\
                     + " ! insult, ! advice, ! number #, ! kanye, ! suggestion, ! bowling, ! alarm"\
                     + " More to come as requested."
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)
# below calls the openweathermap api you will need to provide your own api key for it to work.
        elif "!weather" in new_message.lower():

            weather = new_message.split()
            if len(weather) == 3:
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + weather[-2] + "+" + weather[-1]
                                 + '&units=imperial&appid=')
            else:
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + weather[-1]
                             + '&units=imperial&appid=')
            if r.status_code == 200:
                data = r.json()
                curr_weather_condition = f'{data["weather"][0]["main"]}'
                if curr_weather_condition == "Clouds":
                    curr_weather_condition = "cloudy"
                curr_weather_feel = f'{data["main"]["feels_like"]}'
                curr_weather_temp = f'{data["main"]["temp"]}'
                curr_weather_wind = f'{data["wind"]["speed"]}'
                if len(weather) == 3:
                    string = "The weather in " + weather[-2] +" " + weather[-1] + " is currently "\
                             + curr_weather_condition + ". The current temperature is " + curr_weather_temp\
                             + "F and feels like " + curr_weather_feel + "F and the current wind speed is "\
                             + curr_weather_wind + "mph."
                else:
                   string = "The weather in " + weather[-1] + " is currently " + curr_weather_condition \
                    + ". The current temperature is " + curr_weather_temp + "F and feels like " + curr_weather_feel \
                    + "F and the current wind speed is " + curr_weather_wind + "mph."

            else:
                string = "Sorry that feature isn't  working at this time"
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(3)
