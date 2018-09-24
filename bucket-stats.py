#!python3

# ---------------------------------------
# Bucket-stats est un script python permettant d'extraire des statistiques sur les buckets S3. 
# Il se base en partie sur les metriques de la supervision cloudwatch dans le but d'optimiser les performances.
# Ecrit par Nicolas Tremblier
# v1.0 - 2018-09-23
# ---------------------------------------

import boto3, datetime, sys, getopt, re
from operator import itemgetter
from table_logger import TableLogger

class buck: # Définition de la classe pour le bucket

	# prix au 22/09 sur la console AWS -> https://aws.amazon.com/fr/pricing/?nc2=h_ql_pr
	# Amélioration possible :  https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/index.json
	TARIFAWS = 0.023

	compteur = 0 # compte le nombre de buckets créés

	def __init__(self, s3bucket): # Constructeur
		buck.compteur = buck.compteur + 1
		self.nom = s3bucket.name 
		self.datecreation = s3bucket.creation_date
		self.taille = self.metriqueCloudwatch(s3bucket,"BucketSizeBytes", "StandardStorage") # appel à cloudwatch pour récupérer les stats
		self.nbreObj = self.metriqueCloudwatch(s3bucket,"NumberOfObjects", "AllStorageTypes") # appel à cloudwatch pour récupérer les stats
		
		try: # Récupération de la stratégie de chiffrement, sinon, non chiffré
			boto3.client('s3').get_bucket_encryption(Bucket=s3bucket.name)
			self.chiffre = True
		except:
			self.chiffre = False
		
		# Récupère les infos sur la région du bucket
		self.region = (boto3.client('s3').get_bucket_location(Bucket=s3bucket.name))['LocationConstraint'] # Récupère la région du bucket
		
		# calcul du cout du bucket, source en octets
		self.cout = round(self.taille / 1024**3 * self.TARIFAWS,2) 
				
		try: # Récupération de la stategie de réplication, sinon, non répliqué
			boto3.client('s3').get_bucket_replication(Bucket=s3bucket.name)
			self.replique = True
		except:
			self.replique = False

		# - Last modified date (most recent file of a bucket) / nécessite de passer tous les fichiers en revue
		def collObjInfo(self):
			s3obj = (boto3.client('s3')).list_objects_v2(Bucket=self.nom)
			
			if s3obj['KeyCount'] != 0:
				self.derniereMAJ = s3obj['Contents'][0]['LastModified']
				self.typeStockage = s3obj['Contents'][0]['StorageClass']
			 
		collObjInfo(self)
		self.publique = False # Récupère si le bucket est publié


	def __str__(self): #permet d'afficher le contenu de l'object via print
		return str(self.__class__) + ": " + str(self.__dict__)

	def __getitem__(self, key): #permet de récupérer les champ pour la fonction sorted
		if key == 'region':
			return self.region
		if key == 'typeStockage':
			return self.typeStockage

	def getSize(self, human=False): #retourne la taille en fonction de l'option utilisateur
		if human:
			return humanReadable(self.taille)
		else:
			return self.taille

	def metriqueCloudwatch(self, bucket, NomMetrique, stockage): 	# Méthode de collecte d'information dans cloudwatch
		cloudwatch = boto3.client('cloudwatch')
		now = datetime.datetime.now()
		try:
			cloudwatch_size = cloudwatch.get_metric_statistics(
				Namespace='AWS/S3',
				MetricName=NomMetrique,
				Dimensions=[
					{'Name': 'BucketName', 'Value': bucket.name},
					{'Name': 'StorageType', 'Value': stockage}
				],
				Statistics=['Maximum'],
				Period=86400,
				StartTime=(now - datetime.timedelta(days=1)).isoformat(),
				EndTime=now.isoformat()
			)
			if cloudwatch_size["Datapoints"]:
				return cloudwatch_size["Datapoints"][0]['Maximum']
			else:
				return 0
		except:
			return 0
		
def humanReadable(num, suffix='B'): # permet de convertir les octets en valeurs lisibles, à la façon de df
    for unit in ['','K','M','G','T','P']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def aide(): #Affiche l'aide en cas de mauvais paramètre ou à la demande
	print("Utilisation : bucket-stat [OPTIONS]")
	print("Affiche des renseignements sur les buckets AWS S3, par defaut")
	print("Arguments : \n\
	--help \t\t\t affiche cette aide.\n\
	--crypted-only \t\t n'affiche que les buckets chiffrés\n\
	-c, --csv \t\t ffiche le résultat en CSV\n\
	-s, --sorted \t\t groupe les résultats par region et groupe de stockage\n\
 	-h, --human-readable \t afficher les tailles dans des puissances de 1024 (par exemple 1023M)\n\
	-f, --filter=FILTRE \t filtre la liste des buckets sur la base de l'expression regulière FILTRE") 
			

# ---------------------------------------
# Partie principale du script
# ---------------------------------------

def main():
	
	csv=False
	human = False
	grouper = False
	filtreCrpt = False
	filtre = None
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "shcf:", ["sorted", "help", "csv", "human-readable", "crypted-only", "filter:"])
	except:
		# print help information and exit:
		print("Commande incorrecte, voici l'aide : ")
		aide()
		sys.exit(2)

	for opts, args in opts:
		if opts == "--help":
			aide()
			sys.exit()
		elif opts == "--crypted-only":
			filtreCrpt = True
		elif opts in ("-c", "--csv"):
			csv = True
		elif opts in ("-s", "--sorted"):
			grouper = True
		elif opts in ("-h", "--human-readable"):
			human = True
		elif opts in ("-f", "--filter"):
			if len(args):
				filtre = args
			else:
				aide()
				sys.exit(2)
		
	s3 = boto3.resource('s3')
	bucks = [] # Tableau d'objet de tous les buckets de l'organisation

	listeS3Bucks = s3.buckets.all()
	for bucket in listeS3Bucks:
		try:
			if filtre:
				re.match(filtre,"Chaine de test")
		except:
			print("Erreur d'expression régulière")
			sys.exit(2)

		if (filtre and re.match(filtre,bucket.name)) or not filtre:
			try:
				bucks.append(buck(bucket)) # Création de l'objet et insertion dans le tableau
			except:
				print("Erreur lors de la connexion à AWS, merci de vérifier votre parametrage")
				print("Pour plus d'information : https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html")
				sys.exit(2)

	if grouper: #si l'option de grouper  activée, on reclasse le tableau par région et par type de stockage
		bucks = sorted(bucks, key=itemgetter('region'))
		bucks = sorted(bucks, key=itemgetter('typeStockage'))
		
	# Utilisation de Table-Logger pour l'affichage : https://github.com/AleksTk/table-logger/tree/master/table_logger
	tbl = TableLogger(columns='Nom,Date de Création,Dernière MaJ,Taille,Nombre d\'objets,Chiffré,Stockage,Publique,Région,Cout,Répliqué',
		csv=csv, border=False) 
		
	for cBuck in bucks:
		if (filtreCrpt and cBuck.chiffre) or not filtreCrpt:
			tbl(cBuck.nom, cBuck.datecreation, cBuck.derniereMAJ, cBuck.getSize(human), str(cBuck.nbreObj), 
			cBuck.chiffre,cBuck.typeStockage, cBuck.publique, cBuck.region, "$"+str(cBuck.cout),cBuck.replique)
		
if __name__ == "__main__":
	main()