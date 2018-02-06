#!/usr/bin/python
""" /library/web.py

By David J. Thomas, thePortus.com

This module provides helper functions to get and parse web data, especially
html.

"""

# requires the requests and BeautifulSoup4 pip packages
import requests
from bs4 import BeautifulSoup


def fetch(url, retry=True):
    """
    Makes web request and returns HTML as string. Defaults to infinite retries
    """
    print('Fetching', url)
    # attempt to fetch web page
    try:
        request = requests.get(url)
    # if error in getting page, call self recursively to try again
    except Exception as err:
        print('Error fetching:')
        if retry:
            return fetch(url)
        else:
            return None
    # returning page html instead of the entire request
    return request.text


def soup(url, retry=True):
    """
    Invokes web request then returns a soup object loaded with page HTML
    """
    return BeautifulSoup(fetch(url), 'html.parser')
