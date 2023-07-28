url = [
    
    #챌린저게임 최근1달 챔피언별 승률, 게임당 픽밴율
    #'https://www.op.gg/statistics/champions?tier=challenger&region=kr'
]

def ret_init_url(lck_year, lck_season):
    return 'https://lol.fandom.com/wiki/LCK/' + lck_year + '_Season/' + lck_season + '_Season/Match_History'