/* /udd/reeks/cavin1/CAVIN1.Yuan.23DEC2023.sas Program to use Yuan's PROR GLM program with 3-way factorial design, updated to assess signs, using all analytes tested, 
in all five repeats or three selected repeats */

data temp1;
input repeat sirna $ detect $ ct;
cards; 
1 ConsiRNA CAVIN1 23.748
1 ConsiRNA CAVIN1 23.780
1 CavsiRNA CAVIN1 27.541
1 CavsiRNA CAVIN1 27.659
1 ConsiRNA IL6    33.135
1 ConsiRNA IL6    32.934
1 CavsiRNA IL6    33.182
1 CavsiRNA IL6    34.069
1 ConsiRNA IL8    28.426
1 ConsiRNA IL8    28.197
1 CavsiRNA IL8    27.611
1 CavsiRNA IL8    27.698
1 ConsiRNA IL33   36.184
1 ConsiRNA IL33   36.067
1 CavsiRNA IL33   36.000
1 CavsiRNA IL33   36.000
1 ConsiRNA S100A4 33.575
1 ConsiRNA S100A4 34.440
1 CavsiRNA S100A4 33.941
1 CavsiRNA S100A4 34.076
1 ConsiRNA SIRT1  31.056
1 ConsiRNA SIRT1  31.109
1 CavsiRNA SIRT1  31.479
1 CavsiRNA SIRT1  31.389
1 ConsiRNA SIRT3  34.602
1 ConsiRNA SIRT3  33.777
1 CavsiRNA SIRT3  33.895
1 CavsiRNA SIRT3  33.665
1 ConsiRNA GAPDH  22.152
1 ConsiRNA GAPDH  22.086
1 CavsiRNA GAPDH  21.911
1 CavsiRNA GAPDH  21.968
2 ConsiRNA CAVIN1 24.433
2 ConsiRNA CAVIN1 24.390
2 CavsiRNA CAVIN1 24.936
2 CavsiRNA CAVIN1 24.995
2 CavsiRNA CAVIN1 25.115
2 CavsiRNA CAVIN1 24.926
2 ConsiRNA IL6    30.793
2 ConsiRNA IL6    30.757
2 CavsiRNA IL6    30.482
2 CavsiRNA IL6    30.449
2 CavsiRNA IL6    31.138
2 CavsiRNA IL6    31.130
2 ConsiRNA IL8    27.371
2 ConsiRNA IL8    27.760
2 CavsiRNA IL8    25.974
2 CavsiRNA IL8    26.013
2 CavsiRNA IL8    27.727
2 CavsiRNA IL8    28.189
2 ConsiRNA IL33   35.247
2 ConsiRNA IL33   34.985
2 CavsiRNA IL33   35.552
2 CavsiRNA IL33   35.552
2 CavsiRNA IL33   34.527
2 CavsiRNA IL33   35.913
2 ConsiRNA S100A4 30.118
2 ConsiRNA S100A4 30.398
2 CavsiRNA S100A4 30.034
2 CavsiRNA S100A4 30.100
2 CavsiRNA S100A4 29.846
2 CavsiRNA S100A4 29.939
2 ConsiRNA SIRT1  27.858
2 ConsiRNA SIRT1  27.964
2 CavsiRNA SIRT1  26.833
2 CavsiRNA SIRT1  26.818
2 CavsiRNA SIRT1  27.884
2 CavsiRNA SIRT1  27.945
2 ConsiRNA SIRT3  28.068
2 ConsiRNA SIRT3  27.911
2 CavsiRNA SIRT3  28.582
2 CavsiRNA SIRT3  28.452
2 CavsiRNA SIRT3  27.869
2 CavsiRNA SIRT3  27.724
2 ConsiRNA GAPDH  21.185
2 ConsiRNA GAPDH  20.489
2 CavsiRNA GAPDH  20.370
2 CavsiRNA GAPDH  20.265
2 CavsiRNA GAPDH  20.202
2 CavsiRNA GAPDH  20.208
3 ConsiRNA CAVIN1 25.183
3 ConsiRNA CAVIN1 25.077
3 CavsiRNA CAVIN1 28.146
3 CavsiRNA CAVIN1 28.236
3 ConsiRNA CAVIN1 25.566
3 ConsiRNA CAVIN1 25.562
3 CavsiRNA CAVIN1 28.887
3 CavsiRNA CAVIN1 28.867
3 ConsiRNA IL6    22.155
3 ConsiRNA IL6    22.136
3 CavsiRNA IL6    22.277
3 CavsiRNA IL6    22.267
3 ConsiRNA IL6    22.859
3 ConsiRNA IL6    22.769
3 CavsiRNA IL6    25.061
3 CavsiRNA IL6    25.108
3 ConsiRNA IL8    18.735
3 ConsiRNA IL8    18.759
3 CavsiRNA IL8    18.702
3 CavsiRNA IL8    18.706
3 ConsiRNA IL8    19.160
3 ConsiRNA IL8    19.181
3 CavsiRNA IL8    20.952
3 CavsiRNA IL8    20.967
3 ConsiRNA IL33   27.098
3 ConsiRNA IL33   27.103
3 CavsiRNA IL33   28.255
3 CavsiRNA IL33   28.201
3 ConsiRNA IL33   28.177
3 ConsiRNA IL33   27.981
3 CavsiRNA IL33   30.359
3 CavsiRNA IL33   30.815
3 ConsiRNA S100A4 29.636
3 ConsiRNA S100A4 29.915
3 CavsiRNA S100A4 29.502
3 CavsiRNA S100A4 29.502
3 ConsiRNA S100A4 29.879
3 ConsiRNA S100A4 29.831
3 CavsiRNA S100A4 29.328
3 CavsiRNA S100A4 29.176
3 ConsiRNA SIRT1  24.305
3 ConsiRNA SIRT1  24.289
3 CavsiRNA SIRT1  24.658
3 CavsiRNA SIRT1  24.624
3 ConsiRNA SIRT1  24.338
3 ConsiRNA SIRT1  24.480
3 CavsiRNA SIRT1  25.538
3 CavsiRNA SIRT1  25.863
3 ConsiRNA SIRT3  29.363
3 ConsiRNA SIRT3  29.589
3 CavsiRNA SIRT3  29.239
3 CavsiRNA SIRT3  29.264
3 ConsiRNA SIRT3  29.602
3 ConsiRNA SIRT3  29.765
3 CavsiRNA SIRT3  29.083
3 CavsiRNA SIRT3  29.232
3 ConsiRNA GAPDH  19.982
3 ConsiRNA GAPDH  19.971
3 CavsiRNA GAPDH  20.174
3 CavsiRNA GAPDH  20.123
3 ConsiRNA GAPDH  20.277
3 ConsiRNA GAPDH  20.271
3 CavsiRNA GAPDH  20.985
3 CavsiRNA GAPDH  21.085
4 ConsiRNA CAVIN1 21.469
4 ConsiRNA CAVIN1 21.364
4 CavsiRNA CAVIN1 23.775
4 CavsiRNA CAVIN1 23.828
4 ConsiRNA IL6    29.952
4 ConsiRNA IL6    30.020
4 CavsiRNA IL6    29.719
4 CavsiRNA IL6    29.939
4 ConsiRNA IL8    23.472
4 ConsiRNA IL8    23.682
4 CavsiRNA IL8    22.775
4 CavsiRNA IL8    22.751
4 ConsiRNA IL33   31.386
4 ConsiRNA IL33   31.413
4 CavsiRNA IL33   31.295
4 CavsiRNA IL33   30.928
4 ConsiRNA S100A4 26.232
4 ConsiRNA S100A4 26.424
4 CavsiRNA S100A4 25.768
4 CavsiRNA S100A4 26.089
4 ConsiRNA SIRT1  25.729
4 ConsiRNA SIRT1  25.637
4 CavsiRNA SIRT1  25.667
4 CavsiRNA SIRT1  25.647
4 ConsiRNA SIRT3  27.784
4 ConsiRNA SIRT3  27.908
4 CavsiRNA SIRT3  27.704
4 CavsiRNA SIRT3  27.913
4 ConsiRNA GAPDH  18.312
4 ConsiRNA GAPDH  18.241
4 CavsiRNA GAPDH  17.985
4 CavsiRNA GAPDH  17.985
5 ConsiRNA CAVIN1 26.417
5 ConsiRNA CAVIN1 26.292
5 CavsiRNA CAVIN1 28.032
5 CavsiRNA CAVIN1 28.762
5 ConsiRNA IL6    30.981
5 ConsiRNA IL6    29.233
5 CavsiRNA IL6    31.003
5 CavsiRNA IL6    31.916
5 ConsiRNA IL8    26.381
5 ConsiRNA IL8    26.401
5 CavsiRNA IL8    26.575
5 CavsiRNA IL8    26.095
5 ConsiRNA IL33   36.360
5 ConsiRNA IL33   36.981
5 CavsiRNA IL33   37.245
5 CavsiRNA IL33   38.273
5 ConsiRNA S100A4 24.489
5 ConsiRNA S100A4 23.336
5 CavsiRNA S100A4 33.966
5 CavsiRNA S100A4 33.108
5 ConsiRNA SIRT1  26.961
5 ConsiRNA SIRT1  26.553
5 CavsiRNA SIRT1  27.334
5 CavsiRNA SIRT1  27.707
5 ConsiRNA SIRT3  35.599
5 ConsiRNA SIRT3  35.669
5 CavsiRNA SIRT3  36.338
5 CavsiRNA SIRT3  35.946
5 ConsiRNA GAPDH  22.961
5 ConsiRNA GAPDH  23.478
5 CavsiRNA GAPDH  24.922
5 CavsiRNA GAPDH  23.601
; 
run;

