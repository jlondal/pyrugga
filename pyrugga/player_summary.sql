select
t1.team_name, t1.position, t1.players_name,
case when t1.shirt_no > 15 then 1 else 0 end as replacement,
case when t1.shirt_no < 15 and t2.min < 80 then 1 else 0 end as replaced,
t2.min as mins,

count(distinct action_id) as actions,
avg(phases) as average_phase,
sum(phases) as phases,
sum(points) as points_scored,
sum(metres) as meters_gained,
((x_coord - x_coord_end)*(x_coord - x_coord_end)) + ((y_coord - y_coord_end)*(y_coord - y_coord_end)) as dist_traveled,

-- carry profile
sum(case when event = 'Carry' then 1.0 else 0.0 end ) as carry,
sum(case
   when event = 'Carry' and
   description in ('Crossed Gainline','Failed Gainline','Neutral')
   then 1.0 else 0.0 end ) as gainline_attempts,
sum(case when description = 'Crossed Gainline' then 1.0 else 0.0 end ) as crossed_gainline,
sum(case when event_type = 'One Out Drive' then 1.0 else 0.0 end ) as one_out_drive,
sum(case when event_type = 'One Out Drive' and description = 'Crossed Gainline'  then 1.0 else 0.0 end ) as one_out_drive_crossed_gainline,
sum(case when event_type = 'Support Carry' and description = 'Crossed Gainline' then 1.0 else 0.0 end ) as support_carry_crossed_gainline,
sum(case when event_type = 'Support Carry'  then 1.0 else 0.0 end ) as support_carry,
sum(case when event_type = 'Pick And Go' and description = 'Crossed Gainline' then 1.0 else 0.0 end ) as pick_and_go_crossed_gainline,
sum(case when event_type = 'Restart Return' then 1.0 else 0.0 end ) as retstart_return,
sum(case when event_type = 'Kick Return' then 1.0 else 0.0 end ) as kick_return,
sum(case when event_type = 'Restart Return' then 1.0 else 0.0 end ) as restart_return,
sum(case when event_type = 'Initial Break' then 1.0 else 0.0 end ) as initial_break,
sum(case when event_type = 'Supported Break' then 1.0 else 0.0 end ) as supported_break,
sum(case when event_type = 'Defender Beaten' then 1.0 else 0.0 end ) as defender_beaten,

-- kick profile
sum(case when event = 'Kick' then 1.0 else 0.0 end ) as kick,
sum(case when event_type = 'Kick In Play' then 1.0 else 0.0 end ) as kick_in_play,
sum(case when event_type = 'Kick In Own 22' then 1.0 else 0.0 end ) as kick_in_own_22,
sum(case when event_type = 'Bomb' then 1.0 else 0.0 end ) as bomb,
sum(case when event_type = 'Chip' then 1.0 else 0.0 end ) as chip,
sum(case when event_type = 'Cross Pitch' then 1.0 else 0.0 end ) as cross_pitch,
sum(case when event_type = 'Territorial' then 1.0 else 0.0 end ) as territorial,
sum(case when event_type = 'Kick In Touch (Bounce)' then 1.0 else 0.0 end ) as kick_in_touch_bounce,
sum(case when event_type = 'Kick In Touch (Full)' then 1.0 else 0.0 end ) as kick_in_touch_full,

-- pass profile
sum(case when event = 'Pass' then 1.0 else 0.0 end ) as pass,
sum(case when event_type = 'Off Load' then 1.0 else 0.0 end ) as off_load,
sum(case when event_type = 'Lateral Offload' then 1.0 else 0.0 end ) as lateral_offload,
sum(case when event_type = 'Backward Offload' then 1.0 else 0.0 end ) as backward_offload,
sum(case when event_type = 'Forward Pass' then 1.0 else 0.0 end ) as forward_pass,
sum(case when event_type = 'Incomplete Pass' then 1.0 else 0.0 end ) as incomplete_pass,
sum(case when event_type = 'Intercepted Pass' then 1.0 else 0.0 end ) as intercepted_pass,
sum(case when event_type = 'Key Pass' then 1.0 else 0.0 end ) as key_pass,
sum(case when event_type = 'Off Target Pass' then 1.0 else 0.0 end ) as off_target_pass,
sum(case when event_type = 'Try Pass' then 1.0 else 0.0 end ) as try_pass,
sum(case when event_type = 'Pass Error' then 1.0 else 0.0 end ) as pass_error,
sum(case when event_type = 'Right Pass' then 1.0 else 0.0 end ) as right_pass,
sum(case when event_type = 'Left Pass' then 1.0 else 0.0 end ) as left_pass,
sum(case when event_type = 'Long Pass' then 1.0 else 0.0 end ) as long_pass,
sum(case when event_type = 'Short Pass' then 1.0 else 0.0 end ) as short_pass,

-- tackle profile

