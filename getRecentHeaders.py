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
            print(lastItem) #
            Liste.pop()
            print(Liste) #
            for i in Liste:
                try:
                    os.chdir(str(i))
                except:
                    return (False, False)
            if lastItem in os.listdir():
                try:
                    os.chdir(str(lastItem))
                    print("toto")
                    return (os.getcwd(), False) 
                except:
                    print("toto")
                    return (os.getcwd(), str(lastItem))  
            else:
                print("Fuck")
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


def write2F(Data, PATH2file):
    ''' Écrit data dans PATH2file
    renvoie True si Ok, False sinon.
    '''
    data = str(Data)
    chemin = str(PATH2file)
    fullpath = properPATH2file(chemin)
    print(PATH2file, chemin, fullpath)
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
        a = input("Le fichier existe déjà, l'écraser ?").lower()
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
        print(fichier)
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


URL = "http://techpatterns.com/downloads/firefox/useragentswitcher.xml"
Data = getURL(URL)
boolWritten = write2F(Data, "/tmp/azeffqdsf")


