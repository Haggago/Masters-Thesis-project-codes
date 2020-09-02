# Version 1.0.            Mohammed El-Sayed                                      
# Copyright (c) 2019      Potsdam university                      
# read result tables from PV fischer.c code (by Cullan Howllet:https://github.com/CullanHowlett/PV_fisher) 
import csv
import glob
import pandas as pd


res_dir 			= "./results_new_2904"

def get_pars_from_table(table):
	"""
		read the Full redshift range values of
		zeff, fsigma8(z_eff), percentage error(z_eff)
		from the files produced by the fischer code.
	"""
	
	print ("reading results from file: %s"%table)
	out = {}
	with open(table, 'r') as tab:
		
		lines = tab.readlines()
		out['n_sample'] = float(lines[0].split(":")[-1].strip())
		if lines[1].split(":")[-1].strip() == "False":
			out['w_rsd'] = False
		else:
			out['w_rsd'] = True            
		print(lines[1].split(":")[-1].strip())
		print(bool(lines[1].split(":")[-1].strip()))
		out['pv_d_error'] = float(lines[2].split(":")[-1].strip())
		out['sky_area'] = float(lines[3].split(":")[-1].strip())
		#out['zmax'] = float(lines[4].split(":")[-1].strip())
		out['k_max'] = float(lines[4].split(":")[-1].strip())
		out['free_paramters'] = float(lines[5].split(":")[-1].strip())

	
		last_line = lines[-1]
		pieces = [p.strip() for p in last_line.strip().split(" ") if p not in ['']]
		out['zeff'] = pieces[-3]
		out['fsigma8'] = pieces[-2]
		out['%error'] = pieces[-1]
		#print (repr(out))
	return out

# read all the tables, save average values of parameters
tables = glob.glob(res_dir+"/fisher*.csv")
print ("found %d table files in %s"%(len(tables), res_dir))
results = []
for table in tables:
	out = get_pars_from_table(table)
	results.append(out)
	
#save the extracted results into one big table
#outfile = "global_taibresult.csv"
outfile = "global_Magnitudes_result.csv"
df = pd.DataFrame(results)
print (df)
df.to_csv(outfile, index=False)
print ("saved results to %s"%outfile)