proc sort data=temp1;
by sirna;
run;

proc print data=temp1;
var sirna repeat detect ct;
run;
                                                                                                                          
data temp2a;                                                                                                                   
set temp1;                                                                                                                    
if detect = 'CAVIN1' then delete; /* IL6 and GAPDH only*/
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp2a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL6 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL6 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp2b;
set temp1;
if detect = 'CAVIN1' then delete; /* IL6 and GAPDH only*/
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp2b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL6 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL6 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;



data temp3a;
set temp1;
if detect = 'IL6' then delete; /* CAVIN1 and GAPDH only*/
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp3a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for CAVIN1 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for CAVIN1 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp3b;
set temp1;
if detect = 'IL6' then delete; /* CAVIN1 and GAPDH only*/
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;


proc glm data=temp3b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for CAVIN1 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for CAVIN1 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;


data temp4a;
set temp1;
if detect = 'IL6' then delete; /* IL8 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp4a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL8 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL8 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp4b;
set temp1;
if detect = 'IL6' then delete; /* IL8 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp4b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL8 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL8 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp5a;
set temp1;
if detect = 'IL6' then delete; /* IL33 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp5a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL33 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL33 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp5b;
set temp1;
if detect = 'IL6' then delete; /* IL33 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp5b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for IL33 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for IL33 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;


data temp6a;
set temp1;
if detect = 'IL6' then delete; /* S100A4 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp6a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for S100A4 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for S100A4 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp6b;
set temp1;
if detect = 'IL6' then delete; /* S100A4 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'SIRT1' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp6b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for S100A4 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for S100A4 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp7a;
set temp1;
if detect = 'IL6' then delete; /* SIRT1 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT3' then delete;
run;

proc glm data=temp7a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for SIRT1 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for SIRT1 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp7b;
set temp1;
if detect = 'IL6' then delete; /* SIRT1 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT3' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp7b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for SIRT1 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for SIRT1 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp8a;
set temp1;
if detect = 'IL6' then delete; /* SIRT3 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
run;

proc glm data=temp8a order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for SIRT3 all 5 repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for SIRT3 all 5 repeats' sirna*detect 1 -1 -1 1 ;
run;

data temp8b;
set temp1;
if detect = 'IL6' then delete; /* SIRT3 and GAPDH only*/
if detect = 'CAVIN1' then delete;
if detect = 'IL8' then delete;
if detect = 'IL33' then delete;
if detect = 'S100A4' then delete;
if detect = 'SIRT1' then delete;
if repeat=3 then delete;
if repeat=5 then delete;
run;

