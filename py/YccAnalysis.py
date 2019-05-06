import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import logging
import matplotlib.pyplot as plt
import numpy as np



class YccAnalysis:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.lgr = logging.getLogger('YccAnalysis')
        self.lgr.info('Starting Ycc Analysis...')
        self.boats = {
                      #1: 'Charm',
                      2: {'name' : 'Rising Star',
                          'type' : 'Dinghy',
                          },
                      3: {'name' : 'HiggX',
                          'type' : 'Dinghy',
                          },
                      #4: 'Beauty',
                      5: {'name' : 'Rolling Stone',
                          'type' : 'Dinghy',
                          },
                      #6: 'Isospin',
                      #7: 'Catastrophe',
                      8: {'name' : 'Catapult',
                          'type' : 'Catamarans',
                          },
                      9: {'name' : 'J\'Y-Vais',
                          'type' : 'Yngling',
                          },
                      10: {'name' : 'Y Me',
                          'type' : 'Yngling',
                          },
                      11: {'name' : 'Vas-Y',
                          'type' : 'Yngling',
                          },
                      #12: 'Miss Match',
                      13: {'name' : 'Mic Mac',
                          'type' : 'Surprise',
                          },
                      #14: 'Chick`En II',
                      15: {'name' : 'ResQ',
                          'type' : 'Motor and Service boats',
                          },
                      #16: 'Wind Surf',
                      17: {'name' : 'Gipsy',
                          'type' : 'Cabin Keel-Boat',
                          },
                      18: {'name' : 'Rocket Science',
                          'type' : 'Dinghy',
                          },
                      19: {'name' : 'Mamma Mia',
                          'type' : 'Surprise',
                          },
                      20: {'name' : 'Meerkat',
                          'type' : 'Catamarans',
                          },
                      21: {'name' : 'Pollux 201075',
                          'type' : 'Dinghy',
                          },
                      22: {'name' : 'Castor 201074',
                          'type' : 'Dinghy',
                          },
                      23: {'name' : 'RIB',
                          'type' : 'Motor and Service boats',
                          },
                      24: {'name' : 'Photon 183278',
                          'type' : 'Dinghy',
                          },
                      25: {'name' : 'Jedi',
                          'type' : 'Surprise',
                          },
                      26: {'name' : 'Obsolete Karcher APB',
                          'type' : 'Tools',
                          },
                      27: {'name' : 'Toolbox&Karcher ABP',
                          'type' : 'Tools',
                          },
                      28: {'name' : 'Aquila',
                          'type' : 'Cabin Keel-Boat',
                          },
                      29: {'name' : 'Neutrino',
                          'type' : 'Dinghy',
                          },
                      30: {'name' : 'Santa Maria',
                          'type' : 'Dinghy',
                          },
                      31: {'name' : 'La Nina',
                          'type' : 'Dinghy',
                          },
                      32: {'name' : 'J70',
                          'type' : 'Surprise',
                          },
                      33: {'name' : 'Tornado',
                          'type' : 'Catamarans',
                          },
                      34: {'name': 'Nacra 15',
                          'type': 'Catamarans',
                          },
                      }

        self.load_update_db(update = False)
        self.generate_pies()


    def generate_pie(self, df, name, colors=None, threshold=None, pctmode = 0, fontsize = 10):
        self.lgr.info('Generating pie plot {name:s}'.format(name=name))
        if not df.empty:
            fig = plt.figure()
            if threshold:
                df_t = df[df > threshold]
                df_t['Others'] = df[df <= threshold].sum()
                df = df_t
            pctopt = {0 : lambda k: '{k:1.1f}%\n {t:d}'.format(k=k, t=int(np.round(k * df.sum() / 100.0))),
                      1 : lambda k: '{t:d}'.format(t=int(np.round(k * df.sum() / 100.0))),
                      }
            plt.rcParams.update({'font.size': fontsize})
            ax = df.plot(kind = 'pie', labels=None, colors=colors, autopct=pctopt[pctmode], shadow=True)
            ax.legend(df.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=2)
            fig.savefig('../out/pdf/{name:s}_Pie.pdf'.format(name=name), orientation='portrait',bbox_inches='tight')
            plt.close()

    def generate_pies(self):
        self.generate_pie(df = self.local_logs['Status'].value_counts(), name='Status', colors=['g', 'yellow', 'r', 'w'])
        self.generate_pie(df=self.local_logs['Key Holder'].value_counts(), name='Key Holder', threshold=20, pctmode=1,
                          fontsize=4)
        self.generate_pie(df=self.local_logs['BoatName'].value_counts(), name='Boat', fontsize=4)
        self.generate_pie(df=self.local_logs['BoatType'].value_counts(), name='BoatType', fontsize=4)

        self.generate_pie_per_boat()
        # Boat types dataframe
        self.btn = pd.DataFrame({key: value['type'] for key, value in self.boats.items()}.values())[0].value_counts()
        self.bt_usage = self.local_logs['BoatType'].value_counts().to_frame('usage')
        self.bt_usage['capita'] = self.bt_usage.apply(lambda row: row / float(self.btn[row.name]), axis = 1)
        self.generate_pie(df=self.bt_usage['capita'].sort_values(ascending=False), name='Boat Type per capita', fontsize=4)

    def generate_pie_per_boat(self):
        for id, data in self.boats.items():
            self.generate_pie(df=self.local_logs[self.local_logs['BoatName'] == data['name']]['Status'].value_counts(), name='Status_boat_{boat:s}'.format(boat=data['name']),
                              colors=['g', 'yellow', 'r', 'w'])
            self.generate_pie(df=self.local_logs[self.local_logs['BoatName'] == data['name']]['Key Holder'].value_counts(), name='Key Holder_boat_{boat:s}'.format(boat=data['name']),
                              pctmode=1, fontsize=4)






    def generate_skippers_pie(self):
        df = self.local_logs['Status'].value_counts()


    def load_update_db(self, update = False):
        self.lgr.info('Loading local database...')
        self.log_path = '../db/log.db'
        self.local_logs = pd.read_pickle(self.log_path)
        self.lgr.info('Local log: {n:d} entries'.format(n=len(self.local_logs)))
        if update:
            self.lgr.info('Please type the user name...')
            self.username = input()
            self.lgr.info('Please type the password...')
            self.password = input()
            chrome_options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=chrome_options)
            # self.usage_log_url_fmt = 'https://yachting.web.cern.ch/yachting/cgi-bin/res/login.pl?urlfrom=view_log_12months.pl?boat_ID={id:d}'
            self.usage_log_url_fmt = 'https://yachting.web.cern.ch/yachting/cgi-bin/res/login.pl?urlfrom=view_log.pl?boat_ID={id:d}'
            remote_logs = self.get_all_logs()
            self.driver.close()
            self.lgr.info('Updating local database...')
            self.lgr.info('Remote log: {n:d} entries'.format(n=len(remote_logs)))
            concat_logs = pd.concat([self.local_logs, remote_logs])
            self.local_logs = concat_logs.drop_duplicates()
            self.local_logs.to_pickle(self.log_path)
            self.lgr.info('Updated local log: {n:d} entries'.format(n=len(self.local_logs)))

        self.local_logs['BoatType'] = self.local_logs.apply(lambda row: self.boats[row['boat']]['type'], axis=1)
        self.local_logs['BoatName'] = self.local_logs.apply(lambda row: self.boats[row['boat']]['name'], axis=1)
        #self.local_logs = self.local_logs.replace({'boat': {key:value['name'] for key,value in self.boats.items()}})

        #self.local_logs.replace({'boat': {key: value['name'] for key, value in self.boats.items()}})



    def get_log_pd(self, id):
        self.driver.get(self.usage_log_url_fmt.format(id=id))
        self.driver.find_element_by_name('LOGON_ID').send_keys(self.username)
        self.driver.find_element_by_name('LOGON_PASSWD').send_keys(self.password)
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


    def print_pd(self,data):
        print(tabulate(data, headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    self = YccAnalysis()
    print()
