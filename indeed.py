#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re
from urllib import urlencode,urlopen


AGE = 60 or 'any'
AGE = 60
DIST = 15
LIMIT = 10
SWISS = ['Genève, GE', 'Genève']

regions = ['Paris', 'Rhône-Alpes', 'Essonnes', 'Essonne', 'Lyon', 'Grenoble', 'Genève, GE', 'Annemasse', 'Chambéry', 'Annecy']
postes = ['ingénieur logiciel', 'software engineer', 'développeur', 'devops', 'ingénieur de production']
entreprises = ['CERN', 'CEA', 'INRIA', 'CNRS']
domaines = ['Carte à puce', 'Smartcard', 'Laboratoire']
words = ['python', 'django', 'angular', 'bootstrap', 'responsive']
keywords = postes + [''] + entreprises + [''] + domaines + [''] + words

def build_search_url(**args):
    '''http://www.indeed.fr/emplois?as_and=&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&radius=50&l=Paris&fromage=15&limit=50&sort=date&psf=advsrch'''

    args['as_and'] = args.get('as_and','')
    args['as_phr'] = args.get('as_phr','')
    args['as_any'] = args.get('as_any','')
    args['as_not'] = args.get('as_not','')
    args['as_ttl'] = args.get('as_ttl','')
    args['as_cmp'] = args.get('as_cmp','')
    args['jt'] = args.get('jt','all') # job type
    args['st'] = args.get('st','')
    args['radius'] = args.get('radius',DIST)
    args['l'] = args.get('l','')
    args['fromage'] = args.get('fromage',AGE)
    args['limit'] = args.get('limit',LIMIT)
    args['sort'] = args.get('sort','date')
    args['psf'] = args.get('psf','advsrch')
  
    if args['l'] in SWISS:
        url = 'http://www.indeed.ch/Stellen?'
    else:
        url = 'http://www.indeed.fr/emplois?'
    
    try:
        url += urlencode(args)
    except:
        print args
        raise
    
    # print url
    return url
  

def query(all='', any='', exact='', no='', l='Paris', r=DIST, t=AGE):
    url = build_search_url(as_and=all, as_any=any, as_not=no, l=l, radius=r, fromage=t)
    page = urlopen(url).read()
    
    if l in SWISS:
        pattern = '<div id="searchCount">Stellen (.*) - (.*) von (.*)</div>'
    else:
        pattern = '<div id="searchCount">Emplois (.*) à (.*) sur (.*)</div>'
    m = re.search(pattern, page)
    
    if not m:
        return 0
    else:
        n,tot,max = m.group(1).replace('\xc2\xa0',''),m.group(2).replace('\xc2\xa0',''),m.group(3).replace('\xc2\xa0','')
        # print n, tot, max
    
    if int(tot) == LIMIT:
        return max
    else:
        return tot
    

# print query("python",l="Genève")
# sys.exit(0)

# for r in regions:
# for r in ['Fontainebleau']:
#     print '\n',r
#     for k in keywords:
#         print query(k, l=r) if k else '\''

# print query('ingénieur', any="python django", t=30)
# print query('ingénieur', any="django", no="python", t=30)
# print query('ingénieur', any="python django", no="django", t=30)
# print query('ingénieur', any="python", no="django", t=30)
# print query('', any="ingénieur python", no="django", t=30)
# print query('ingénieur python', t=30)
# print query('ingénieur django', t=30)
# print query('ingénieur python django', t=30)
# print query("django")
# print query("python")
# print query("python django")
# print query(any="python django")
# print query("django", no="python")
# print query("django")
# print query("python")

### DISTANCES Vol d'oiseau ###

# Annecy-Genève ou Annemasse 33
# Annecy-Gex 47
# Annecy-Chambéry 40
# Chambéry-Aix les bains 13
# Chambéry-Grenoble 46 (49 d'après indeed)
# Chambéry-Genève 74
# Chambéry-Gex 86
# Chambéry-Lyon 86
# Grenoble-Lyon 94
# Grenoble-Genève 119
# Lyon-Genève 112
# Lyon-Chalon 112
# Lyon-Valence 92
# Lyon-Clermont 135

# Versailles-Paris 17
# Palaiseau-Versailles 13
# Palaiseau-Evry 17
# Evry-Arpajon 14
# Evry-Melun 19
# Melun-Fontainebleau 16

### RECHERCHES ###

# Très Large : Lyon 120 Km
# Large : Chambéry 75-80 Km
# Ciblée: Grenoble 25, Chambéry 25, Annemasse 30? ou Annecy 20, Annemasse 20

#### Popularité des technos :
# Bootstrap, angularjs, backbonejs, web components, rails, django, symphony2,

# print query("python", l="Chambéry", t=60, r=49)
# print query("python", l="Chambéry", t=60, r=10)
# print query("python", l="Grenoble", t=60, r=10)
# print query("python", l="Aix-les-Bains", t=60, r=10)
# print query("python", l="Annecy", t=60, r=10)
# print query("python", l="Bourgoin-Jailleu", t=60, r=10)
# print query("python", l="Albertville", t=60, r=10)

print query("scada", l="Annemasse", t=60)