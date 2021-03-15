# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import argparse
import logging
import datetime
import urllib.request
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        file_content = response.read().decode('utf-8')
    return file_content

def processData(file_content):
    logger = logging.getLogger("assignment2")
    data_list = file_content.split('\n')

    webData = {}
    lineum = 0
    for line in data_list:
        lineum = lineum +1
        info = line.split(',')
        if len(info) < 3 or lineum == 1:
            continue
        else:
            try:
                date =   datetime.datetime.strptime(info[1], "%Y-%m-%d %H:%M:%S")
                address = info[0]
                browser = info[2]
                status = info[3]
                size = info[4]
                #print("blah")
                data_tuple = (date, browser, status, size)
                #saving as a list of tuples as one image is accessed different number of times
                if address not in webData.keys():
                    webData[address] = [data_tuple]
                else:
                    webData[address].append(data_tuple) 
            except:
                logging.error("Error processing line #" + str(lineum) + "for ID #" +str(info[0]))
    #print(webData)
    return webData

def imageHit(data):
    total = 0
    images = 0
    for i in data.keys():
        if  re.search(r"\.png$|\.PNG$", i) or re.search(r"\.gif$|\.GIF$", i) or re.search(r"\.jpg$|\.JPG$", i) or re.search(r"\.jpeg$|\.JPEG$", i):
            #print(i)
            images += len(data[i])
        else:
            #print("Here",i)
            pass
        total += len(data[i])
    percent = images / total *100
    #print(total, images)
    #print(data.keys())
    return percent
            
def popular_browser(data):
    browser_string = ""
    for v in data.values():
        for i in v:
            #print(i[1])
            browser_string += i[1]+", "
    #print(browser_string)
    browser_list = ["Mozilla","Chrome","Safari","Internet\sExplorer"]
    d = {}
    for i in browser_list:
        d[i] = len(re.findall(i,browser_string))

    pop_browser = ""
    max_used = 0

    for k,v in d.items():
        if v > max_used:
            max_used = v
            pop_browser = k

    return("The most popular browser is "+pop_browser+" with "+str(max_used)+" hits.")

    #result = re.findall("Mozilla",browser_string)
    #result2 = re.findall("Chrome",browser_string)
    #result3 = re.findall("Safari",browser_string)
    #result4 = re.findall("Internet\sExplorer", browser_string)
    #l = [result1,result2,result3,result4]
    #print(len(result),len(result2),len(result3),len(result4))
    

def main(url):
    print(f"Running main with URL = {url}...")
    try:
        file_content = downloadData(url)
        webData = processData(file_content)
        imageReq = imageHit(webData)
        print("Image requests account for "+str(imageReq)+" of all requests")
        print(popular_browser(webData))
    
    except Exception as e:
        print (str(e))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    logger = logging.getLogger("assignmet")
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    main(args.url)
