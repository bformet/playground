#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, sys, os.path
from urllib import urlencode, urlopen
from datetime import datetime

maps_url = 'https://maps.google.fr/maps?'

args = {
    'dg': 'oo',
    'output': 'classic',
    'saddr': 'Palaiseau',
    'daddr': 'Paris',
    'q': '',
}

# adresses
PARIS = ('Paris', '59 rue du chateau des rentiers, Paris')
VILLEMOISSON = ('Villemoisson', "10 rue des Tisserands, Villemoisson-sur-Orge")
INRIA = ('Inria', "1 Rue Honore d'Estienne d'Orves, Palaiseau")
MASSY = ('Massy', "Quartier Vilmorin, Massy")
VILLEBON = ('Villebon', "Rue Paul Valeryy, Villebon-sur-Yvette")
SXLESCH = ('Saulx-les-Chartreux', "Saulx-les-Chartreux")
NOZAY = ('Nozay', "Nozay")
VILLEJUST = ('Villejust', 'Villejust')
ATLANTIS = ('Atlantis', 'Rue Charcot, Massy')

# recherches
searchs = [
    (INRIA, PARIS),
    (INRIA, MASSY),
    (INRIA, VILLEBON),
    (INRIA, SXLESCH),
    (INRIA, NOZAY),
    (INRIA, VILLEJUST),
    (INRIA, ATLANTIS),
    (VILLEMOISSON, PARIS),
    (VILLEMOISSON, MASSY),
    (VILLEMOISSON, VILLEBON),
    (VILLEMOISSON, SXLESCH),
    (VILLEMOISSON, NOZAY),
    (VILLEMOISSON, VILLEJUST),
    (VILLEMOISSON, ATLANTIS),
]


def get_distance(a ,b):
    args['saddr'] = a
    args['daddr'] = b
    url = maps_url + urlencode(args)    
    page = urlopen(url).read()
    # print url

    pattern = '([0-9]+|[0-9] heures? [0-9]+) min</span>'
    res = re.findall(pattern, page)
    
    def normalize(x):
        if 'heures' in x:
            return reduce(lambda i,j: int(i)*60+int(j), x.split(' heures '))
        elif 'heure' in x:
            return reduce(lambda i,j: int(i)*60+int(j), x.split(' heure '))
        else:
            return int(x)
    
    res = [normalize(x) for x in res]
    i = iter(res)
    res = zip(i, i)
    # print res
    
    min_time = 100000
    for a, b in res:
        if b < min_time:
            min_time = b
            diff = b - a
    
    return (min_time, diff)


# min_time, diff = get_distance(PARIS[1], INRIA[1])
# print datetime.now().strftime("%d/%m/%Y %H:%M"), min_time, diff

# total: 41 requetes par jours x 20 recherches = 820 requetes par jour

runtimes = ['01:00','05:00','07:00','07:30','08:00','08:30','08:45','09:00','09:10','09:20','09:30','09:45','10:00','10:30','11:00','11:30','12:00','12:30',
'13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','17:45','18:00','18:15','18:30','18:45','19:00','19:30','20:00','21:00','23:00']
# len=38

now = datetime.now()
with open("last-run",'w') as fd:
    fd.write(now.strftime("%d/%m/%Y %H:%M\n"))

if now.strftime("%H:%M") not in runtimes:
    sys.exit(1)

for a, b in searchs:
    name = '%s-%s' % (a[0], b[0])
    fname = '%s.csv' % name.lower()
    min_aller, diff_aller = get_distance(b[1], a[1])
    min_retour, diff_retour = get_distance(a[1], b[1])
    print name, min_aller, diff_aller, min_retour, diff_retour
    
    miss_header = not os.path.isfile(fname)
    fd = open(fname,'a')
    if miss_header:
        fd.write('Heure,Aller,Retour,Bouchons aller,Bouchons retour\n')
    fd.write(','.join([now.strftime("%d/%m/%Y %H:%M"), str(min_aller), str(min_retour), str(diff_aller), str(diff_retour)]))
    fd.write('\n')
    fd.close()

