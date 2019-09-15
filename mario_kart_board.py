import matplotlib.pyplot as plt
import subprocess as sp
import datetime as dt
import numpy as np
import sys
import os

FILE = sys.argv[1]
TIMEFORMAT_F = '%M:%S.%f'
TIMEFORMAT_M = '%S.%f'
SHOW_PLOTS = False
SAVE_PLOTS = True
SAVE_FOLDER = "mk_graphs"
TRACK_NAME = "Unknown_Track"
EXECUTE_VIEWER = True

IMAGE_VIEWER = "eog"

def show(filename=None):
    if filename and SAVE_PLOTS:
        print("saving",filename)
        plt.savefig(SAVE_FOLDER+"/"+TRACK_NAME+"/"+filename)
        plt.clf()
    if SHOW_PLOTS:
        plt.show()
    
def normalize(values):
    mv = max(values)
    return [v/mv for v in values]

def randname(size):
    # unused
    chars = list('bcdfghjklmnpqrstvwxyz')
    vowels = list('aeiou')
    return ''.join([sample(chars,1)[0]+sample(vowels,1)[0] for i in range(int(size/2))]).title()
    
def gen_names(number, min_size, max_size):
    # unused
    return list(set([randname(randint(min_size,max_size)) for i in range(number)]))

def lineplotter(x,y,title,xlabel,ylabel,color='black',line='-'):
    plt.rcParams["date.autoformatter.hour"] = "%H:%M:%S"
    plt.rcParams["date.autoformatter.minute"] = "%H:%M:%S"
    plt.rcParams["date.autoformatter.second"] = "%H:%M:%S"
    plt.rcParams["date.autoformatter.microsecond"] = "%H:%M:%S"
    plt.plot(x,y,line,color=color)
    plt.scatter(x,y,color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

f = open(FILE).read().split('\n')
# getting track name
TRACK_NAME = f[0].replace('#','').strip().replace(' ','_')
# checking if folder exists
path = f'./{SAVE_FOLDER}/{TRACK_NAME}'
exists = os.path.isdir(path)
if not exists:
    print(f"{path} Doesn't exists. Creating new")
    os.makedirs(path)
#
lines = [v.replace(' ','').split('|') for v in f if "#" not in v and v]


players = {}
for pname, total_time, best_lap, worst_lap, index in lines:
    if pname not in players:
        players[pname] = {'best_race':None, 'best_lap':None, 'history': []}
    o = {'total':total_time,'best_lap':best_lap,'worst_lap':worst_lap,'index':index}
    players[pname]['history'].append(o)

# finding best race of each player
for player in players:
    times = []
    for race in players[player]['history']:
        if '-' not in race['total']:
            times.append(dt.datetime.strptime(race['total'],TIMEFORMAT_F))
    best_time = times[0]
    for time in times:
        if time<best_time:
            best_time = time
    players[player]['best_race'] = best_time.strftime(TIMEFORMAT_F).split(' ')[-1]

# finding best lap of each player
for player in players:
    times = []
    for race in players[player]['history']:
        if '-' not in race['best_lap']:
            times.append(dt.datetime.strptime(race['best_lap'],TIMEFORMAT_M))
    best_time = times[0]
    for time in times:
        if time<best_time:
            best_time = time
    players[player]['best_lap'] = best_time.strftime(TIMEFORMAT_F).split(' ')[-1]


#
def to_dt(x):
    if isinstance(x,dt.datetime):
        return x
    else:
        return dt.datetime.strptime(x,TIMEFORMAT_F)

def to_dt_m(x):
    if isinstance(x,dt.datetime):
        return x
    else:
        return dt.datetime.strptime(x,TIMEFORMAT_M)

ms_dif = lambda t1,t2: abs(to_dt(t1).timestamp()-to_dt(t2).timestamp())
ms_dif_m = lambda t1,t2: abs(to_dt_m(t1).timestamp()-to_dt_m(t2).timestamp())

# total time ranking
race_ranking = []
for player in players:
    obj = [players[player]['best_race'],player]
    race_ranking.append(obj)
race_ranking = sorted(race_ranking)

times, names = zip(*race_ranking)
biggest_time = times[-1]
best_time = times[0]

race_ranking = [[ms_dif(v[0],biggest_time),v[1]] for v in race_ranking]

print("\nRanking")
print(race_ranking)

times, names = zip(*race_ranking)
y_pos = np.arange(len(names))

times = normalize(times)

plt.bar(y_pos, times, align='center', alpha=1, color='black')
plt.xticks(y_pos, names)
plt.ylabel('time')
plt.title('Best Races Ranking')
show("race_ranking.jpg")

# best lap ranking
lap_ranking = []
for player in players:
    obj = [players[player]['best_lap'],player]
    lap_ranking.append(obj)
lap_ranking = sorted(lap_ranking)

times, names = zip(*lap_ranking)
biggest_time = times[-1]
best_time = times[0]

lap_ranking = [[ms_dif(v[0],biggest_time),v[1]] for v in lap_ranking]

print(lap_ranking)

times, names = zip(*lap_ranking)
y_pos = np.arange(len(names))

times = normalize(times)

plt.bar(y_pos, times, align='center', alpha=1, color='black')
plt.xticks(y_pos, names)
plt.ylabel('time')
plt.title('Best Laps Ranking')
show("ranking_laps.jpg")

# personal history
variancias = []
for player in players:
    phistory = players[player]['history']
    pdata = []
    for h in phistory:
        if '-' not in str(h):
            tot = to_dt(h['total'])
            best_lap = to_dt_m(h['best_lap'])
            worst_lap = to_dt_m(h['worst_lap'])
            index = int(h['index'])
            d = [index,tot,best_lap,worst_lap]
            pdata.append(d)
    pdata = sorted(pdata)
    index, total, best, worse = zip(*pdata)
    variance = [ms_dif(worse[i],best[i]) for i in range(len(best))]
    # def lineplotter(x,y,title,xlabel,ylabel,color='black',line='-'):
    ## races
    title = player+" races"
    lineplotter(index,total,title,"index","time")
    show("best_race_"+player+".jpg") 
    ## best lap
    title = player+" best and worse laps"
    lineplotter(index,best,title,"index","time",color='blue',line='--')
    lineplotter(index,worse,title,"index","time",color='red',line='--')
    show("best_lap_"+player+".jpg") 
    ## variance
    title = 'Variation between best and worse laps ('+player+')'
    lineplotter(index,variance,title,'index','time')
    show("vari_"+player+".jpg")
    #
    variancias.append([min(variance),player])

print(variancias)

varis, names = zip(*variancias)
y_pos = np.arange(len(names))

plt.bar(y_pos, varis, align='center', alpha=1, color='black')
plt.xticks(y_pos, names)
plt.ylabel('instability')
plt.title('Lap times variation')
show("instab.jpg")

if EXECUTE_VIEWER:
    sp.getoutput(f"{IMAGE_VIEWER} {path}")
