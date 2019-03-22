"""
Author: James Londal
Copyright: Copyright 2019, Picopie Ltd
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal

Description:

Conversts SuperScout XML file into two dataframes. One containing the events of the match and the other is a summary of the match.
The main function is to_df

"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
from tempfile import NamedTemporaryFile
import tempfile


from pyrugga.lookup import events, descriptions

"""
Returns a dataframe with a summary of each players in the match

-- fixture_code
-- team_id
-- player_id
-- team_name
-- players_name
-- min (minutes on pitch)
-- shirt_no
-- position

"""
def get_players_fixture(f_in):
    tree = ET.parse(f_in)
    root = tree.getroot()

    for child in root:
        fixture_code = child.text

    fout = NamedTemporaryFile(mode='wt',delete=False)

    c = 0

    for a in tree.findall(".//Player"):
        out = ''
        if c == 0:
            out = 'fixture_code,'
            for i in a.keys():
                out +=  i + ","

            out = out[:-1] + '\n'

        out += str(fixture_code) + ','
        for i in a.keys():
            out +=  a.get(i) + ","

        out = out[:-1] + '\n'

        c += 1
        fout.write(out)

    fout.close()

    players = pd.read_csv(fout.name)
    os.remove(fout.name)


    players['players_name'] = players['PLFORN'] + ' ' + players['PLSURN']


    players = players.rename(columns={
            'Club' : 'team_id',
            'PLID' : 'player_id',
            'TEAMNAME' : 'team_name' ,
            'MINS' : 'min',
            'Metres' : 'metres' ,
            'PosID' : 'position',
            'ShirtNo' : 'shirt_no'
        })
    players = players[['fixture_code','team_id','player_id','team_name','players_name','min','shirt_no','position']]
    return players

"""
Returns a dataframe with all the events from a match

-- action_id
-- action_result
-- action_type
-- fixture_code
-- team_name
-- match_time
-- metres
-- phases
-- set_num
-- player_id
-- ps_id
"""
def get_fixture_actions(f_in):
    tree = ET.parse(f_in)
    root = tree.getroot()

    fout = NamedTemporaryFile(mode='wt',delete=False)

    c = 0

    for a in tree.findall(".//ActionRow"):
        out = ''
        if c == 0:
            for i in a.keys():
                out +=  i + ","

            out = out[:-1] + '\n'
        for i in a.keys():
            out +=  a.get(i) + ","

        out = out[:-1] + '\n'

        c += 1
        fout.write(out)

    fout.close()

    actions = pd.read_csv(fout.name)
    os.remove(fout.name)


    actions = actions.rename(columns={
        'ID' : 'action_id' ,
        'Actionresult' : 'action_result' ,
        'ActionType' : 'action_type',
        'FXID' : 'fixture_code' ,
        'TEAMNAME' : 'team_name' ,
        'MatchTime' : 'match_time',
        'Metres' : 'metres' ,
        'PlayNum' : 'phases' ,
        'SetNum' : 'set_num',
        'PLID' : 'player_id',
        'psID' : 'ps_id'
        })

    actions['action_type'] = pd.to_numeric(actions.action_type)
    actions['action_result'] = pd.to_numeric(actions.action_result)
    actions['qualifier3'] = pd.to_numeric(actions.qualifier3)
    actions['qualifier4'] = pd.to_numeric(actions.qualifier4)
    actions['qualifier5'] = pd.to_numeric(actions.qualifier5)

    return actions

"""
Returns a dataframe with summary of a match


-- fixture_code
-- ref_id
-- ref_name
-- fixture_date
-- fx_week
-- awayteam
-- hometeam

