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

class Match:

    events = None
    summary = None
    timeline = None

    """
    The default method for defining an region on the pitch.
    This function can be replaced using when calling the __init__
    """

    """
    Creates a Match object from a Superscout XML file
    """
    def __init__(self, fn_name, zones=None):
        (self.events,self.summary) = to_df(fn_name)
        self._genTimeLine()

        def _Zones( x ): return round( x / 10)

        if  zones == None:
            self._Zones = _Zones
        else :
            self._Zones = zones


    def getRef(self):
        return self.summary['ref_name'].values[0]

    def HomeWin(self):
        return (self.summary['home_score'] > self.summary['away_score'])[0]

    def Draw(self):
        return (self.summary['home_score'] == self.summary['away_score'])[0]

    def _genTimeLine(self):

        tmp_filename = str(uuid.uuid4())
        conn = sqlite3.connect(tmp_filename)

        engine = create_engine('sqlite:///%s' % (tmp_filename))

        self.summary.to_sql('match_summary',engine,if_exists='replace',index=False)
        self.events.to_sql('match_events',engine,if_exists='replace',index=False)

        # Generates a time of the match
        sql = """
        select
        t1.period,
        t1.set_num,
        t1.team_name,
        case when outcome = 'End Pen Con' then -1*t2.points else t2.points end as points,
        x_coord,
        x_coord_end,
        y_coord,
        y_coord_end,
        metres as meters_gained,
        ((x_coord - x_coord_end)*(x_coord - x_coord_end)) + ((y_coord - y_coord_end)*(y_coord - y_coord_end)) as dist_traveled,
        ps_timestamp as start,
        ps_endstamp - ps_timestamp as length,
        event_type as start_event,
        outcome as end_event,
        phases,
        --carry
        sum(carry) as carry,
        sum(collection) as collection,
        sum(other_carry) as other_carry,
        sum(kick_return) as kick_return,
        sum(one_out_drive) as one_out_drive,
        sum(defender_beaten) as defender_beaten,
        sum(defensive_catch) as defensive_catch,
        sum(defensive_loose_ball) as defensive_loose_ball,
        sum(attacking_loose_ball) as attacking_loose_ball,
        sum(support_carry) as support_carry,
        sum(pick_and_go) as pick_and_go,
        sum(stepped) as stepped,
        sum(dropped_ball_unforced) as dropped_ball_unforced,
        sum(initial_break) as initial_break,
        sum(restart_catch) as restart_catch,
        sum(restart_return) as restart_return,
        sum(supported_break) as supported_break,


        --kicks
        sum(kick) as kick,
        sum(goal_kick) as goal_kick,
        sum(box) as box,
        sum(territorial) as territorial,
        sum(bomb) as bomb,
        sum(touch_kick) as touch_kick,

        --lineouts
        sum(lineout) as lineout,
        sum(lineout_take) as lineout_take,
        sum(throw_middle) as throw_middle,
        sum(lineout_win_middle) as lineout_win_middle,
        sum(lineout_win_front) as lineout_win_front,

        --rucks & mauls
        sum(case when t1.team_name = t3.team_name then maul else 0 end) as maul,
        sum(ruck) as ruck,

        --passes
        sum(pass) as pass,
        sum(complete_pass) as complete_pass,
        sum(offload) as offload,
        sum(scrum_half_pass) as scrum_half_pass,
        sum(break_pass) as break_pass,
        sum(incomplete_pass) as incomplete_pass,

        --penalty
        sum(case when t1.team_name = t3.team_name then penalty_conceded else 0 end) as penalty_conceded,
        sum(case when t1.team_name <> t3.team_name then penalty_conceded else 0 end) as penalty_won,

        --scrum
        sum(scrum) as scrum,
        sum(defensive_scrum) as defensive_scrum,
        sum(offensive_scrum) as offensive_scrum,
        sum(no_8_pick_up) as no_8_pick_up,
        sum(no_8_pass) as no_8_pass,

        --tackles
        sum(tackle) as tackle,
        sum(missed_tackle) as missed_tackle,
        sum(line_tackle) as line_tackle,
        sum(chase_tackle) as chase_tackle,
        sum(other_tackle) as other_tackle,
        sum(cover_tackle) as cover_tackle,
        sum(guard_tackle) as guard_tackle,
        sum(bumped_off) as bumped_off,

        --turnovers
        sum(jackal) as jackal,
        sum(turnover_won) as turnover_won,


        sum(try) as try,
        sum(conversion) as conversion,

        sum(t3.advantage) as advantage,


        sum(low) as low,
        sum(tap_back) as tap_back,
        sum(edge_tackle) as edge_tackle,
        sum(positional) as positional,
        sum(throw_front) as throw_front,
        sum(attacking_catch) as attacking_catch,
        sum(carried_in_touch) as carried_in_touch,
        sum(penalty_kick) as penalty_kick,
        sum(scrum_half_kick) as scrum_half_kick,
        sum(start_set_lineout_steal) as start_set_lineout_steal,

        sum(tap_pen) as tap_pen,
        sum(lost_ball_forced) as lost_ball_forced,
        sum(lost_in_ruck_or_maul) as lost_in_ruck_or_maul,

        sum(restart_22m) as restart_22m,
        sum(cross_pitch) as cross_pitch,
        sum(in_goal_touchdown) as in_goal_touchdown,
        sum(lineout_steal_front) as lineout_steal_front,
        sum(penalty_goal) as penalty_goal,
        sum(try_pass) as try_pass,
        sum(chip) as chip,
        sum(free_kick) as free_kick,
        sum(interception) as interception,
        sum(lineout_win_15m_plus) as lineout_win_15m_plus,
        sum(lineout_win_quick) as lineout_win_quick,
        sum(not_releasing) as not_releasing,
        sum(obstruction) as obstruction,
        sum(start_period) as start_period,
        sum(throw_15m_plus) as throw_15m_plus,
        sum(throw_back) as throw_back,
        sum(throw_quick) as throw_quick,
        sum(accidental_offside) as accidental_offside,
        sum(bad_pass) as bad_pass,
        sum(charge_down) as charge_down,
        sum(failure_to_find_touch) as failure_to_find_touch,
        sum(forward_pass) as forward_pass,
        sum(foul_play_high_tackle) as foul_play_high_tackle,
        sum(foul_play_other) as foul_play_other,
        sum(foul_play) as foul_play,
        sum(hands_in_ruck) as hands_in_ruck,
        sum(intercepted_pass) as intercepted_pass,
        sum(kick_error) as kick_error,
        sum(lineout_steal_middle) as lineout_steal_middle,
        sum(lineout_win_back) as lineout_win_back,
        sum(mark) as mark,
        sum(not_rolling_away) as not_rolling_away,
        sum(offside_at_kick) as offside_at_kick,
        sum(outpaced) as outpaced,
        sum(scrum_offence) as scrum_offence,
        sum(video_ref_awarded) as video_ref_awarded,
        sum(won_penalty_try) as won_penalty_try,
        sum(yellow_card) as yellow_card,
        sum(red_card) as red_card,
        sum(clean_break) as clean_break,
        sum(collected_bounce) as collected_bounce,
        sum(end_set_kick_error) as end_set_kick_error,
        sum(error) as error,
        sum(error_out_of_play) as error_out_of_play,
        sum(error_terratorial_loss) as error_terratorial_loss,
        sum(forced_in_touch) as forced_in_touch,
        sum(goal_kicked) as goal_kicked,
        sum(goal_missed) as goal_missed,
        sum(in_goal) as in_goal,
        sum(ineffective) as ineffective,
        sum(kick_in_touch_bounce) as kick_in_touch_bounce,
        sum(lost_overthrown) as lost_overthrown,
        sum(off_load) as off_load,
        sum(pen_conceded) as pen_conceded,
        sum(penalty_try) as penalty_try,
        sum(penalty_won) as penalty_won,
        sum(pressure_error) as pressure_error,
        sum(pressure_in_touch) as pressure_in_touch,
        sum(reset) as reset,
        sum(sack) as sack,
        sum(tackled_dominant) as tackled_dominant,
        sum(tackled_ineffective) as tackled_ineffective,
        sum(tackled_neutral) as tackled_neutral,
        sum(to_ground) as to_ground,
        sum(loose_head_offensive) as loose_head_offensive,
        sum(hooker_offensive) as hooker_offensive,
        sum(tight_head_offensive) as tight_head_offensive,
        sum(lock_4_offensive) as lock_4_offensive,
        sum(lock_5_offensive) as lock_5_offensive,
        sum(flanker_6_offensive) as flanker_6_offensive,
        sum(flanker_7_offensive) as flanker_7_offensive,
        sum(number_8_offensive) as number_8_offensive,
        sum(scrum_half_offensive) as scrum_half_offensive,
        sum(fly_half_offensive) as fly_half_offensive,
        sum(left_wing_offensive) as left_wing_offensive,
        sum(inside_centre_offensive) as inside_centre_offensive,
        sum(outside_centre_offensive) as outside_centre_offensive,
        sum(right_wing_offensive) as right_wing_offensive,
        sum(full_back_offensive) as full_back_offensive,
        sum(loose_head_defensive) as loose_head_defensive,
        sum(hooker_defensive) as hooker_defensive,
        sum(tight_head_defensive) as tight_head_defensive,
        sum(lock_4_defensive) as lock_4_defensive,
        sum(lock_5_defensive) as lock_5_defensive,
        sum(flanker_6_defensive) as flanker_6_defensive,
        sum(flanker_7_defensive) as flanker_7_defensive,
        sum(number_8_defensive) as number_8_defensive,
        sum(scrum_half_defensive) as scrum_half_defensive,
        sum(fly_half_defensive) as fly_half_defensive,
        sum(left_wing_defensive) as left_wing_defensive,
        sum(inside_centre_defensive) as inside_centre_defensive,
        sum(outside_centre_defensive) as outside_centre_defensive,
        sum(right_wing_defensive) as right_wing_defensive,
        sum(full_back_defensive) as full_back_defensive

        from
        match_events t1 left join
        (
        select
        period,
        set_num,
        sum(points) as points
        from
        match_events
        group by
        period,
        set_num
        ) t2 on (t1.period = t2.period and t1.set_num = t2.set_num) left join
        (
        select
        period,
        set_num,
        team_name,
        --events
        sum(case when event = 'Carry' then 1 else 0 end) as carry,
        sum(case when event = 'Collection' then 1 else 0 end) as collection,
        sum(case when event = 'Defensive Scrum' then 1 else 0 end) as defensive_scrum,
        sum(case when event = 'Goal Kick' then 1 else 0 end) as goal_kick,
        sum(case when event = 'Kick' then 1 else 0 end) as kick,
        sum(case when event = 'Lineout Take' then 1 else 0 end) as lineout_take,
        sum(case when event = 'Lineout Throw' then 1 else 0 end) as lineout_throw,
        sum(case when event = 'Maul' then 1 else 0 end) as maul,
        sum(case when event = 'Missed Tackle' then 1 else 0 end) as missed_tackle,
        sum(case when event = 'Offensive Scrum' then 1 else 0 end) as offensive_scrum,
        sum(case when event = 'Pass' then 1 else 0 end) as pass,
        sum(case when event = 'Penalty Conceded' then 1 else 0 end) as penalty_conceded,
        sum(case when event = 'Restart' then 1 else 0 end) as restart,
        sum(case when event = 'Ruck' then 1 else 0 end) as ruck,
        sum(case when event = 'Scrum' then 1 else 0 end) as scrum,
        sum(case when event = 'Tackle' then 1 else 0 end) as tackle,
        sum(case when event = 'Try' then 1 else 0 end) as try,
        sum(case when event = 'Turnover' then 1 else 0 end) as turnover,

        --event_types
        sum(case when event_type = 'Complete Pass' then 1 else 0 end) as complete_pass,
        sum(case when event_type = 'Line Tackle' then 1 else 0 end) as line_tackle,
        sum(case when event_type = 'Other Carry' then 1 else 0 end) as other_carry,
        sum(case when event_type = 'Kick Return' then 1 else 0 end) as kick_return,
        sum(case when event_type = 'One Out Drive' then 1 else 0 end) as one_out_drive,
        sum(case when event_type = 'Chase Tackle' then 1 else 0 end) as chase_tackle,
        sum(case when event_type = 'Defender Beaten' then 1 else 0 end) as defender_beaten,
        sum(case when event_type = 'Lineout' then 1 else 0 end) as lineout,
        sum(case when event_type = 'Defensive Catch' then 1 else 0 end) as defensive_catch,
        sum(case when event_type = 'Defensive Loose Ball' then 1 else 0 end) as defensive_loose_ball,
        sum(case when event_type = 'Other Tackle' then 1 else 0 end) as other_tackle,
        sum(case when event_type = 'Attacking Loose Ball' then 1 else 0 end) as attacking_loose_ball,
        sum(case when event_type = 'Box' then 1 else 0 end) as box,
        sum(case when event_type = 'Cover Tackle' then 1 else 0 end) as cover_tackle,
        sum(case when event_type = 'Offload' then 1 else 0 end) as offload,
        sum(case when event_type = 'Support Carry' then 1 else 0 end) as support_carry,
        sum(case when event_type = 'Pick And Go' then 1 else 0 end) as pick_and_go,
        sum(case when event_type = 'Scrum Half Pass' then 1 else 0 end) as scrum_half_pass,
        sum(case when event_type = 'Dropped Ball Unforced' then 1 else 0 end) as dropped_ball_unforced,
        sum(case when event_type = 'Stepped' then 1 else 0 end) as stepped,
        sum(case when event_type = 'Advantage' then 1 else 0 end) as advantage,
        sum(case when event_type = 'Territorial' then 1 else 0 end) as territorial,
        sum(case when event_type = 'Initial Break' then 1 else 0 end) as initial_break,
        sum(case when event_type = 'No 8 Pick Up' then 1 else 0 end) as no_8_pick_up,
        sum(case when event_type = 'Guard Tackle' then 1 else 0 end) as guard_tackle,
        sum(case when event_type = 'Bumped Off' then 1 else 0 end) as bumped_off,
        sum(case when event_type = 'Break Pass' then 1 else 0 end) as break_pass,
        sum(case when event_type = 'Jackal' then 1 else 0 end) as jackal,
        sum(case when event_type = 'Incomplete Pass' then 1 else 0 end) as incomplete_pass,
        sum(case when event_type = 'Low' then 1 else 0 end) as low,
        sum(case when event_type = 'Restart Catch' then 1 else 0 end) as restart_catch,
        sum(case when event_type = 'Turnover Won' then 1 else 0 end) as turnover_won,
        sum(case when event_type = 'Throw Middle' then 1 else 0 end) as throw_middle,
        sum(case when event_type = 'Bomb' then 1 else 0 end) as bomb,
        sum(case when event_type = 'Lineout Win Middle' then 1 else 0 end) as lineout_win_middle,
        sum(case when event_type = 'No 8 Pass' then 1 else 0 end) as no_8_pass,
        sum(case when event_type = 'Restart Return' then 1 else 0 end) as restart_return,
        sum(case when event_type = 'Supported Break' then 1 else 0 end) as supported_break,
        sum(case when event_type = 'Tap Back' then 1 else 0 end) as tap_back,
        sum(case when event_type = 'Touch Kick' then 1 else 0 end) as touch_kick,
        sum(case when event_type = 'Edge Tackle' then 1 else 0 end) as edge_tackle,
        sum(case when event_type = 'Positional' then 1 else 0 end) as positional,
        sum(case when event_type = 'Throw Front' then 1 else 0 end) as throw_front,
        sum(case when event_type = 'Attacking Catch' then 1 else 0 end) as attacking_catch,
        sum(case when event_type = 'Conversion' then 1 else 0 end) as conversion,
        sum(case when event_type = 'Carried In Touch' then 1 else 0 end) as carried_in_touch,
        sum(case when event_type = 'Penalty Kick' then 1 else 0 end) as penalty_kick,
        sum(case when event_type = 'Scrum Half Kick' then 1 else 0 end) as scrum_half_kick,
        sum(case when event_type = 'Start Set Lineout Steal' then 1 else 0 end) as start_set_lineout_steal,
        sum(case when event_type = 'Tap Pen' then 1 else 0 end) as tap_pen,
        sum(case when event_type = 'Lineout Win Front' then 1 else 0 end) as lineout_win_front,
        sum(case when event_type = 'Lost Ball Forced' then 1 else 0 end) as lost_ball_forced,
        sum(case when event_type = 'Lost In Ruck Or Maul' then 1 else 0 end) as lost_in_ruck_or_maul,
        sum(case when event_type = '22m Restart' then 1 else 0 end) as restart_22m,
        sum(case when event_type = 'Cross Pitch' then 1 else 0 end) as cross_pitch,
        sum(case when event_type = 'In Goal Touchdown' then 1 else 0 end) as in_goal_touchdown,
        sum(case when event_type = 'Lineout Steal Front' then 1 else 0 end) as lineout_steal_front,
        sum(case when event_type = 'Penalty Goal' then 1 else 0 end) as penalty_goal,
        sum(case when event_type = 'Try Pass' then 1 else 0 end) as try_pass,
        sum(case when event_type = 'Chip' then 1 else 0 end) as chip,
        sum(case when event_type = 'Free Kick' then 1 else 0 end) as free_kick,
        sum(case when event_type = 'Interception' then 1 else 0 end) as interception,
        sum(case when event_type = 'Lineout Win 15m+' then 1 else 0 end) as lineout_win_15m_plus,
        sum(case when event_type = 'Lineout Win Quick' then 1 else 0 end) as lineout_win_quick,
        sum(case when event_type = 'Not Releasing' then 1 else 0 end) as not_releasing,
        sum(case when event_type = 'Obstruction' then 1 else 0 end) as obstruction,
        sum(case when event_type = 'Start Period' then 1 else 0 end) as start_period,
        sum(case when event_type = 'Throw 15m+' then 1 else 0 end) as throw_15m_plus,
        sum(case when event_type = 'Throw Back' then 1 else 0 end) as throw_back,
        sum(case when event_type = 'Throw Quick' then 1 else 0 end) as throw_quick,
        sum(case when event_type = 'Accidental Offside' then 1 else 0 end) as accidental_offside,
        sum(case when event_type = 'Bad Pass' then 1 else 0 end) as bad_pass,
        sum(case when event_type = 'Charge Down' then 1 else 0 end) as charge_down,
        sum(case when event_type = 'Failure To Find Touch' then 1 else 0 end) as failure_to_find_touch,
        sum(case when event_type = 'Forward Pass' then 1 else 0 end) as forward_pass,
        sum(case when event_type = 'Foul Play - High Tackle' then 1 else 0 end) as foul_play_high_tackle,
        sum(case when event_type = 'Foul Play - Other' then 1 else 0 end) as foul_play_other,
        sum(case when event_type = 'Foul Play?' then 1 else 0 end) as foul_play,
        sum(case when event_type = 'Hands In Ruck' then 1 else 0 end) as hands_in_ruck,
        sum(case when event_type = 'Intercepted Pass' then 1 else 0 end) as intercepted_pass,
        sum(case when event_type = 'Kick Error' then 1 else 0 end) as kick_error,
        sum(case when event_type = 'Lineout Steal Middle' then 1 else 0 end) as lineout_steal_middle,
        sum(case when event_type = 'Lineout Win Back' then 1 else 0 end) as lineout_win_back,
        sum(case when event_type = 'Mark' then 1 else 0 end) as mark,
        sum(case when event_type = 'Not Rolling Away' then 1 else 0 end) as not_rolling_away,
        sum(case when event_type = 'Offside At Kick' then 1 else 0 end) as offside_at_kick,
        sum(case when event_type = 'Outpaced' then 1 else 0 end) as outpaced,
        sum(case when event_type = 'Scrum Offence' then 1 else 0 end) as scrum_offence,
        sum(case when event_type = 'Video Ref Awarded' then 1 else 0 end) as video_ref_awarded,
        sum(case when event_type = 'Won Penalty Try' then 1 else 0 end) as won_penalty_try,
        sum(case when event_type = 'Yellow' then 1 else 0 end) as yellow_card,
        sum(case when event_type = 'Red' then 1 else 0 end) as red_card,

        --outcomes
        sum(case when event = 'Clean Break' then 1 else 0 end) as clean_break,
        sum(case when event = 'Collected Bounce' then 1 else 0 end) as collected_bounce,
        sum(case when event = 'End Set Kick Error' then 1 else 0 end) as end_set_kick_error,
        sum(case when event = 'Error' then 1 else 0 end) as error,
        sum(case when event = 'Error - Out Of Play' then 1 else 0 end) as error_out_of_play,
        sum(case when event = 'Error - Terratorial Loss' then 1 else 0 end) as error_terratorial_loss,
        sum(case when event = 'Forced In Touch' then 1 else 0 end) as forced_in_touch,
        sum(case when event = 'Goal Kicked' then 1 else 0 end) as goal_kicked,
        sum(case when event = 'Goal Missed' then 1 else 0 end) as goal_missed,
        sum(case when event = 'In Goal' then 1 else 0 end) as in_goal,
        sum(case when event = 'Ineffective' then 1 else 0 end) as ineffective,
        sum(case when event = 'Kick In Touch (Bounce)' then 1 else 0 end) as kick_in_touch_bounce,
        sum(case when event = 'Lost Overthrown' then 1 else 0 end) as lost_overthrown,
        sum(case when event = 'Off Load' then 1 else 0 end) as off_load,
        sum(case when event = 'Pen Conceded' then 1 else 0 end) as pen_conceded,
        sum(case when event = 'Penalty Try' then 1 else 0 end) as penalty_try,
        sum(case when event = 'Penalty Won' then 1 else 0 end) as penalty_won,
        sum(case when event = 'Pressure Error' then 1 else 0 end) as pressure_error,
        sum(case when event = 'Pressure In Touch' then 1 else 0 end) as pressure_in_touch,
        sum(case when event = 'Reset' then 1 else 0 end) as reset,
        sum(case when event = 'Sack' then 1 else 0 end) as sack,
        sum(case when event = 'Tackled Dominant' then 1 else 0 end) as tackled_dominant,
        sum(case when event = 'Tackled Ineffective' then 1 else 0 end) as tackled_ineffective,
        sum(case when event = 'Tackled Neutral' then 1 else 0 end) as tackled_neutral,
        sum(case when event = 'To Ground' then 1 else 0 end) as to_ground,


        -- player interactions
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '1' then 1 else 0 end) as loose_head_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '2' then 1 else 0 end) as hooker_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '3' then 1 else 0 end) as tight_head_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '4' then 1 else 0 end) as lock_4_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '5' then 1 else 0 end) as lock_5_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '6' then 1 else 0 end) as flanker_6_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '7' then 1 else 0 end) as flanker_7_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '8' then 1 else 0 end) as number_8_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '9' then 1 else 0 end) as scrum_half_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '10' then 1 else 0 end) as fly_half_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '11' then 1 else 0 end) as left_wing_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '12' then 1 else 0 end) as inside_centre_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '13' then 1 else 0 end) as outside_centre_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '14' then 1 else 0 end) as right_wing_offensive,
        sum(case when event in ('Collection','Carry','Kick','Lineout Take','Lineout Throw','Pass','Try') and position = '15' then 1 else 0 end) as full_back_offensive,

        sum(case when event in ('Tackle','Turnover') and position = '1' then 1 else 0 end) as loose_head_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '2' then 1 else 0 end) as hooker_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '3' then 1 else 0 end) as tight_head_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '4' then 1 else 0 end) as lock_4_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '5' then 1 else 0 end) as lock_5_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '6' then 1 else 0 end) as flanker_6_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '7' then 1 else 0 end) as flanker_7_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '8' then 1 else 0 end) as number_8_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '9' then 1 else 0 end) as scrum_half_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '10' then 1 else 0 end) as fly_half_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '11' then 1 else 0 end) as left_wing_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '12' then 1 else 0 end) as inside_centre_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '13' then 1 else 0 end) as outside_centre_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '14' then 1 else 0 end) as right_wing_defensive,
        sum(case when event in ('Tackle','Turnover') and position = '15' then 1 else 0 end) as full_back_defensive

        from
        match_events
        group by
        period,
        set_num,
        team_name
        ) t3 on (t1.period = t3.period and t1.set_num = t3.set_num)

        where
        event = 'Possession'

        group by
        1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        order by
        1,2

        """

        os.remove(tmp_filename)

        timeline = pd.io.sql.read_sql(sql,conn)

        tmp = self.events.groupby(['team_name','set_num'])['points'].sum().reset_index()
        tmp = pd.pivot_table(tmp, values='points', index=['set_num'],columns=['team_name'], aggfunc=np.sum).cumsum()

        timeline = pd.merge(timeline,tmp,how='left',left_on='set_num',right_on='set_num').interpolate(method='linear')

        timeline['dist_traveled'] = np.sqrt(timeline['dist_traveled'])

        timeline[timeline.columns[-2:-1][0] + "_points"] = np.array((timeline.iloc[:,-2:-1] - timeline.iloc[:,-2:-1].shift(1)).fillna(0)).ravel()
        timeline[timeline.columns[-2:-1][0] + "_points"] = np.array((timeline.iloc[:,-2:-1] - timeline.iloc[:,-2:-1].shift(1)).fillna(0)).ravel()
        self.timeline = timeline

    def getTerritoryX(self,perc=False):
        pos = self.events.groupby(['team_name','x_coord']).count()['action_id'].reset_index()

        pos['x_coord'] = pos['x_coord'].apply(self._Zones)
        df2 = pd.pivot_table(pos, values='action_id', index=['x_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('x_coord > 0 and x_coord < 11' )/df2.query('x_coord > 0 and x_coord < 11' ).sum()

        return df2.query('x_coord > 0 and x_coord < 11')

    def getTerritoryY(self,perc=False):
        pos = self.events.groupby(['team_name','y_coord']).count()['action_id'].reset_index()

        pos['y_coord'] = pos['y_coord'].apply(self._Zones)
        df2 = pd.pivot_table(pos, values='action_id', index=['y_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('y_coord > 0 and y_coord < 11' )/df2.query('y_coord > 0 and y_coord < 11' ).sum()

        return df2.query('y_coord > 0 and y_coord < 11')

    def getTerritory(self, perc=False):
        pos = self.events.groupby(['team_name','x_coord','y_coord']).count()['action_id'].reset_index()

        pos['y_coord'] = pos['y_coord'].apply(self._Zones)
        pos['x_coord'] = pos['x_coord'].apply(self._Zones)

        df2 = pd.pivot_table(pos, values='action_id', index=['y_coord','x_coord'],columns=['team_name'], aggfunc=np.sum, fill_value=0)

        if perc == True:
            return df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11' )/df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11' ).sum()

        return df2.query('y_coord > 0 and y_coord < 11 and x_coord > 0 and x_coord < 11')