sum(case when event = 'Tackle' then 1.0 else 0.0 end ) as tackle,
sum(case when event = 'Missed Tackle' then 1.0 else 0.0 end ) as missed_tackle,
sum(case when event_type = 'Chase Tackle' then 1.0 else 0.0 end ) as chase_tackle,
sum(case when event_type = 'Cover Tackle' then 1.0 else 0.0 end ) as cover_tackle,
sum(case when event_type = 'Line Tackle' then 1.0 else 0.0 end ) as line_tackle,
sum(case when event_type = 'Guard Tackle' then 1.0 else 0.0 end ) as guard_tackle,
sum(case when event_type = 'Edge Tackle' then 1.0 else 0.0 end ) as edge_tackle,
sum(case when event_type = 'Forced In Touch' then 1.0 else 0.0 end ) as forced_in_touch,
sum(case when event_type = 'Offload Allowed' then 1.0 else 0.0 end ) as offload_allowed,
sum(case when event_type = 'Sack' then 1.0 else 0.0 end ) as sack,
sum(case when event_type = 'Bumped Off' then 1.0 else 0.0 end ) as bumped_off,
sum(case when event_type = 'Stepped' then 1.0 else 0.0 end ) as stepped,
sum(case when event_type = 'Outpaced' then 1.0 else 0.0 end ) as outpaced,
sum(case when event = 'Tackle' and description = 'Tackle Assist' then 1.0 else 0.0 end ) as assist_tackle,

-- scrum profile
sum(case when event = 'Scrum' then 1.0 else 0.0 end ) as scrum,
sum(case when event = 'Scrum' and description = 'Negative' then 1.0 else 0.0 end ) as scrum_neg,
sum(case when event = 'Scrum' and description = 'Positive' then 1.0 else 0.0 end ) as scrum_pos,
sum(case when event = 'Offensive Scrum' then 1.0 else 0.0 end ) as offensive_scrum,
sum(case when event = 'Defensive Scrum' then 1.0 else 0.0 end ) as defensive_scrum,
sum(case when event = 'Scrum Offence' then 1.0 else 0.0 end ) as scrum_offence,

-- lineout profile

sum(case when event = 'Lineout Throw' then 1.0 else 0.0 end ) as lineout_throw,
sum(case when event = 'Lineout Take' then 1.0 else 0.0 end ) as lineout_take,
sum(case when event_type = 'Lineout Steal Front' then 1.0 else 0.0 end ) as lineout_steal_front,
sum(case when event_type = 'Lineout Steal Middle' then 1.0 else 0.0 end ) as lineout__steal_mid,
sum(case when event_type = 'Lineout Steal Back' then 1.0 else 0.0 end ) as lineout__steal_back,
sum(case when event_type = 'Lineout Win Back' then 1.0 else 0.0 end ) as lineout_win_back,
sum(case when event_type = 'Lineout Win Front' then 1.0 else 0.0 end ) as lineout_win_front,
sum(case when event_type = 'Lineout Win Middle' then 1.0 else 0.0 end ) as lineout_mid,
sum(case when description = 'Catch And Drive' then 1.0 else 0.0 end ) as catch_and_drive,
sum(case when description = 'Catch And Pass' then 1.0 else 0.0 end ) as catch_and_pass,
sum(case when description = 'Off The Top' then 1.0 else 0.0 end ) as off_the_top,
sum(case when event_type = 'Lineout Offence' then 1.0 else 0.0 end ) as lineout_offence,


sum(case when event = 'Penalty Conceded' then 1.0 else 0.0 end ) as penalty_conceded,
sum(case when event_type = 'Not Releasing' then 1.0 else 0.0 end ) as not_releasing,
sum(case when event_type = 'Hands In Ruck' then 1.0 else 0.0 end ) as hands_in_ruck,
sum(case when event_type = 'Wrong Side' then 1.0 else 0.0 end ) as wrong_side,
sum(case when event_type = 'Offside' then 1.0 else 0.0 end ) as offside,
sum(case when event_type = 'Not Rolling Away' then 1.0 else 0.0 end ) as not_rolling_away,
sum(case when event_type = 'Foul Play - Foot Contact' then 1.0 else 0.0 end ) as foul_play_foot_contact,
sum(case when event_type = 'Foul Play - Mid Air Tackle' then 1.0 else 0.0 end ) as foul_play_mid_air_tackle,
sum(case when event_type = 'Foul Play - High Tackle' then 1.0 else 0.0 end ) as foul_play_high_tackle,
sum(case when event_type = 'Foul Play - Other' then 1.0 else 0.0 end ) as foul_play_other,
sum(case when event_type = 'Obstruction' then 1.0 else 0.0 end ) as obstruction,

sum(case when event = 'Turnover' then 1.0 else 0.0 end ) as turnover,
sum(case when event_type = 'Turnover Won' then 1.0 else 0.0 end ) as turnover_won,
sum(case when event = 'Try' then 1.0 else 0.0 end ) as try,
sum(case when event = 'Goal Kick' then 1.0 else 0.0 end ) as goal_kick,

sum(case when event_type = 'Conversion' then 1.0 else 0.0 end ) as conversion,
sum(case when event_type = 'Drop Goal' then 1.0 else 0.0 end ) as drop_goal,
sum(case when event_type = 'Penalty Goal' then 1.0 else 0.0 end ) as penalty_kick,

sum(case when event = 'Collection' then 1.0 else 0.0 end ) as collection,
sum(case when event = 'Card' then 1.0 else 0.0 end ) as card


from
match_events t1 join
players t2 on (
  t1.team_name	  = t2.team_name	and
  t1.position	    = t2.position and
  t1.players_name = t2.players_name
)
where
t1.position > 0
group by
1,2,3,4,5,6
order by
1,2
