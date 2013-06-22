# coding: utf-8cd
import simplejson
from machtnetz import csvstore
import sys,os

home="/home/martin/projekte/machtnetz/py"
sys.path.append(home)
os.chdir(home)


d=csvstore.csvstore("../data/Sicherungskopie Aufsichtsraete_23Jan2012_v39 - nach Unternehmen.csv")


persons={}
companies={}
edges=[]

def makeid(a) :
    return str(hash(a))


for p in d.data :
    if not p["name"] in persons :
        persons[p["name"]]={ "id" : makeid(p["name"]), "name" : p["name"], "data" : { "raw": [] }}
    persons[p["name"]]["data"]["raw"].append(p)
    if not p["unternehmen"] in companies :
        companies[p["unternehmen"]]={ "id" : makeid(p["unternehmen"]), "name" : p["unternehmen"],
                                      "data" : {} }
    edges.append({ "source" : persons[p["name"]]["id"],
                   "target" : companies[p["unternehmen"]]["id"],
                   "data"   : { "raw" : p } } )
    
nodes=[]
for n in persons.values() :
    for f in ("geschlecht","geboren") :
        n["data"][f]=n["data"]["raw"][0][f]
    del n["data"]["raw"]
    n["type"]="person"
    nodes.append(n)
    
for n in companies.values() :
    n["type"]="company"
    nodes.append(n)
    
for e in edges :
    for f in ("ar_vertritt","ar_vergütung") :
        ef=f.replace("ar_","")
        e["data"][ef]=e["data"]["raw"][f]
    del e["data"]["raw"]
    
simplejson.dump({ "edges" : edges, "nodes" : nodes }, open("../data/aufsichtsrat.json", "w"))
