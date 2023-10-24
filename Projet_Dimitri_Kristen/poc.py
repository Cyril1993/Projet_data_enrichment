import pandas as pd
import numpy as np

# load of data.gouv data into dataframe
data_geo = pd.read_csv("Ressources/StockEtablissementActif_utf8_geo.csv", low_memory=False)

# selecting columns of interest and transfor
x = data_geo[["siret","latitude","longitude","codePostalEtablissement","numeroVoieEtablissement","typeVoieEtablissement",
              "libelleVoieEtablissement","libelleCommuneEtablissement",
             "geo_adresse"]]
x.rename(columns={'siret': 'Numéro SIRET'}, inplace=True)
x['latitude']=x['latitude'].round(4)
x['longitude']=x['longitude'].round(4)

data_client = pd.read_excel("Ressource/Données réponses fournisseurs.xlsx")
y = data_client[["Numéro SIRET","Nom du site ou de l’agence (nom d’usage)","Adresse (du site)","Code postal (du site)",
                 "Ville (du site)",'Etat/Département','Coordonnées GPS : latitude','Coordonnées GPS : longitude']]

list_a_supprimer =['841 156 888 00015','SE556193413301','3303355712223Z','385\xa0163\xa0191 00047','478 334 576 00038',
                  'RC B 46483','A81604464','B98276230','8527979350002B','faquesiret','0405 414 072', np.NaN,'47774653100029 ape 8899b']
y_clean = y[~y['Numéro SIRET'].isin(list_a_supprimer)]
y_clean=y_clean.drop(0)

y_clean['Coordonnées GPS : latitude'] = pd.to_numeric(y_clean['Coordonnées GPS : latitude'], errors='coerce')
y_clean['Coordonnées GPS : longitude'] = pd.to_numeric(y_clean['Coordonnées GPS : longitude'], errors='coerce')
y_clean['Numéro SIRET'] = y_clean['Numéro SIRET'].astype(int)
y_clean['Code postal (du site)'] = y_clean['Code postal (du site)'].str.replace(r'[\s\_\-]', '', regex=True)
y_clean['Ville (du site)'] = y_clean['Ville (du site)'].str.replace(r'^\s+|\s+$', '', regex=True)

y_clean_filtered = y_clean[y_clean['Numéro SIRET'].isin(x['Numéro SIRET'].tolist())]

test = pd.merge(y_clean_filtered, x, on='Numéro SIRET')

test['CodePostalEgaux']= test['Code postal (du site)']==test['codePostalEtablissement']

print(test.head(20))

chemin_du_fichier_excel = 'Resultats/test.xlsx'

test.to_excel(chemin_du_fichier_excel, index=False)
