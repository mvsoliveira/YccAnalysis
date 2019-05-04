import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

class YccAnalysis:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=chrome_options)
        #self.usage_log_url_fmt = 'https://yachting.web.cern.ch/yachting/cgi-bin/res/login.pl?urlfrom=view_log_12months.pl?boat_ID={id:d}'
        self.usage_log_url_fmt = 'https://yachting.web.cern.ch/yachting/cgi-bin/res/login.pl?urlfrom=view_log.pl?boat_ID={id:d}'
        self.log_path = '../db/log.db'
        self.local_logs = pd.read_pickle(self.log_path)
        print(len(self.local_logs))
        #self.update_db()
        #print(len(self.local_logs))

    def update_db(self):
        remote_logs = self.get_all_logs()
        concat_logs = pd.concat([self.local_logs, remote_logs])
        self.local_logs = concat_logs.drop_duplicates()


    def get_log_pd(self, id):
        self.driver.get(self.usage_log_url_fmt.format(id=id))
        self.driver.find_element_by_name('LOGON_ID').send_keys('')
        self.driver.find_element_by_name('LOGON_PASSWD').send_keys('')
        self.driver.find_element_by_name('.submit').click()
        soup = BeautifulSoup(self.driver.page_source,features="lxml")
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table))
        return df[0]['Usage log']

    def get_all_logs(self):
        logs = pd.DataFrame()
        for id in range(1,35):
            data = self.get_log_pd(id)
            data['boat'] = pd.Series([id] * len(data), index=data.index)
            if logs.empty:
                logs = data
            else:
                logs = pd.concat([logs,data])

        return logs

    def save_log(self, df):
        df.to_pickle('log.db')


    def print_pd(self,data):
        print(tabulate(data, headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    Ycc = YccAnalysis()
    print()
