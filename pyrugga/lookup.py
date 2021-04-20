"""
Author: James Londal
Copyright: Copyright 2021, Picopie Ltd
License: GNU AFFERO GENERAL PUBLIC LICENSE
Version: 1.0.0
Maintainer: James Londal
"""

import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd

EVENTS = StringIO("""action,event
1,Carry
2,Tackle
3,Pass
4,Kick
5,Scrum
6,Lineout Throw
7,Penalty Conceded
8,Turnover
9,Try
10,Attacking Qualities
11,Goal Kick
12,Missed Tackle
13,Turnover Won
14,Restart
15,Possession
16,Other
17,Period
18,Collection
19,Team Play
20,Ref Review
21,Card
22,Clock
23,Ruck
24,Maul
26,Sequence
27,Lineout Take
28,Offensive Scrum
29,Defensive Scrum
44,Counter Attack
45,Defensive Exits
46,Attacking 22 Entry
41,Players Leavign Field
40,Defensive Actions
42,Player Enters Field
43,Ruck OOA""")

DESCRIPTIONS = StringIO("""qualifier,qualifier_description
101,One Out Drive
102,Pick And Go
103,Other Carry
104,Kick Return
105,Restart Return
106,Support Carry
107,Tackled Dominant
108,Tackled Neutral
109,Crossed Gainline
110,Neutral
111,Failed Gainline
112,Initial Break
113,Supported Break
115,Penalty Won
116,Defender Beaten
117,Try Scored
118,Other
119,Error
120,Kick
121,Pass
122,Off Load
124,Pen Conceded
125,Back Move
126,Lateral Offload
127,Backward Offload
128,Own Player
129,To Ground
130,To Opposition
131,Slow
132,Normal
133,Fast
134,Review
135,Left Play
136,Right Play
137,Open Play
138,Blind Play
139,Pass Play
140,Kick Run Play
141,Set Move Play
142,Chase Tackle
143,Cover Tackle
144,Line Tackle
145,Guard Tackle
146,Edge Tackle
147,Other Tackle
148,Penalty Kick
149,Low
150,High
151,Offload
152,Kick Pressure
153,Complete
154,Forced In Touch
155,Offload Allowed
156,Turnover Won
157,Pen Conceded
158,Try Saver
159,Sack
160,Passive - To Ground
161,Missed
162,Bumped Off
163,Stepped
164,Outpaced
165,Positional
166,Tackled
167,Clean Break
168,Try Scored
169,Complete Pass
170,Ruck Pass
171,Miss Pass
172,Break Pass
173,Forward Pass
174,Incomplete Pass
175,Intercepted Pass
176,Key Pass
177,Off Target Pass
178,Try Pass
179,Receiver
180,Pass Error
181,Right Pass
182,Left Pass
183,Long Pass
184,Short Pass
185,Kick In Play
186,Kick In Own 22
187,Bomb
188,Chip
189,Cross Pitch
190,Territorial
191,Low
192,Kick In Touch (Bounce)
193,Kick In Touch (Full)
194,Error - Charged Down
195,Error - Out Of Play
196,Error - Terratorial Loss
197,Error - Dead Ball
198,Caught Full
199,Collected Bounce
200,In Goal
201,Own Player - Collected
202,Own Player - Failed
203,Pressure Carried Over
204,Pressure In Touch
205,Pressure Error
206,Try Kick
207,Catch And Drive
208,Catch And Pass
209,Won Penalty Try
210,Penalty Won
211,Off The Top
212,Pressured Kick
213,No Pressure Kick
214,Offence
215,Defence
216,Not Releasing
217,Hands In Ruck
218,Wrong Side
219,Offside
220,Offside At Kick
221,Collapsing Maul
222,Scrum Offence
223,Lineout Offence
224,Off Feet At Ruck
225,Not Rolling Away
226,Foul Play - Foot Contact
227,Foul Play - Mid Air Tackle
228,Foul Play - High Tackle
229,Foul Play - Other
230,Other Offence
231,Obstruction
232,Dissent
233,Full Penalty
235,Free Kick
236,No Action
237,Yellow Card
238,Red Card
239,On Report
240,Warning
241,Penalty Try
242,TJ Intervention - Pen
243,Ref Discussion
244,Video Review
245,Advantage
246,Yellow
247,Red
248,White
249,Attempted Intercept
250,Bad Offload
251,Bad Pass
252,Carried Over
253,Carried In Touch
254,Dropped Ball Unforced
255,Forward Pass
256,Lost Ball Forced
257,Accidental Offside
258,Lost In Ruck Or Maul
259,Reset
260,Other Error
261,Kick Error
262,Failure To Find Touch
263,Grounding Ball
264,Defence
265,Attack
266,Forced
267,Unforced
268,Interception
269,In Goal Touchdown
270,Mark
271,Attacking Catch
272,Attacking Loose Ball
273,Defensive Catch
274,Defensive Loose Ball
275,Restart Catch
276,Jackal
277,Success
278,Fail
279,Pressure
280,No Pressure
281,50m Restart Kick
282,22m Restart Kick
283,Forward Play
284,Restart Retained
285,Restart Opp Error
286,Restart Opp Collection
287,Restart Own Error
288,Restart Long
289,Restart Short
290,Restart High
291,Restart Low
292,Restart Out Of Play
293,Restart Not 10
294,Restart Offside
295,Conversion
296,Drop Goal
297,Penalty Goal
298,Goal Missed
299,Goal Kicked
300,Miss Left
301,Miss Right
302,Miss Short
303,Miss Hit Goal Kick
304,Hit Post
305,22m Restart
306,Lineout
307,50m Restart
308,Turnover Won
309,Scrum
310,Tap Pen
311,Kick Return
312,Free Kick
313,End Drop Goal
314,End Try
315,End Kick Out Of Play
316,End Pen Won
317,End Scrum
318,End Turnover
319,End Pen Con
320,End Other
321,End Of Play
322,Start Clock
323,Stop Clock
324,Injury
325,Video Replay
326,Disciplinary
327,End Of Period
328,Other
329,Foul Play?
330,Handling Err?
331,Line Decision?
332,Techinical Offence?
333,Video Ref Awarded
334,Video Ref Dissallowed
335,Disallowed Try
336,Ruck Offence?
337,Good Decision
338,Poor Referee Signal
339,Scrum Formation
340,LO Offence?
341,Techinal offence?
342,Wrong Mark?
343,Non Playing Personnel
344,Foul Play - Fighting
345,Foul Play - Dangerous Throw
346,Box
347,Touch Kick
348,Start Set Lineout Steal
349,Start Set 22m Restart Retained
350,Start Set 50m Restart Retained
351,End Set Kick In Play
352,Other Review
353,Won Outright
354,Won Try
356,Won Free Kick
357,Won Penalty
358,Lost Outright
359,Lost Pen Con
360,Lost Free Kick
361,Lost Reversed
362,Anti-Clockwise
363,Clockwise
364,Positive
365,Neutral
366,Negative
367,Scrum Half Pass
368,Scrum Half Kick
369,Scrum Half Run
370,No 8 Pick Up
371,Throw Front
372,Throw Middle
373,Throw Back
374,Throw 15m+
375,Throw Quick
376,Won Clean
377,Won Tap
378,Won Penalty
379,Won Free Kick
380,Won Other
381,Lost Not Straight
382,Lost Clean
383,Lost Free Kick
384,Lost Penalty
385,Lost Other
386,Lineout Win Front
387,Lineout Win Middle
388,Lineout Win Back
389,Lineout Win 15m+
390,Lineout Win Quick
391,Lineout Steal Front
392,Lineout Steal Middle
393,Lineout Steal Back
394,Lineout Steal 15m+
395,Lineout Steal Quick
396,Clean Catch
397,Clean Tap
398,Ineffective Tap
399,Error Missed Take
400,Error Dropped Take
401,Won Outright
402,Lost Outright
403,Penalty Won
404,Penalty Conceded
405,Try Scored
406,Penalty Try
407,Start Period
408,End Period
409,Tackled Ineffective
410,No 8 Pass
411,End Turnover (Scrum)
412,Start Set Scrum Steal
413,End Set Kick Error
414,End Set Kick In Goal
415,End Set Own Lineout
416,Restart Kick In Touch
417,Lost Handling Error
418,Lost Not 5m
419,Lost Overthrown
420,Catch and Run
421,Wrong Side At Ruck
422,Wrong Side At Maul
423,Deliberate Knock On
424,Foul Play - Late Tackle
425,Charging Into Ruck
426,Collapsing
427,Standing Up
428,Back Rows Unbound
429,Whipping Scrum
430,No 9 Offside
431,Not Straight
432,Delaying Put In
433,Barging
434,Obstruction
435,Offside
436,Taking Man In Air
437,Tap Back
438,Charge Down
439,Accidental Knock On
440,Referee Obstruction
441,Tackle Assist
442,Offside At Ruck - Att
443,Offside At Ruck - Def
444,Offside In General Play
445,Offside At Restart
446,Maul Obstruction
447,TJ Intervention - YC
448,TJ Intervention - RC
449,Boring In
450,Early Engagement
451,Wrong Side Run
452,Unplayable
453,Delaying Throw
454,Closing Gap
455,Early Lift
456,Wrong Numbers
457,Dissent Advance
458,Illegal Binding
459,Other Scrum Offence
460,Dominant Contact
461,Neutral Contact
462,Ineffective Contact
463,Quick throw from knock on
464,5 second rule
465,Lineout Alternative
466,Quick throw from upfield postion
467,Ineffective
468,Concussion
469,Retained Collection
470,FTSU
471,Passive - Upright
472,Neutral
473,Dominant Tackle Contact
474,Neutral Tackle Contact
475,Ineffective Tackle Contact
560,Tackle Arrival 
653,The player successfully kicks a ’50/22’ 
652,The player successfully kicks a ’22/50’ 
653,22 Entry Points – Try without Conversion 
654,22 Entry Points – Try and Conversion 
655,22 Entry Points – Penalty Try
656,22 Entry Points – Penalty Goal 
657,22 Entry Points – Drop Goal
658,22 Entry Outcome - Turnover 
659,22 Entry Outcome – Try 
660,22 Entry Outcome – Scrum Won
661,22 Entry Outcome – Penalty Won 
662,22 Entry Outcome – Penalty Goal Attempt 
663,22 Entry Outcome – Penalty Conceded 
664,22 Entry Outcome – Lineout Won
665,22 Entry Outcome – Kick Turnover 
638,22 Entry Outcome – Drop Goal
637,Captains Referral - Inconclusive 
636,Captains Referral – Overturned 
635,Captains Referral – Upheld
633,Defensive OOA 
632,Attacking OOA 
631,General Catch 
632,Kicked out of 22 
633,Carried out of 22 
628,Failed Exit From 22 
629,Turnover 
630,Try Scored
631,Scrum Won 
632,Penalty  Won 
633,Penalty Conceded
634,Lineout 621 Won 
635,Kicked Out 
636,Kick To Opposition
618,Drop Goal 
619,OOA Entry 15th Entry- Def 
620,OOA Entry 14th Entry- Def 
621,OOA Entry 13th Entry- Def 
622,OOA Entry 12th Entry- Def 
623,OOA Entry 11th Entry- Def 
624,OOA Entry 10th Entry- Def 
625,OOA Entry 9th Entry- Def 
626,OOA Entry 8th Entry- Def 
627,OOA Entry 7th Entry- Def 
628,OOA Entry 6th Entry- Def 
629,OOA Entry 5th Entry- Def 
630,OOA Entry 4th Entry- Def 
631,OOA Entry 3rd Entry- Def 
632,OOA Entry 2nd Entry- Def 
633,OOA Entry 1st Entry- Def 
634,OOA Entry 15th Entry- Att 
635,OOA Entry 14th Entry- Att 
636,OOA Entry 13th Entry- Att 
637,OOA Entry 12th Entry- Att 
638,OOA Entry 11th Entry- Att 
639,OOA Entry 10th Entry- Att 
640,OOA Entry 9th Entry- Att 
641,OOA Entry 8th Entry- Att 
642,OOA Entry 7th Entry- Att 
643,OOA Entry 6th Entry- Att 
644,OOA Entry 5th Entry- Att 
645,OOA Entry 4th Entry- Att 
646,OOA Entry 3rd Entry- Att 
647,OOA Entry 2nd Entry- Att 
648,OOA Entry 1st Entry- Att 
649,Own Team 5th+ Entry 
650,Own Team 4th Entry 
651,Own Team 3rd Entry 
652,Own Team 2nd Entry 
653,Own Team 1st Entry 
654,Penalty Conceded - Def 
655,Penalty Conceded – Att
656,Penalty Won 
657,Turnover Won 
658,Got Cleaned Out 
659,Not Clearing
660,Nuisance 
661,Attended 
662,Secured 
663,Failed Clearout 
664,Cleaned Out 
665,Red Card 
666,Yellow Card 
667,Reversal Front Row Replacement 
668,Reversal Concussion Replacement
669,Reversal Blood Replacement 
566,Front Row Replacement
565,Concussion 
564,Blood Replacement 
563,Injury
562,Tactical
561,Aerial Kick Contest 
562,N/A Ruck Speed 
563,6+ Seconds
564,5-6 Seconds
565,4-5 Seconds
566,3-4 Seconds
567,2-3 Seconds
568,1-2 Seconds
569,0-1 Seconds
570,N/A Gainline
571,Euqal to Gainline
572,Behind Gainline
548,Over Gainline
549,Stamping 
550,Persistent Infringement 
551,Fighting
552,Dissent
553,Professional Foul 
542,Foul Play
543,Charged Down 
544,Dropped Short 
545,Hit Crossbar 
546,Hit Right Post 
547,Hit Left Post 
548,Missed Right 
533,Missed Left 
534,Intercepted Break 
535,Kick Line Break 
536,Line Break
537,Snake 
538,Decoy 
539,Break Assist 
526,Try Assist 
527,Reload 
528,Idle 
505,Stayed on Ground 
506,4+ Tacklers Committed 
507,3 Tacklers Committed 
508,2 Tacklers Committed 
509,1 Tackler Committed
500,0 Tacklers Committed""")

events = pd.read_csv(EVENTS, sep=",")
descriptions = pd.read_csv(DESCRIPTIONS, sep=",")