import pandas as pd
import os

class Data:
    def __init__(self, filename, datalist):
        self.columns = ['date', 'patch_version', 'team1', 'team2', 'team1_win',
                 'team1_top_champ', 'team1_jungle_champ', 'team1_mid_champ', 'team1_adc_champ', 'team1_support_champ',
                 'team2_top_champ', 'team2_jungle_champ', 'team2_mid_champ', 'team2_adc_champ', 'team2_support_champ',
                 'team1_top_player', 'team1_jungle_player', 'team1_mid_player', 'team1_adc_player', 'team1_support_player',
                 'team2_top_player', 'team2_jungle_player', 'team2_mid_player', 'team2_adc_player', 'team2_support_player'
                 ],
        self.filename = filename
        self.datalist = datalist
        self.df = pd.DataFrame(self.datalist, columns = self.columns[0])
        
    def init_insert(self):
        csv_file_name = self.filename
        self.df.to_csv(os.getcwd() + '/csv/' + csv_file_name)
        
    def insert(self):
        # To Be Implemented
        return None
    
    def integrate(self):
        year = ['2020', '2021', '2022', '2023']
        season = ['Spring', 'Summer']
        csvfiles = []
        for i in year:
            for j in season:
                filename = 'lck' + i + '_' + j + '_data.csv'
                csvfiles.append(pd.read_csv(os.getcwd() + '/csv/' + filename))
        
        res = pd.concat(csvfiles)
        res.sort_values(by=['date'], axis=0, ascending=True, inplace=True, ignore_index=True)
        res.drop(['Unnamed: 0'], axis=1, inplace=True)
        res = res.reset_index(drop=True)
        
        res.to_csv(os.getcwd() + '/csv/lck_data.csv')
    