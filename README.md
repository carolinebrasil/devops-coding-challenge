# bucket-stat 

Bucket-stats est un script python permettant d'extraire des statistiques sur les buckets S3. Il se base sur les metriques de la supervision cloudwatch.

## Installation

> Prérequis :
> - python3
> - python3-pip
> - git
> - Un compte AWS configuré sur la machine : [documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

### Cloner le dépôt

```$ git clone https://github.com/zk1ppy/devops-coding-challenge.git```

### Installer les prérequis python

```$ python3 -m pip install -r requirements.txt```

## Utilisation

Le script peut-être appelé sans paramètre pour afficher les informations standards :
- Nom du bucket
- Date de création
- Nombre de fichiers
- Taille totale des fichiers
> - Dernière date de mise-à-jour

Exemples :

```shell
$ python3 bucket-stats.py
Nom                  Date de Création    Dernière MaJ                      Taille Nombre d'objets      Chiffré              Stockage             Publique             Région               Cout                 Répliqué            
testcoveodevops      2018-09-22 10:37:18 2018-02-16 22:32:16          3253.000000 2.0                  True                 STANDARD             False                eu-west-3            $0.0                 True                
testcoveodevops2     2018-02-18 21:16:29 2018-02-18 21:19:03          2722.000000 1.0                  False                STANDARD             False                eu-west-3            $0.0                 False               
testcoveodevopsrepl  2018-09-22 10:13:49 2018-09-22 12:56:05             0.000000 0                    False                STANDARD             False                eu-west-2            $0.0                 False               

```

```shell
$ python3 bucket-stats.py -h -f "^.*2$"
Nom,Date de Création,Dernière MaJ,Taille,Nombre d'objets,Chiffré,Stockage,Publique,Région,Cout,Répliqué
testcoveodevops2,2018-02-18 21:16:29,2018-02-18 21:19:03,2.7KB,1.0,False,STANDARD,False,eu-west-3,$0.0,False
```

## Utilisation

Utilisation : bucket-stat [OPTIONS]

Affiche des renseignements sur les buckets AWS S3, par defaut

Arguments :

--help 			 affiche cette aide.

--crypted-only 		 n'affiche que les buckets chiffrés

-c, --csv 		 ffiche le résultat en CSV

-s, --sorted 		 groupe les résultats par region et groupe de stockage

 -h, --human-readable 	 afficher les tailles dans des puissances de 1024 (par exemple 1023M)

-f, --filter=FILTRE 	 filtre la liste des buckets sur la base de l'expression regulière FILTRE