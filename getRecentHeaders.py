#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
But : définir des fonctions
1 : get : "http://techpatterns.com/downloads/firefox/useragentswitcher.xml"
2 : parse
3 : create valid strings, eg : "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
4 : sort : mobile, ff, ch, gb, sa, ie, opera...
#"""

import os
import re
#~ import urllib as ul
import urllib.request as ulr


def isValidPATH(chemin):
    var = str(chemin)
    if var == "":
        return -1
    if "..." in var:
        return -1 
    if var == "." or var == "..":
        return 1
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    if slashes:
        var = var.replace('//', '/') 
        if var[-1] == "/":
            try:
                os.chdir(var)
                return 1  
            except:
                return -1 
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return -1
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    return 1      
                except:
                    return 2    
            else:
                return -2   
    else:
        try:
            os.chdir(var)
            return 1    
        except:
            if var in os.listdir():
                return 0    
            else:
                return -1   


def properPATH(chemin):
    ''' essaie de renvoyer un chemin valide. 
    properPATH(str()) renvoit un tuple : (PATH, FILE), avec :
        *  PATH = False si le chemin est faux.
        *  FILE = False si le ficher OU le chemin n'existe pas.  
    '''
    var = str(chemin)
    if var == "":
        return (False, False)
    if "..." in var:
        return (False, False)
    if var == "." or var == ".." or var == '/':
        return (str(var), False)
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    if slashes:
        var = var.replace('//', '/')
        if var[-1] == "/":
            try:
                os.chdir(var)
                return (os.getcwd(), False)
            except:
                return (False, False)
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            Liste.pop()
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return (False, False)
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    return (os.getcwd(), False)
                except:
                    return (os.getcwd(), str(lastItem))
            else:
                return (os.getcwd(), False)
    else:
        try:
            os.chdir(var)
            return (os.getcwd(), False)
        except:
            if var in os.listdir():
                return (os.getcwd(), str(var)) 
            else:
                return (False, False)


def properPATH2file(chemin):
    var = str(chemin) 
    if var == "":
        return (False, False)
    if "..." in var:
        return (False, False)
    if var == "." or var == ".." or var == '/':
        return (str(var), False)
    if var[0] == '/':
        os.chdir('/')
        var = var[1:]
    slashes = var.count('/')
    if slashes:
        var = var.replace('//', '/')
        if var[-1] == "/":
            try:
                os.chdir(var)
                return (os.getcwd(), False)   
            except:
                return (False, False) 
        #
        else:
            Liste = var.split('/')
            lastItem = Liste[-1]
            #~ print(lastItem) #
            Liste.pop()
            #~ print(Liste) #
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return (False, False)
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    #~ print("toto")
                    return (os.getcwd(), False) 
                except:
                    #~ print("tutu")
                    return (os.getcwd(), str(lastItem))  
            else:
                #~ print("titi")
                return (os.getcwd(), False, str(lastItem))   # changé par rapport à properPATH. On veut pouvoir créer un fichier, s'il n'existe pas.
    else:
        try:
            os.chdir(var)
            return (os.getcwd(), False)  
        except:
            if var in os.listdir():
                return (os.getcwd(), str(var))  
            else:
                return (False, False)   


def getURL(URL):
    ''' la même, en mieux.
    Renvoie str(data) si ok, False sinon.
    '''
    var = str(URL)
    data = False
    try:
        reponse = ulr.urlopen(var)
    except:
        return data
    data = reponse.read()
    return data


def formatText(rawData):
    ''' Le texte obtenu n'est pas dans le bon format.
    Retourne Le texte dans le format correct.
    '''
    var = str(rawData)[2:-3]
    #~ print(var[0:15], var[-20:-1])
    var = var.replace(r'\n', '\n').replace(r'\t', '\t')
    return var


def write2F(Data, PATH2file):
    ''' Écrit data dans PATH2file
    renvoie True si Ok, False sinon.
    '''
    data = str(Data)
    chemin = str(PATH2file)
    fullpath = properPATH2file(chemin)
    #~ print(PATH2file, chemin, fullpath)
    #~ print(len(fullpath))
    if len(fullpath) == 2:
        chemin, fichier = fullpath
    else:
        #~ print(len(fullpath))
        chemin, test, fichier = fullpath
        os.chdir(chemin)
        f = open(fichier, 'w')
        f.write(data)
        f.close()
        return True
    if chemin and fichier:
        a = input("Le fichier existe déjà, l'écraser ?? ").lower()
        if a == 'y' or a == 'yes' or a == 'ok' or a == 'oui' or a == 'o':
            os.chdir(chemin)
            f = open(fichier, 'w')
            f.write(data)
            f.close()
            print("Done.")
            return True
        else:
            return False
    elif chemin and not fichier:
        #~ print(fichier)
        fichier = input("Nom du fichier ? ")
        if fichier == "":
            return False
        if fichier in os.listdir(chemin):
            a = input("Le fichier existe déjà. l'écraser ? ")
            if a == 'y' or a == 'yes' or a == 'ok' or a == 'oui' or a == 'o':
                os.chdir(chemin)
                f = open(fichier, 'w')
                f.write(data)
                f.close()
                return True
            else:
                return False
        else:
            os.chdir(chemin)
            f = open(fichier, 'w')
            f.write(data)
            f.close()
            return True
    else:
        raise Exception('Not a valid PATH.')
        return False
    

def parseXMLheader(fichierIn, fichierOut):
    ''' Parser le fichier XML obtenu, et créer les strings correspondantes.
    Retourne True si Ok. False sinon.
    '''
    chemin = properPATH(fichierIn)
    print(chemin)
    if chemin[0] and chemin[1]:
        fr = open(str(chemin[0]) + '/' + str(chemin[1]), 'r')       # Ne pas oublier le '/'
        dico = {}
        chemin2 = properPATH(fichierOut)
        fw = open(str(chemin2[0]) + '/' + str(chemin2[1]), 'w')
        for i, line in enumerate(fr):
            regex1 = re.compile(r'<useragent description=')
            regex2 = re.compile(r'useragent=')
            if regex1.findall(line) and regex2.findall(line):
                #~ print(":", end = '')
                paires = line.split(r' useragent=')
                #~ print(len(paires), end = '')
                clef = paires[0].strip()[1:]
                valeur = paires[1].strip()[:-3]
                dico[clef] = valeur
                fw.write(clef)
                fw.write('§')
                fw.write(valeur)
                fw.write('\n')
            else:
                print(";", end='')
        fw.close()
        fr.close()
        return True
            


URL = "http://techpatterns.com/downloads/firefox/useragentswitcher.xml"
Data = getURL(URL)
Data = formatText(Data)
boolWritten = write2F(Data, "/tmp/azeffqdsf")
boolParse = parseXMLheader('/tmp/azeffqdsf', '/tmp/blabla')



