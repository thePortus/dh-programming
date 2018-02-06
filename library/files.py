#!/usr/bin/python
""" /library/files.py

Several helper objects to work with various kinds of files, especially loading
and saving operations.

Contents:
    Path
    TextFile
    TextFolder # TODO
    CSVFile
"""

import os
import csv
import errno
from collections import UserString


class Path(UserString):
    """
    Used to interact with a system path in various ways. Not generally meant to
    be used directly, Path is parent to various Folder and File classes.

    Example:
        if(Path('a_path.txt').is_file()):
            some_function()
    """

    def __init__(self, filepath):
        if type(filepath) is not str:
            raise Exception('filepath is not a string')
        # call parent class constructor and set to a string
        super().__init__(str)
        # if relative path sent, join it to working dir
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)
        self.data = filepath

    @property
    def exists(self):
        """
        check if anything exists at the filepath
        """
        return os.path.exists(self.data)

    @property
    def is_dir(self):
        """
        returns true if path points to existing directory
        """
        return os.path.isdir(self.data)

    @property
    def is_file(self):
        """
        returns true if path points to existing file
        """
        return os.path.isfile(self.data)

    def load(self, options={'encoding': 'utf-8'}):
        """
        Called by child class load methods, stops from loading non-extant file
        """
        print('Loading', self.data)
        if not self.exists:
            raise Exception('Cannot open item, nothing exists at' + self.data)

    def save(self, options={'overwrite': False}):
        """
        Called by child class save methods, prevents overwrite without option
        """
        print('Saving to', self.data)
        if self.exists and not options['overwrite']:
            raise Exception(
                'Item exists at ' + self.data + 'and overwrite not specified'
            )
        # create all parent directories required for save
        self.makedirs()

    def makedirs(self):
        """
        Automatically creates any parent directories of the current path
        that do not already exist.
        """
        # if parent directory is non-extant
        if not os.path.exists(os.path.dirname(self.data)):
            # attempt to make parent directories
            try:
                os.makedirs(os.path.dirname(self.data))
            # raise an error if somehow directories were created after check
            except OSError as exc:
                if exc.errno != errno.EEXist:
                    raise


class TextFile(Path):
    """
    Used to load or save a single string to a single plaintext file. Will only
    overwrite existing files if passed as a property in the options dict.

    Example:
        text = 'Lorem ipsum dolor sit amet.'
        PlainTextFile('a_path.txt').load(text, options={ 'encoding': 'utf-8' })
        PlainTextFile('a_path.txt').save(text, options={ 'overwrite': True })
    """

    def load(self,  options={'encoding': 'utf-8'}):
        """
        Opens file and returns contents as a single string
        """
        super(self.__class__, self).load(options)
        if not self.is_file():
            raise Exception('Item is not a file')
        file_data = ''
        with open(self.data, 'r+', encoding=options['encoding']) as read_file:
            file_data = read_file.read()
        return file_data

    def save(self, data, options={'encoding': 'utf-8', 'overwrite': 'false'}):
        """
        Saves string data to file, won't overwrite unless option is flagged
        """
        super(self.__class__, self).save(options)
        with open(self.data, 'w+', encoding=options['encoding']) as write_file:
            write_file.write(data)
        return True


class TextFolder(Path):
    """
    Can load or save a folder of plaintext files as a list of strings.
    """

    def load(self, options={'encoding': 'utf-8'}):
        """
        Load all .txt (or other types) in a folder as list of strings
        """
        super(self.__class__, self).load(options)
        if not self.is_folder():
            raise Exception('Item is not a folder')
        # TODO Add loading here
        pass

    def save(self, data, options={'encoding': 'utf-8', 'overwrite': False}):
        """
        Save list of strings as .txt, will be named sequentially (1.txt...)
        unless a second list of strings with equal length is passed containing
        output filenames
        """
        super(self.__class__, self).save(options)
        # TODO add saving here
        pass


class CSVFile(Path):
    """
    Makes loading and saving CSV data a simple matter. Simplifies the use
    of the csv.DictReader and csv.DictWriter for loading or saving csv's as
    lists of dictionaries.
    """

    def load(self, options={'encoding': 'utf-8'}):
        """
        Load csv as list of dictionaries.

        Example:
            loaded_data = CSVFile('a_path.csv').load()
            for data_row in loaded_data:
                print(data_row)
        """
        super(self.__class__, self).load(options)
        if not self.is_file:
            raise Exception('Item is not a file')
        data_rows = []
        with open(self.data, 'r+', encoding=options['encoding']) as csv_file:
            csv_reader = csv.DictReader(csv_file, newline='')
            for csv_row in csv_reader:
                data_rows.append(csv_row)
        return data_rows

    def save(
        self, data, fieldnames,
        options={'encoding': 'utf-8', 'overwrite': 'false'}
    ):
        """
        Save a list of dictionaries to a .csv file. You must specify
        the column headers (fieldnames) with a list of strings. Returns True
        upon success

        Example:
            sample_data = [
                {'id': 1, 'name': 'Sample1'},
                {'id': 2, 'name': 'Sample2'},
            ]
            fieldnames = ['id', 'name']
            CSVFile('a_path.csv').save(sample_data, fieldnames)
        """
        super(self.__class__, self).save(options)
        with open(self.data, 'w+', encoding=options['encoding']) as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames, newline=''
            )
            csv_writer.writeheader()
            for data_row in data:
                csv_writer.writerow(data_row)
        return True
