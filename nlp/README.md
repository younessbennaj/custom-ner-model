# Travel Order Resolver

Ce dépot contient un résolveur d'itinéraire qui en fonction d'un ordre de trajet donné en entré peut donner en sortie l'itinéraire approprié. 

## Installation 

Le résolveur d'itinéraire requière l'utilisation d'autres programmes pour fonctionner. Il faut donc débuter par l'installation de ces derniers. 

### Python 3  

+ Pour les utilisateurs de Windows ou de Mac, télécharger Python 3 (https://www.python.org/downloads/) puis l'installer.

+ Pour les utilisateurs de Linux, dans votre terminal il faut exécuter ```sudo apt update``` puis ```sudo apt install python3 python3-pip```.

### Bibliothèques Python

Dans la conception de ce résolveur, nous avons eu besoin d'utiliser des fonctionnalités supplémentaires qui ne se trouvent pas dans la version de base de Python. Nous avons donc eu recours à plusieurs bibliothèques: 

+ ```csv``` pour travailler avec les documents au format csv (datasets)
+ ```re``` pour travailler avec les chaines de caractères
+ ```pathlib``` pour utiliser le système de fichier de la machine
+ ```spacy``` c'est la bibliothèque de NLP qui va nous permettre de concevoir et d'entrainer notre model de NER custom pour répondre à notre problématique spécifique.
+ ```json``` pour utiliser et convertir nos données au format JSON
+ ```difflib``` pour calculer la probabilité de ressemblance entre deux chaines de caractères
+ ```pandas``` pour travailler avec des dataframes

Il faut donc télécharger puis installer ces bibliothèques. 

```
pip3 install -r requirements.txt
```

### Utilisation 

Pour utiliser le code, déplacez vous dans le dossier: 

```
cd travel-order-resolver 
```

Puis vous pouvez utiliser la commande suivante pour éxectuer le fichier principal du projet:

```
python3 main.py
```