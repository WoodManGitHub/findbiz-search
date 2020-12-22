import re
import time
import json
import random
import string
import argparse

from bs4 import BeautifulSoup
from selenium import webdriver
from json2html import *

from util.crawler import BrowserDriverCrawler


class ExtractData(object):
    def __init__(self, searchName):
        self.searchName = searchName
    
    def ToJson(self):
        soup = BrowserDriverCrawler().LaunchFirefox(self.searchName)
        txt = soup.findAll('table', class_='table table-striped')[0].text
        pre = re.findall('[^\n\t\xa0]+', txt)

        d = {
                '公司基本資料': {
                    '統一編號': '',
                    '公司狀況': '',
                    '公司名稱': '',
                    '章程所訂外文公司名稱': '',
                    '資本總額(元)': '',
                    '實收資本額(元)': '',
                    '代表人姓名': '',
                    '公司所在地': '',
                    '登記機關': '',
                    '核准設立日期': '',
                    '最後核准變更日期': '',
                    '所營事業資料': ''
                }
            }

        ix = 0
        while ix < len(pre):
            if (pre[ix] == '統一編號') and (pre[ix + 1] != '公司狀況'):
                d['公司基本資料']['統一編號'] = pre[ix + 1]
    
            elif (pre[ix] == '公司狀況') and (pre[ix + 1] != '公司名稱'):
                d['公司基本資料']['公司狀況'] = pre[ix + 1]

            elif (pre[ix] == '公司名稱') and (pre[ix + 1] != '章程所訂外文公司名稱'):
                d['公司基本資料']['公司名稱'] = pre[ix + 1]

            elif (pre[ix] == '章程所訂外文公司名稱') and (pre[ix + 1][:4] != '資本總額'):
                d['公司基本資料']['章程所訂外文公司名稱'] = pre[ix + 1]

            elif pre[ix][:4] == '資本總額':
                num = re.findall('[0-9]+', pre[ix].replace(',', ''))
                d['公司基本資料']['資本總額(元)'] = int(str(num).strip('[\'').strip('\']'))

            elif (pre[ix] == '實收資本額(元)') and (pre[ix + 1] != '代表人姓名'):
                d['公司基本資料']['實收資本額(元)'] = int(pre[ix + 1].replace(',', ''))

            elif (pre[ix] == '代表人姓名') and (pre[ix + 1] != '公司所在地'):
                d['公司基本資料']['代表人姓名'] = pre[ix + 1]

            elif (pre[ix] == '公司所在地') and (pre[ix + 1] != '電子地圖'):
                d['公司基本資料']['公司所在地'] = pre[ix + 1]

            elif (pre[ix][:4] == '登記機關'):
                d['公司基本資料']['登記機關'] = pre[ix][4:]

            elif (pre[ix][:6] == '核准設立日期'):
                d['公司基本資料']['核准設立日期'] = pre[ix][6:]

            elif (pre[ix][:8] == '最後核准變更日期'):
                d['公司基本資料']['最後核准變更日期'] = pre[ix][8:]

            elif (pre[ix][:6] == '所營事業資料'):
                tmp = []
                ii = ix + 1
                while ii < 60:
                    try:
                        tt = pre[ii]
                        tmp.append(tt)
                    except:
                        pass
                    finally:
                        ii += 1
                d['公司基本資料']['所營事業資料'] = tmp
            ix += 1
        return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search', help='Search by company name or tax ID number.', dest='company', required=True)
    args = parser.parse_args()

    if args.company is '':
        print('Please input company name or tax ID number.')
        return;

    
    try:
        print("Please wait...")
        info = ExtractData(args.company).ToJson()
    except:
        print('Error')
        return

    items = info['公司基本資料']['所營事業資料']
    data = ''

    for item in items:
        data += item + '\n\t\t\t '

    print('統一編號\t\t {}'.format(info['公司基本資料']['統一編號']))
    print('公司狀況\t\t {}'.format(info['公司基本資料']['公司狀況']))
    print('公司名稱\t\t {}'.format(info['公司基本資料']['公司名稱']))
    print('章程所訂外文公司名稱\t {}'.format(info['公司基本資料']['章程所訂外文公司名稱']))
    print('資本總額(元)\t\t {}'.format(info['公司基本資料']['資本總額(元)']))
    print('實收資本額(元)\t\t {}'.format(info['公司基本資料']['實收資本額(元)']))
    print('代表人姓名\t\t {}'.format(info['公司基本資料']['代表人姓名']))
    print('公司所在地\t\t {}'.format(info['公司基本資料']['公司所在地']))
    print('登記機關\t\t {}'.format(info['公司基本資料']['登記機關']))
    print('核准設立日期\t\t {}'.format(info['公司基本資料']['核准設立日期']))
    print('最後核准變更日期\t {}'.format(info['公司基本資料']['最後核准變更日期']))
    print('所營事業資料\t\t {}'.format(data))

if __name__ == '__main__':
    main()