"""
def get_fixture(f_in):
    tree = ET.parse(f_in)
    root = tree.getroot()

    for child in root:
        fixture_code = child.text

    fout = NamedTemporaryFile(mode='wt',delete=False)

    c = 0

    for a in tree.findall(".//Data"):
        out = ''
        if c == 0:
            out = 'fixture_code,'
            for i in a.keys():
                out +=  i + ","

            out = out[:-1] + '\n'

        out += str(fixture_code) + ','
        for i in a.keys():
            out +=  a.get(i) + ","

        out = out[:-1] + '\n'

        c += 1

        fout.write(out)

    fout.close()


    match = pd.read_csv(fout.name)
    os.remove(fout.name)

    match = match.rename(columns={
        'REFID' : 'ref_id' ,
        'REFNAME' : 'ref_name' ,
        'FxWeek' : 'fx_week',
        'FxDate' : 'fixture_date'
        })

    match = match[['fixture_code','ref_id','ref_name','fixture_date','fx_week','awayteam','hometeam']]
    return match

"""
Returns the points scored from in an event
"""
def calc_score(row):
    score = 0
    if row['event'] == "Try":
        score = 5
        if row['event_type'] == 'Won Penalty Try':
            score += 2

    if row['event_type'] == "Conversion" and row['outcome'] == 'Goal Kicked':
        score = 2

    if row['event_type'] == "Penalty Goal" and row['outcome'] == 'Goal Kicked':
        score = 3

    if row['event_type'] == "Drop Goal" and row['outcome'] == 'Goal Kicked':
        score = 3

    return score


"""
Returns a dataframe with event by events details
"""
def to_df(super_scout_file_name):


    actions = get_fixture_actions(super_scout_file_name)
    players = get_players_fixture(super_scout_file_name)
    match = get_fixture(super_scout_file_name)

    actions_players = pd.merge(actions, players,  left_on = 'player_id', right_on = 'player_id')
    actions_players = pd.merge(actions_players, events,  left_on = 'action', right_on = 'action')
    actions_players = pd.merge(actions_players, descriptions, how='left', left_on = 'action_type', right_on = 'qualifier')
    actions_players = pd.merge(actions_players, descriptions, how='left', left_on = 'action_result', right_on = 'qualifier')
    actions_players = pd.merge(actions_players, descriptions, how='left', left_on = 'qualifier3', right_on = 'qualifier')
    actions_players = pd.merge(actions_players, descriptions, how='left', left_on = 'qualifier4', right_on = 'qualifier')
    actions_players = pd.merge(actions_players, descriptions, how='left', left_on = 'qualifier5', right_on = 'qualifier')


    actions_players = actions_players[[
       'fixture_code_x',
        'set_num',
       'action_id' ,
       'match_time',
       'ps_timestamp',
       'ps_endstamp',
       'advantage',
       'team_name',
       'players_name',
        'shirt_no',
        'position',
       'event',
       'qualifier_description_x',
       'qualifier_description_y',
       'x_coord',
       'y_coord',
       'x_coord_end',
       'y_coord_end',
        'metres',
        'phases' ,
        'period',
        'score_advantage'
    ]]

    actions_players.columns = [
       'fixture_code_x',
        'set_num',
       'action_id' ,
       'match_time',
       'ps_timestamp',
       'ps_endstamp',
       'advantage',
       'team_name',
       'players_name',
        'shirt_no',
        'position',
       'event',
       'event_type',
       'description',
       'outcome' ,
       'additional',
       'x_coord',
       'y_coord',
       'x_coord_end',
       'y_coord_end',
        'metres',
        'phases',
        'period',
        'home_team_advantage'
    ]

    actions_players.sort_values(by='action_id',inplace=True)

    actions_team = pd.merge(actions, players[['team_id','team_name']].drop_duplicates(), left_on = 'player_id', right_on = 'team_id')
    actions_team = pd.merge(actions_team, events,  left_on = 'action', right_on = 'action')

    actions_team = pd.merge(actions_team, descriptions, how='left', left_on = 'action_type', right_on = 'qualifier')
    actions_team = pd.merge(actions_team, descriptions, how='left', left_on = 'action_result', right_on = 'qualifier')
    actions_team = pd.merge(actions_team, descriptions, how='left', left_on = 'qualifier3', right_on = 'qualifier')
    actions_team = pd.merge(actions_team, descriptions, how='left', left_on = 'qualifier4', right_on = 'qualifier')
    actions_team = pd.merge(actions_team, descriptions, how='left', left_on = 'qualifier5', right_on = 'qualifier')

    actions_team = actions_team[[
       'fixture_code',
        'set_num',
       'action_id' ,
       'match_time',
       'ps_timestamp',
       'ps_endstamp',
       'advantage',
       'team_name',
       'event',
       'qualifier_description_x',
       'qualifier_description_y',
       'x_coord',
       'y_coord',
       'x_coord_end',
       'y_coord_end',
        'metres',
        'phases',
        'period',
        'score_advantage'

    ]]

    actions_team.columns = [
       'fixture_code',
       'set_num',
       'action_id' ,
       'match_time',
       'ps_timestamp',
       'ps_endstamp',
       'advantage',
       'team_name',
       'event',
       'event_type',
       'description',
       'outcome' ,
       'additional',
       'x_coord',
       'y_coord',
       'x_coord_end',
       'y_coord_end',
        'metres',
        'phases',
        'period',
        'home_team_advantage'
    ]

    actions_team.sort_values(by='action_id',inplace=True)

    match_events = pd.concat([actions_players,actions_team],sort=True).sort_values('action_id')

    del match_events['fixture_code_x']

    match_events['fixture_code'] = min(match_events.fixture_code)
    match_events['position'] = match_events['position'].fillna(0)

    match_events['shirt_no'] = match_events['shirt_no'].fillna(0)

    match_events['points'] = match_events.apply(calc_score, axis=1)

    match = pd.merge(match,match_events.groupby('team_name')\
            ['points'].sum().reset_index(),left_on='hometeam',right_on='team_name').\
            rename(columns={'points':'home_score'})

    match = pd.merge(match,match_events.groupby('team_name')\
            ['points'].sum().reset_index(),left_on='awayteam',right_on='team_name').\
            rename(columns={'points':'away_score'})

    del match['team_name_y']
    del match['team_name_x']

    return (match_events,match)
