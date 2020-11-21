#Traitemnt de fichier et repertoires
import sys
import os
#Expression régulière
import re
#Traitement de caractères Unicode
import unicodedata
#Mots vides NLTK français
from nltk.corpus import stopwords
# lemmatiseur français
from nltk.stem.snowball import FrenchStemmer

#---------------------Fonctions-----------------------------------------

#Convertire une chaine de caractère Unicode en sa représentation ascii (élimination des accents ..)
def unicodeToAscii(word) :
    unicode_string = unicodedata.normalize('NFKD', word).encode('ascii','ignore')
    ascii_string = unicode_string.decode("utf-8")
    return ascii_string

#Nettoyage d'un docmument
def clean(docName):

    #Liste qui va contenit les mots vide à éliminer
    stopWords = []

    # la liste des mots vides de nltk
    stop_words_nltk = stopwords.words('french')

    # convertir tous les mots de la liste vide de unicode vers code ascii
    for word in stop_words_nltk :
        converted_word = unicodeToAscii(word)
        stopWords.append(converted_word)

##    # notre propre fichier contenant 398 mots vides
##    file_mots_vides = open('liste mots vides.txt','rU', encoding='utf-8')
##
##    for word in file_mots_vides :
##        #enlever le saut de ligne à la fin du mot
##        word = re.sub(r'\n+','', word)
##        # convertir tous les mots de la liste vide du unicode vers code ascii
##        word = unicodeToAscii(word)
##        # Ajouter le mot à la liste des mots vides
##        if word not in stopWords:
##            stopWords.append(word)
##
##    # fermer le fichier des mots vides
##    file_mots_vides.close()

    # une liste contenant tout les signes de ponctuations
    listPonct = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '\\','}','l\'','d\'','/','*','-','+','=']


    #Ouverture du document à nettoyer
    document = open(docName,'rU')
    # lire le ficheir en entrée
    text = document.read()
    # convertir le texte en des mots minuscule
    text = text.lower()

    # supprimer les caractères non alphanumériques
    i = 0
    while (i < len(text)) :
        if not (text[i].isalpha()):
            if (text[i] in listPonct) :
                text = text.replace(text[i], " ")
            else :
                # remplacer le caractère ø par un vide
                text = text.replace('ø', " ")
        i = i + 1

    # découper le texte en des mots dans une liste
    textSplit = text.split()
    #List qui va contenir les mots nettoyé
    cleanWords = []

    for word in textSplit :
        # vérifier si le mot n'appartient pas à la liste des mots vides
        if word not in stopWords and not (word.isdigit()):
        # insérer le mot dans la liste des mots
            cleanWords.append(word)

    #List temporaire qui va contenir le traitement de certains des cas spéciaux
    tempList = []
    # on parcourt la liste des mots
    for word in cleanWords :
    # remplacer le caractère œ par un oe
        if ('œ' in word):
            word = re.sub(r'œ', 'oe', word)
        tempList.append(word)
    
    cleanWords = tempList
    document.close()
    
    var = os.path.basename(docName).split(".")
    if not os.path.exists("Clean"):
        os.makedirs("Clean")
    nomFichNettoy = "Clean/"+var[0]+'_Clean.txt'
    # ouvrir le fichier de sortie en mode écriture
    f = open(nomFichNettoy,'w', encoding = "utf-8")

    listMots = []
    nvlChaine = " "
    for word in cleanWords :

    # convertir tous les mots de la liste des mots du unicode vers code ascii
        txt = unicodeToAscii(word)
    # remplacer les sauts de lignes, les espaces multiples et les mots contenant des chiffres
    # de chaque mot de la liste par un espace
        txt = re.sub(r'\\n', '', txt)
        txt = re.sub(r'\s\s+', ' ', txt)
        txt = re.sub(r'(\w[0-9])', '', txt)
        txt = re.sub(r'(\w[0-9]\w)', '', txt)
        txt = re.sub(r'([0-9]\w)', '', txt)
#
    # remplir une nouvelle liste des mots après nettoyge
        listMots.append(txt)
    # appel de stemmer
    stemmer = FrenchStemmer()

    # de chaque mot de la liste des mots nettoyée
    for word in listMots :
    # lemmatiser les mots de la liste des mots
        word = stemmer.stem(word)
    # retourner le résultat dans une chaine de caractère
        nvlChaine += "".join(word)
        nvlChaine += " "

    # écrire le résultat dans un fichier de sortie
    f.write(nvlChaine)  # Stored on disk as UTF-8
    f.close()

    # réouvrir le fichier de sortie en mode écriture
    f = open(nomFichNettoy,'r', encoding = "utf-8")
    listMotNettoy = f.read().split()

    #Retourne un dictionnaire des mots du document qui sera utilisé dans la classification
    dictFile = {}
    for word in listMotNettoy :
        dictFile[word] = True

    f.close()

    return dictFile
#clean("2.txt")
