"""
Author: James Londal
Copyright: Copyright 2019, Picopie Ltd
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal
"""

#converts SuperScout file to DataFrame
from pyrugga.parse_xml import to_df

import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import uuid
import matplotlib.pyplot as plt
import seaborn as sns
import pkgutil
import sys

class Match:

    events = None
    summary = None
    timeline = None
    players = None

    hometeam = None
    awayteam = None


    def __init__(self, fn_name, zones=None):
        """
        Creates a Match object from a Superscout XML file
        """
        (self.events,self.summary,self.players) = to_df(fn_name)
        self._genTimeLine()

        """
        The default method for defining an region on the pitch.
        This function can be replaced using when calling the __init__
        """
        def _Zones( x ): return round( x / 10)

        if  zones == None:
            self._Zones = _Zones
        else :
            self._Zones = zones

        self.hometeam = self.summary['hometeam'].values[0]
        self.awayteam = self.summary['awayteam'].values[0]

        self.homewin = (self.summary['home_score'] > self.summary['away_score'])[0]

        self.ref_name = self.summary['ref_name'].values[0]

        self.draw = (self.summary['home_score'] == self.summary['away_score'])[0]

    def _genTimeLine(self):
        """
        generates a timeline of match
        """

        tmp_filename = str(uuid.uuid4())
        conn = sqlite3.connect(tmp_filename)

        engine = create_engine('sqlite:///%s' % (tmp_filename))

        self.summary.to_sql('match_summary',engine,if_exists='replace',index=False)
        self.events.to_sql('match_events',engine,if_exists='replace',index=False)

        d = os.path.dirname(sys.modules['pyrugga'].__file__)
        sql = open(os.path.join(d, 'timeline.sql'), 'r').read()

        os.remove(tmp_filename)

        timeline = pd.io.sql.read_sql(sql,conn)

        tmp = self.events.groupby(['team_name','set_num'])['points'].sum().reset_index()
        tmp = pd.pivot_table(tmp, values='points', index=['set_num'],columns=['team_name'], aggfunc=np.sum).cumsum()

        timeline = pd.merge(timeline,tmp,how='left',left_on='set_num',right_on='set_num').interpolate(method='linear')

        timeline['dist_traveled'] = np.sqrt(timeline['dist_traveled'])

        timeline[timeline.columns[-2:-1][0] + "_points"] = np.array((timeline.iloc[:,-2:-1] - timeline.iloc[:,-2:-1].shift(1)).fillna(0)).ravel()
        timeline[timeline.columns[-2:-1][0] + "_points"] = np.array((timeline.iloc[:,-2:-1] - timeline.iloc[:,-2:-1].shift(1)).fillna(0)).ravel()
        self.timeline = timeline


    def getTerritoryX(self,perc=False, event=None, event_type=None, description=None):
        """
        Gets the activities by zone length
        """

        tmp = self.events

        if event is not None :
            tmp = self.events.query('event == "%s"' % (event))

        if event_type is not None :
            tmp = self.events.query('event_type == "%s"' % (event_type))

        if description is not None :
            tmp = self.events.query('description == "%s"' % (description))

        pos = tmp.groupby(['team_name','x_coord']).count()['action_id'].reset_index()

        pos['x_coord'] = pos['x_coord'].apply(self._Zones)
        df2 = pd.pivot_table(pos, values='action_id', index=['x_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('x_coord > 0 and x_coord < 11' )/df2.query('x_coord > 0 and x_coord < 11' ).sum()

        return df2.query('x_coord > 0 and x_coord < 11')


    def getTerritoryY(self,perc=False, event=None, event_type=None, description=None):
        """
        Gets the activities by zone breadth
        """
        tmp = self.events

        if event is not None :
            tmp = self.events.query('event == "%s"' % (event))

        if event_type is not None :
            tmp = self.events.query('event_type == "%s"' % (event_type))

        if description is not None :
            tmp = self.events.query('description == "%s"' % (description))

        pos = tmp.groupby(['team_name','y_coord']).count()['action_id'].reset_index()

        pos['y_coord'] = pos['y_coord'].apply(self._Zones)
        df2 = pd.pivot_table(pos, values='action_id', index=['y_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('y_coord > 0 and y_coord < 11' )/df2.query('y_coord > 0 and y_coord < 11' ).sum()

        return df2.query('y_coord > 0 and y_coord < 11')


    def getTerritory(self,perc=False, event=None, event_type=None, description=None):
        """
        Gets the activities by zone breadth
        """
        tmp = self.events

        if event is not None :
            tmp = self.events.query('event == "%s"' % (event))

        if event_type is not None :
            tmp = self.events.query('event_type == "%s"' % (event_type))

        if description is not None :
            tmp = self.events.query('description == "%s"' % (description))

        pos = tmp.groupby(['team_name','x_coord','y_coord']).count()['action_id'].reset_index()


        pos['y_coord'] = pos['y_coord'].apply(self._Zones)
        pos['x_coord'] = pos['x_coord'].apply(self._Zones)

        df2 = pd.pivot_table(pos, values='action_id', index=['y_coord','x_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11' )/df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11' ).sum()

        return df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11')


    def getTerritoryMetric(self, event=None, event_type=None, description=None):
        """
        Returns the territory metric
        """
        return pd.DataFrame((self.getTerritoryX(perc=False, event=event, event_type=event_type, description=description) / self.getTerritoryX(perc=False,event=event, event_type=event_type, description=description).sum().sum()).sum()).reset_index().rename(columns={ 0 : 'territory'})


    def heat_map(self, event=None, event_type=None, description=None):
        """
        Draws a heatmap of where the type of events took place

        inputs

            event=
            event_type=
            description=

        outputs

         two heat maps one for each team

        """
        fig = plt.figure(figsize=(20,6))


        fig.suptitle('%s vs. %s ' % (self.hometeam, self.awayteam),fontsize="x-large")

        ax  = plt.subplot(1, 2, 2)
        plt.title(self.hometeam)

        hmap = self.getTerritory(perc=False,event=event, event_type=event_type, description=description).reset_index()\
        .pivot("y_coord","x_coord",self.hometeam).fillna(0).astype(int)

        sns.heatmap(hmap, annot=True, fmt="d", linewidths=.5,ax=ax,cmap="Greens")

        ax  = plt.subplot(1, 2, 1)
        plt.title(self.awayteam)

        hmap = self.getTerritory(perc=False,event=event, event_type=event_type, description=description).reset_index()\
        .pivot("y_coord","x_coord",self.awayteam).fillna(0).astype(int)

        # Draw a heatmap with the numeric values in each cell
        sns.heatmap(hmap, annot=True, fmt="d", linewidths=.5,ax=ax,cmap="Greens")

        plt.show()


    def player_summary(self,norm=None):
        """
        Summary for each player in a team along with option to normalise metrics by
        minutes played, actions involved in or phases
        norm = ['min','actions','phases']
        """

        tmp_filename = str(uuid.uuid4())
        conn = sqlite3.connect(tmp_filename)

        engine = create_engine('sqlite:///%s' % (tmp_filename))

        self.events.to_sql('match_events',engine,if_exists='replace',index=False)
        self.players.to_sql('players',engine,if_exists='replace',index=False)

        d = os.path.dirname(sys.modules['pyrugga'].__file__)
        sql = open(os.path.join(d, 'player_summary.sql'), 'r').read()

        player_summary = pd.io.sql.read_sql(sql,conn)

        os.remove(tmp_filename)

        player_summary['dist_traveled'] = np.sqrt(player_summary['dist_traveled'])

        player_summary = player_summary.set_index(['team_name', 'position', 'players_name'])


        if norm == 'min':
            player_summary.iloc[:,3:] = player_summary.iloc[:,7:].div(player_summary['mins'], axis=0)
        elif norm == 'actions':
            player_summary.iloc[:,3:] = player_summary.iloc[:,7:].div(player_summary['actions'], axis=0)
        elif norm == 'phases':
            player_summary.iloc[:,3:] = player_summary.iloc[:,7:].div(player_summary['phases'], axis=0)

        return player_summary
