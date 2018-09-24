# Coveo DevOps Challenge
### Le défi
Ton défi, si tu l’acceptes, est de développer un outil permettant d’analyser la taille des ressources de stockage S3 d’un compte Amazon Web Services (AWS).
Afin de tester ton outil, tu peux te créer un compte gratuit sur [Amazon](http://aws.amazon.com/fr/free/) (si tu n’en as pas déjà un).
### Spécifications
L’outil doit se présenter sous forme d’une commande shell (Windows, Mac ou Linux) qui permet d’obtenir des informations sur l’ensemble des ressources [S3](https://aws.amazon.com/documentation/s3/) d’un compte Amazon.
##### L’outil doit permettre d’obtenir les informations suivantes:
- Nom du bucket
- Date de création
- Nombre de fichiers
- Taille totale des fichiers
- Dernière date de mise-à-jour

##### Les options suivantes doivent être supportées:
- Possibilité de sortir les résultats en octets, Kilooctets, Megaoctets, … ;
- Pouvoir sortir les informations par [type de stockage](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html) (Standard, IA, RR) ;
- Pouvoir spécifier une liste de buckets (bonus si support des expressions régulières) ;
- Pouvoir regrouper les informations par [régions](http://docs.aws.amazon.com/fr_fr/AWSEC2/latest/UserGuide/using-regions-availability-zones.html).

##### Idées de fonctionnalités supplémentaires
Il serait bien de pouvoir filtrer les fichiers considérés dans le calcul à l’aide d’un préfixe (ex: s3://mybucket/Folder/SubFolder/log*). Il est également utile de pouvoir filtrer ou organiser les résultats selon le [type d'encryption](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingEncryption.html), d’obtenir des informations supplémentaires sur les buckets (Life cycle, cross-region replication, etc.) ou de tenir compte des [versions précédentes](https://docs.aws.amazon.com/AmazonS3/latest/UG/enable-bucket-versioning.html) des fichiers (nombre + taille).

Des statistiques pour afficher le pourcentage de l’espace total occupé par un bucket ou toute autre bonne idée que tu pourrais avoir sont également les bienvenues.
### Plus d'informations
- Tu es libre d’utiliser le langage et le [SDK](https://aws.amazon.com/tools/) de ton choix ;
- Nous allons tester le fruit de ton travail sur notre environnement qui, soit dit en passant, contient des millions de fichiers. La performance globale de la solution proposée est donc à considérer ;
- Ton code doit être disponible à partir de n'importe quel gestionnaire de code source publique (tu peux faire un "fork" de notre challenge si tu veux).

## Conseils

- **Tente de créer ta solution comme si c'était du vrai code de production**. Montre nous comment tu crées du code propre et maintenable qui fait des choses incroyables. Construit quelque chose à laquelle nous serions heureux de contribuer. Ceci n'est pas un concours de programmation où les "hack" malpropres remportent la victoire.
- N'hésite pas à ajouter des fonctionnalités! Nous sommes curieux de voir ce à quoi tu peux penser. Nous nous attendrons à la même chose si tu travailles avec nous.
- La documentation et la maintenabilité est un plus.
- N'oublie pas les tests unitaires.
