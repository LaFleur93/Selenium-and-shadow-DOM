import pandas as pd
from datetime import *

def missed_planting(d):
	#2023-01-21
	day = date(int(d[0:4]), int(d[5:7]), int(d[8:10]))

	date_14 = day + timedelta(days=-14)
	week_14 = date_14.isocalendar().week

	date_21 = day + timedelta(days=-21)
	week_21 = date_21.isocalendar().week

	week_14 = 'W'+str(week_14).zfill(2)
	week_21 = 'W'+str(week_21).zfill(2)

	weeks = [week_14, week_21]

	missing = []

	herbs_dict = {'pr26': 'Flat Parsley_2x18cc', 'pr21': 'Curly Parsley_33cc_3weeks', 'tm5': 'Thyme_33cc 3Week Acre', 'cr26': 'Flat Coriander_33cc CPH', 'rs4': 'Rosemary_33cc CPH', 'mn24': 'Green Mint_33cc CPH', 'mn25': 'Green Mint_33cc CPH', 'sg2': 'Sage_33cc', 'bs49': 'Italian Basil_33cc CPH', 'dl6': 'Dill_33cc CPH', 'di6': 'Dill_33cc CPH'}
	pots_dict = {'bs49': 'Pots_Italian Basil_2x33cc CPH_Bs105', 'bs105': 'Pots_Italian Basil_2x33cc CPH_Bs105', 'cr26': 'Pots_Flat Coriander_2x33cc CPH', 'tm5': 'Pots_Thyme_2x33cc CPH', 'mn24': 'Pots_Green Mint_2x33cc CPH', 'mn25': 'Pots_Green Mint_2x33cc CPH', 'rs4': 'Pots_Rosemary_2x33cc CPH', 'che9': 'Pots_Chervil_2x33cc CPH', 'wtc2': 'Pots_Watercress_2x33cc CPH', 'mls5': 'Pots_Melissa_2x33cc CPH', 'or17': 'Pots_Oregano_2x33cc', 'pr26': 'Pots_Flat Parsley_2x33cc CPH', 'pea3': 'Pea Tops - Early Harvest', 'bs49 - test': 'Pots_Italian Basil_2x33cc CPH_Bs105'}

	for week in weeks:

		missed_planting_id, sheet_name = '1azyJv6WsCrQ5mQ2Z0V9R_JQOWz8wtzWi-cro2nlcYuw', week

		url = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(missed_planting_id, sheet_name)

		# Dataframe Missed Planting
		df_missed_planting = pd.read_csv(url)
		df_missed_planting = pd.DataFrame(df_missed_planting)
		df_missed_planting = df_missed_planting.to_numpy()

		search_date = d[8:10]+'.'+d[5:7]+'.'+d[0:4]
		
		if int(week[1:]) >= 4:
			col_extra = 16
		else:
			col_extra = 15

		for i in range(len(df_missed_planting)):
			if df_missed_planting[i][6] == search_date:
				if df_missed_planting[i][4]*30 == df_missed_planting[i][5]:
					if type(df_missed_planting[i][1]) == float:
						continue
					else:
						missing.append(df_missed_planting[i][3])
						missing.append(herbs_dict[df_missed_planting[i][1].lower()])
						missing.append(df_missed_planting[i][5])
				else:
					if type(df_missed_planting[i][1]) == float:
						continue
					else:
						missing.append(df_missed_planting[i][3])
						missing.append(pots_dict[df_missed_planting[i][1].lower()])
						missing.append(df_missed_planting[i][5])

	missing = [[missing[i], missing[i+1], str(missing[i+2])] for i in range(0, len(missing), 3)]

	return missing

#print(missed_planting('2023-03-15'))