proc glm data=temp8b order=data;
class repeat sirna detect;
model ct = repeat|sirna|detect;
lsmeans sirna*detect /pdiff cl tdiff adjust=tukey;
contrast 'Treatment and Gene Effect for SIRT3 3 selected repeats' sirna*detect 1 -1 -1 1 ;
estimate 'Treatment and Gene Effect for SIRT3 3 selected repeats' sirna*detect 1 -1 -1 1 ;
run;


/* now calculate relative effects using delta delta Ct method

data ct1;
input repeat siRNA $ gapdhct hhipct sp3ct;
cards;
1 sp3 20.4561180 30.0776695 25.6477145 
1 nt  20.5309735 30.5909890 25.2185325
2 sp3 19.8919280 28.3263815 25.3350685
2 nt  19.8252710 29.1104860 24.9887295
3 sp3 19.5058030 27.7605400 27.0309180
3 nt  19.5810450 28.6820590 25.6902970
4 sp3 19.4704810 29.7023905 25.0445055
4 nt  19.4245900 30.4145050 24.4818865
5 sp3 19.4108065 29.7099975 24.6528900
5 nt  19.5189230 30.7543410 24.3361025
;
run;

data ct2;
set ct1;
deltahhip = hhipct - gapdhct;
deltasp3 = sp3ct - gapdhct;
run;

proc print data = ct2;
var repeat siRNA deltahhip deltasp3;
run;

data ct3;
input repeat gene $ deltasi deltant;
cards;
1 hhip  9.6216   10.0600
1 sp3   5.19160  4.68756
2 hhip  8.4345   9.2852
2 sp3   5.44314  5.16346
3 hhip  8.2547   9.1010
3 sp3   7.52512  6.10925
4 hhip  10.2319  10.9899
4 sp3   5.57402  5.05730
5 hhip  10.2992  11.2354
5 sp3   5.24208  4.81718
;
run;

data ct4;
set ct3;
deltdelt = deltasi - deltant;
expdelt = 2**((-1)*(deltdelt));
run;

proc sort data=ct4;
by gene;
run;

proc means data=ct4 mean stddev stderr;
var deltdelt expdelt;
by gene;
run;
 
*/
