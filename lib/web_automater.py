from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from lib.ingredient import Ingredient
import json

def search_for_item( browser, item_string, quantity ):
    if( quantity < 1 ):
        print( 'Error' )
        return

    browser.get( 'https://www.instacart.com/store/aldi/search_v3/{}'.format(
        item_string.replace( r'%', r'%25' ).replace( ',', r'%2C' ).replace( ' ', r'%20' ) ) )

    browser.find_element_by_xpath(
        '//button[@aria-label="Add 1 item {}"]'.format( item_string ) ).click()

    for i in range( 1, quantity ):
        browser.find_element_by_xpath(
            '//button[@aria-label="Increment quantity of {}"]'.format( item_string ) ).click()

def build_cart( shopping_list ):

    opts = Options()
    if False:
        opts.set_headless()

    browser = Chrome( options=opts )
    browser.implicitly_wait( 30 )
    browser.get( 'https://www.instacart.com/store/home' )

    # Log in
    browser.find_element_by_xpath( '//button[text()="Log in"]' ).click()
    browser.find_element_by_xpath(
        '//button[text()="Continue with Google"]' ).click()

    # Get credentials
    with open( 'credentials/instacart_credentials.json' ) as f:
        data = json.load( f )

    username = data[ 'username' ]
    password = data[ 'password' ]

    # Enter Username
    username_input = browser.find_element_by_xpath(
        '//input[@type="email"]' )
    username_input.send_keys( username )

    browser.find_element_by_xpath(
        '//span[text()="Next"]/parent::button' ).click()

    # Enter Password
    wait = WebDriverWait( browser, 60 )
    password_input = wait.until( EC.element_to_be_clickable( ( By.XPATH, '//input[@type="password"]' ) ) )
    password_input.send_keys( password )

    browser.find_element_by_xpath(
        '//span[text()="Next"]/parent::button' ).click()

    # Wait for the page to load to complete login
    wait.until( EC.element_to_be_clickable( ( By.XPATH, '//button[@data-identifier="cart_view_button"]' ) ) )

    # Go to the ALDI storefront page
    browser.get( 'https://www.instacart.com/store/aldi/storefront' )

    # Clear the cart if it is filled
    browser.find_element_by_xpath(
        '//button[@data-identifier="cart_view_button"]' ).click()

    remove_buttons = browser.find_elements_by_xpath(
        '//button[text()="Remove"]' )
    for remove_button in remove_buttons:
        remove_button.click()

    for item in shopping_list:
        try:
            search_for_item( browser, item.name, item.quantity )
        except:
            print( item.name + " was not found." )
            continue

    # Wait for the page to be manually closed by the user
    while True:
        try:
            browser.get_window_position()
            continue
        except:
            break
