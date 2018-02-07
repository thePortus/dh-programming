#!/usr/bin/python
""" /library/web.py

By David J. Thomas, thePortus.com

This module provides helper functions to get and parse web data, especially
html.

"""

from collections import UserString

import requests
from bs4 import BeautifulSoup


class WebPage(UserString):
    """
    Provides methods to download/parse a specified webpage. Merges the request
    package with BeautifulSoup functions to enable users to request/soup
    a page in a single line.
    """

    def __init__(self, url, options={'delay': '2', 'max_retries': 0}):
        # call parent constructor
        super().__init__(str)
        if type(url) is not str:
            raise Exception('URL must be a string')
        self.data = url
        self.delay = options['delay']
        self.max_retries = options['max_retries']

    def fetch(self, retry_num=0):
        """
        Makes web request and returns HTML as string.
        """
        print('Fetching', self.data)
        # attempt to fetch web page
        try:
            request = requests.get(self.data)
        # if error in getting page, call self recursively to try again
        except Exception as err:
            print('Problem fetching', self.data)
            # if infinite retries is set, always try again
            if not self.max_retries:
                print('Retrying...')
                return self.fetch()
            # if below retry limit, return recursively and increment counter
            elif retry_num <= self.max_retries:
                print('Retrying')
                return self.fetch(retry_num=retry_num + 1)
            # otherwise retry limit has been hit, stop fetching
            else:
                print('Retry limit reached, skipping', self.data)
                return None
        # if everything ok, returning page html instead of the entire request
        return request.text

    def soup(self, retry=True):
        """
        Invokes web request then returns a soup object loaded with page HTML
        """
        return BeautifulSoup(self.fetch(), 'html.parser')
