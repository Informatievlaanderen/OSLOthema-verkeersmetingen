import pandas as pd
import openpyxl
from openpyxl import load_workbook
import xlrd
from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

dataframe = load_workbook('codelists.xlsx')

languages = ["en", "fr", "de"]

# Define filepath
filepath = 'codelists.xlsx'

# Load Excel file using Pandas
f = pd.ExcelFile(filepath)


# Define an empty list to store individual DataFrames
list_of_dfs = []
list_of_sheets = []

# Iterate through each worksheet
for sheet in f.sheet_names:

    # Parse data from each worksheet as a Pandas DataFrame
    df = f.parse(sheet)

    # And append it to the list
    list_of_dfs.append(df)
    list_of_sheets.append(sheet)



# Combine all DataFrames into one
data = pd.concat(list_of_dfs, ignore_index=True)



text = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \n"
text = text + "@prefix skos: <http://www.w3.org/2004/02/skos/core#> . \n"

text = text + "\n"

#for i in range(len(list_of_sheets)):
#    print(list_of_sheets[i])

sheet = 1

text = text + "<https://data.vlaanderen.be/id/conceptscheme/" + \
    str(list_of_sheets[sheet].replace(" ", "_")) + ">  a skos:ConceptScheme ; \n"
text = text + "<https://www.w3.org/ns/adms#status> <https://wegenenverkeer.data.vlaanderen.be/id/concept/VkmStatus/ingebruik > ; \n"
text = text + "\n"

text = text + 'skos:prefLabel "' + str(list_of_dfs[sheet]["Label"][0]) + '"@nl ; \n'
text = text + 'skos:definition "' + \
    str(list_of_dfs[sheet]["Definitie"][0]) + '"@nl ; \n'



for i in range(len(list_of_dfs)-1):
    i = i+1
    text = text + "<https://data.vlaanderen.be/id/conceptscheme/" + \
        str(list_of_dfs[sheet]["Klasse"][i]) + ">  a skos:Concept ; \n"
    text = text + "<https://www.w3.org/ns/adms#status> <https://wegenenverkeer.data.vlaanderen.be/id/concept/VkmStatus/" + str(list_of_dfs[sheet]["Status"][i]) +" > ; \n"
    
    text = text + 'skos:definition "' + \
        str(list_of_dfs[sheet]["Definitie"][i]) + '"@nl ; \n'
        
    text = text + 'skos:inscheme "' + \
        str(list_of_dfs[sheet]["Definitie"][i]) + '"@nl ; \n'

    
    for language in languages:
        text = text + 'skos:definition "' + \
            translator.translate(
                str(list_of_dfs[sheet]["Definitie"][i]), dest=language).text + '"@' + language + ' ; \n'
        text = text + 'skos:prefLabel "' + \
            translator.translate(
                str(list_of_dfs[sheet]["Label"][i]), dest=language).text + '"@' + language + ' ; \n'
        

    text = text + 'skos:inscheme <https://data.vlaanderen.be/id/conceptscheme/' + \
        str(list_of_sheets[sheet].replace(" ", "_")) + '>'
    text = text + 'skos:notation "' + str(list_of_dfs[sheet]["Notation"][i]) + '" ; \n'
    text = text + 'skos:prefLabel "' + \
        str(list_of_dfs[sheet]["Label"][i]) + '"@nl ; \n'
    
    text = text + 'skos:topConceptOf <https://data.vlaanderen.be/id/conceptscheme/' + \
        str(list_of_sheets[sheet].replace(" ", "_")) + '> . \n'

    text = text + "\n"

print(text)


with open('VkmMeettechnieken.ttl', 'w') as f:
    f.write(text)
    

