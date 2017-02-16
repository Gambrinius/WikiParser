import sys
import csv
import requests
from bs4 import BeautifulSoup

__author__ = 'Ilya Konon'


def read_csv_file(filename):
    """
    Read data from input csv file
    :param filename:
    :return: urls list
    """
    urls_list = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls_list.append(row[0])

    return urls_list


def write_csv_file(filename, dictionary):
    """
    Write date into output csv file
    :param filename:
    :param dictionary:
    :return:
    """
    with open(filename, 'w') as csvfile:
        fieldnames = ['wikipedia_page_url', '​website_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'wikipedia_page_url': 'wikipedia_page_url', '​website_url': '​website_url'})   # write headers
        for key, value in dictionary.items():   # write rows
            writer.writerow({'wikipedia_page_url': key, '​website_url': value})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            result_dict = {}  # for results of parsing
            page_urls = read_csv_file(sys.argv[1])

            for url in page_urls:
                r = requests.get(url)
                # filename = "%s.html" % url.split('/')[-1]

                soup = BeautifulSoup(r.text.encode('utf-8'), "lxml")
                tr_list = soup.find_all('tr')

                for tr in tr_list:
                    if tr.find('th', text='Website'):
                        company_link = tr.find('td').find('a').get('href')

                        result_dict[url] = company_link
                        break

            output_csv_filename = 'wikipedia_answers.csv'
            write_csv_file(output_csv_filename, result_dict)

        except FileNotFoundError as e:
            print("Error: %s" % e.strerror)
    else:
        print("Error: missed argument, name of csv file")
