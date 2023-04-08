from selenium import webdriver
from random import randint
import undetected_chromedriver as uc
from undetected_chromedriver.options import ChromeOptions
import os
from selenium.webdriver.common.by import By
import time

def main():
    Selection = int(input('(1) Send Connection Requests \n(2) Withdraw all pending connections\nWhich would you like to do: '))
    LoginUser = input('\nEnter your LinkedIn email: ')
    LoginPass = input('\nEnter your LinkedIn Password: ')

    print('\nSigning in... (Takes about 10 seconds)')


    # Feel free to comment out the three lines below and uncomment the fourth one if you would like to watch the process!
    myoptions = ChromeOptions()
    #myoptions.add_argument("--headless")
    driver = uc.Chrome(options=myoptions)
    # driver = uc.Chrome
    
    # Opening LinkedIn Signinpage
    urltoSignInPage = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(urltoSignInPage)
    time.sleep(2)

    # Logging in
    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    password = driver.find_element(By.XPATH,"//input[@name='session_password']")

    username.send_keys(LoginUser)
    password.send_keys(LoginPass)
    time.sleep(2)
    submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # Login Process Complete.
    os.system('cls||clear')
    print('\nSuccessfully signed in!')

    if (Selection == 1):
        chose_Connect(driver)
    elif (Selection == 2):
        chose_withdraw(driver)

def chose_Connect(driver):
    Keywords = []
    KeywordNum = int(input('How many keywords would you like to use: '))

    for x in range(KeywordNum):
        Keywords.append(input(f'Enter Keyword {x+1}: '))
        

    maxConnect = int(input('\nHow many connection requests would you like to send? (Stay below 50 to be safe): '))
    os.system('cls||clear')
    Keywords = [w.replace(" ", "%20") for w in Keywords]
    Keywords = str.join("%20", Keywords)

    
    i = 0
    # if program is crashing, increment K variable below by 5
    k = 10
    print("\nBeginning connection request process...\nThere is a delay between requests intentionally to bypass bot detections")
    while i < maxConnect:
        try:
            # Construct the URL for the search results page
            urllink = f"https://www.linkedin.com/search/results/people/?&keywords={Keywords}&network=%5B%22S%22%2C%22O%22%5D&origin=SWITCH_SEARCH_VERTICAL&page={k}&sid=aiC&spellCorrectionEnabled=true"
            
            # Load the search results page and wait for it to load
            driver.get(urllink)
            time.sleep(2)

            # Find all the Connect buttons on the page
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

            # Loop through all the Connect buttons and send connection requests
            for btn in connect_buttons:
                driver.execute_script("arguments[0].click();", btn)
                name = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/p/span/strong").text
                print(f"Sending connection request to {name}")
                time.sleep(randint(4, 15))
                send = driver.find_element(By.XPATH, "//button[@aria-label='Send now']")
                driver.execute_script("arguments[0].click();", send)
                close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                driver.execute_script("arguments[0].click();", close)
                time.sleep(randint(4, 15))
                time.sleep(2)

            # If there are no more Connect buttons on the page, go to the next page
            if len(connect_buttons) == 0:
                k += 1
            else:
                # Update the counter for the number of connections made and go to the next page
                i += len(connect_buttons)
                k += 1

            # Print the total number of connection requests sent so far
            print(f"Connection Invitations sent = {i}")

            # Exit the loop if the maximum number of connections has been reached
            if i >= maxConnect:
                break

    # Handle any exceptions that may arise during the process
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break


def chose_withdraw(driver):
    i = 0
    urllink = "https://www.linkedin.com/notifications/?origin=SWITCH_SEARCH_VERTICAL&sid=aiC&filter=invitations_sent_people"
    driver.get(urllink)
    print('Withdrawing all current connection requests!\nPlease be aware that there is an intentional delay to avoid being banned as a bot.')
    while i < 400:
        time.sleep(2)
        all_buttons = driver.find_elements(By.XPATH,"//button/span/span[1]")    
        
        withdraw_buttons = [btn for btn in all_buttons if btn.text == "Withdraw"]

        for btn in withdraw_buttons:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(randint(6,20))
            send = driver.find_element(By.XPATH,"//button[@aria-label='Withdraw']")
            driver.execute_script("arguments[0].click();", send)
            time.sleep(randint(6,20))
        time.sleep(4)
        i+=len(withdraw_buttons)
        print("Connection Invitations withdrawn = ", i )
        more = driver.find_element(By.XPATH,"//button[@class='artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--3 artdeco-button--fluid artdeco-button--tertiary ember-view redesigned-experience__show-more-btn pv3']")
        driver.execute_script("arguments[0].click();", more)
            
    driver.quit()
    exit(0)

if __name__ == "__main__":
    main()