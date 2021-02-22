#!usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 3:  Expressions"""

import argparse
import urllib
import csv
import re


def download_data(url):
    """
    Args:
        url (str): A string for a website URL.
    Returns:
        data_content : Content of CSV File.
    Examples:
        >>> download_data('http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')
    """
    data_content = urllib.urlopen(url)
    return data_content


def process_data(content):
    """
    Args:
        content:
    Returns:
        None
    Examples:
        >>> process_data('http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv')
            Total of 9800 page hits today.
            Images account for 43.5% of all request.
            Google Chrome is browser top used with 4042 hits.
    """
    counts = {'imagehit': 0,
              'rowcount': 0}

    browsers = {'Internet Explorer': 0,
                'Firefox': 0,
                'Google Chrome': 0,
                'Safari': 0}

    for line in csv.reader(content):
        counts['rowcount'] += 1
        if re.search(r"jpe?g|JPE?G|GIF|PNG|gif|png", line[0]):
            counts['imagehit'] += 1
        if re.search("MSIE", line[2]):
            browsers['Internet Explorer'] += 1
        elif re.search("Chrome", line[2]):
            browsers['Google Chrome'] += 1
        elif re.search("firefox", line[2], re.I):
            browsers['Firefox'] += 1
        elif re.search("Safari", line[2]) and not re.search("Chrome", line[2]):
            browsers['Safari'] += 1

    image_cal = (float(counts['imagehit']) / counts['rowcount']) * 100
    top_browsed = [max(b for b in browsers.items())]
    resultname = top_browsed[0][0]
    resultnum = top_browsed[0][1]

    report = ("Total of {} page hits today.\n"
              "Images account for {} % of all requests.\n"
              "{} is browser top used with {} hits.").format(counts['rowcount'],
                                                             image_cal,
                                                             resultname,
                                                             resultnum)
    print(report)


def main():
    """
    Args:
        #parser (class): Argument parser instance for terminal use.
        #args (class): Argument Instance for terminal use.
    Returns:
        None
    Examples:
        >>> main()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="Enter URL Link to CSV File")
    args = parser.parse_args()

    if args.url:
        try:
            inf = download_data(args.url)
            process_data(inf)
        except urllib.URLError as url_err:
            print('URL not valid')
            raise url_err
    else:
        print('Enter a valid URL.')


if __name__ == '__main__':
    main()
