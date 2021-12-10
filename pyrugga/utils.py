"""
Author: James Londal
Copyright: Copyright 2021, Picopie Ltd
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal
"""

import pyrugga as prg
import pandas as pd


def _find_files(path,extension):
    import os
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for f in files:
        # checks the name of file ends in .xml
        if '.' + extension in f.lower() :
            yield f
            
def _generate_id(df):
    hometeam = df['hometeam'].apply(lambda x: x[:3])[0].title()
    awayteam = df['awayteam'].apply(lambda x: x[:3])[0].title()

    year = df['fixture_date'].apply(lambda x: x[-2:])[0]
    month = df['fixture_date'].apply(lambda x: x[3:-5])[0]
    day = df['fixture_date'].apply(lambda x: x[:2])[0]

    fixture_id = hometeam+"v"+awayteam+"_"+day+month+year
    return fixture_id


def get_Events(FILES_LOC):
    """
    Gets a collections of files and appends multiple match events into a single dataframe
    
    get_Events('../../datalake/Rugby/pacific_nations_cup/')
    """    
    df = pd.DataFrame()

    for fn in _find_files(FILES_LOC,'xml'):
        #loads each file and stores them in an list
        match = prg.Match(FILES_LOC + fn) 

        tmp_df = match.events
        tmp_df['x_fixture_id'] = _generate_id(match.summary)

        #this is how we should have done this 
        #tmp_df['fixture_id'] = match.summary['fixture_id']

        df = pd.concat([df,tmp_df]) 
        
    return df
    
#VINNY# Looks lovely!
    
 
# appends multiple match timelines into a single dataframe
def get_Timelines(FILES_LOC):
    
    df = pd.DataFrame()

    for fn in _find_files(FILES_LOC,'xml'):
        #loads each file and stores them in an list
        match = prg.Match(FILES_LOC + fn) 

        tmp_df = match.timeline
        tmp_df['x_fixture_id'] = _generate_id(match.summary)

        #this is how we should have done this 
        #tmp_df['fixture_id'] = match.summary['fixture_id']

        df = pd.concat([df,tmp_df]) 
        
    return df 
#VINNY# Looks lovely! Question... if someone used this and then wanted to add / update it with newer games, what you think the process would be?    
    
    
# appends multiple player summaries into a single dataframe   
def get_Players(FILES_LOC):
    df = pd.DataFrame()

    for fn in _find_files(FILES_LOC,'xml'):
        #loads each file and stores them in an list
        match = prg.Match(FILES_LOC + fn) 

        tmp_df = match.player_summary(norm='mins').reset_index()
        tmp_df['x_fixture_id'] = _generate_id(match.summary)

        #this is how we should have done this 
        #tmp_df['fixture_id'] = match.summary['fixture_id']

        df = pd.concat([df,tmp_df]) 
        
    return df 
    
#VINNY# Class!!! The x_fixture_ID is ideal for an easier to read version. Opta do have APIs etc but this seems properly accessible. Amazing!    
