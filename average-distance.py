#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os.path, glob
from datetime import datetime


for file in glob.glob('csv/*.csv'):
    if '-avg' in file:
        continue
    num = {
        'Samedi': {},
        'Dimanche': {},
        'Semaine': {},
    }
    tot = {
        'Samedi': {},
        'Dimanche': {},
        'Semaine': {},
    }
    with open(file) as fd:
        for line in fd.readlines()[1:]:
            time, aller, retour, da, dr = line.rstrip('\n').split(',')
            t = time.split(' ')
            d = datetime.strptime(t[0], '%d/%m/%Y').isoweekday()
            if d == 6:
                j = 'Samedi'
            elif d == 7:
                j = 'Dimanche'
            else:
                j = 'Semaine'
            t = t[1]
            if t not in tot[j]:
                tot[j][t] = (0,0,0,0)
                num[j][t] = 0
            tot[j][t] = map(sum, zip(tot[j][t], map(int, [aller,retour,da,dr])))
            num[j][t] += 1
    
    with open(file[:-4]+'-avg.csv', 'w') as fd:
        fd.write('Heure,Aller Semaine,Retour Semaine, Aller Sam, Retour Sam, Aller Dim, Retour Dim\n')
        for t in sorted(tot['Semaine']):
            avg_week = map(lambda x: x / num['Semaine'][t], tot['Semaine'][t])
            avg_sat = map(lambda x: x / num['Samedi'][t], tot['Samedi'][t])
            avg_sun = map(lambda x: x / num['Dimanche'][t], tot['Dimanche'][t])
            fd.write(','.join(map(str, [datetime.now().strftime("%d/%m/%Y ")+t, avg_week[0], avg_week[1], avg_sat[0], avg_sat[1], avg_sun[0], avg_sun[1] ])))
            fd.write('\n')
            print t, avg_week
