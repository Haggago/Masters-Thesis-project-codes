# Version 1.0.            Mohammed El-Sayed                                      
# Copyright (c) 2019      Potsdam university 
# Fisher forecast Matrix approach                     
# execute fisher.c code(by Cullan Howllet:https://github.com/CullanHowlett/PV_fisher) on a set of survey parameters
# to determine the expected value of fsigam8 (and it's error) for each of the surveys.

import subprocess
import glob

pv_fisher_exe		= "./PV_new"
example_file_dir 	= "/home/hegoo/PV_fisher-master/example_files"
res_dir 			= "./results1"

# --- define parameter space grid --- #

pv_dist_errs	= [0.03, 0.05, 0.1, 0.15, 0.2, 0.3]
k_maxs			= [0.05, 0.1, 0.15, 0.2]
with_rsd 		= [True, False]
sky_dists		= [ 0.5, 1, 2, 3, 4]#[0.1, 0.33, 0.57, 1.57, 3]
#sample_sizes	= [397, 1191, 1377, 2357, 3970, 4131, 6560, 7071, 12500, 13770, 19680, 23570, 37500, 65600, 125000]
sample_sizes	= [756, 1531, 2268, 2920, 4593, 7560, 8760, 15310, 29200]
nparams			= [1, 2, 3, 4, 5]#(0=β, 1=fσ8, 2=rg, 3=σg, 4=σu)
#z_maxs			= [0.0125, 0.05, 0.08, 0.1, 0.15]




#z_maxs			= [0.08, 0.1, 0.15]


pv_dist_errs	= [0.05]
k_maxs			= [0.2]
with_rsd 		= [False]
sky_dists		= [3]
sample_sizes	= [4593]
nparams			= [5]

# --- functions --- #

def find_sample_size_file(sample_size, file_dir=example_file_dir):
	"""
		look into file dir for the file corresponding
		to a given sample size.
	"""
	
	# look for all the files matching the naming scheme
	files = glob.glob(example_file_dir+"/*example_nbar_vel.dat")
	
	# look for the file with the right sample size
	for f in files:
		# extract the sample size number from the file name
		ss_from_file = int(f.split('/')[-1].replace("example_nbar_vel.dat", ""))
		# match it to given sample size
		if ss_from_file == sample_size:
			print ("found file %s for sample size %d"%(f, sample_size))
			return f
			
	# raise error if match fails
	print ("for sample size %d"%sample_size)
	print ("found files: %s"%repr(files))
	raise RuntimeError(
		"Can't match example file to sample size! Look into %s"%file_dir)
#repr(outf)
def find_rsd_file(with_rsd):
	"""
		return the right RSD file if you want to include this
		effect or not.
	"""	
	out = None
	if with_rsd:
		out = example_file_dir+"/example_nbar_red.dat"
	else:
		out = example_file_dir+"/RSD0.dat"
	print ("for with_rsd %s found file: %s"%(with_rsd, out))
	return out

def run_for_set_of_parameters(pv_dist_err, sample_size, k_max, w_rsd, sky_dist, nparam):
	"""
		for a set of 5 parameters, determine (zeff, fsigma8(zeff), percentage_err(zeff))
		- create sample from simsurvey code
		- rest fisher paramters
		- read output
		- save result to table file   
	"""
	
	print ("PV dist err: %f"%pv_dist_err)
	print ("Max wavenumber: %f"%k_max)
	print ("With RSD: %s"%w_rsd)
	print ("Sky distribution: %f"%sky_dist)
	print ("Sample size: %d"%sample_size)
	print ("The number of free parameters: %d"%nparam)

	# look for the example file
	example_file = find_sample_size_file(sample_size)
	rsd_file = find_rsd_file(w_rsd)
	
	# FIXME: let's use the file that works for now
	#example_file = "../example_files/example_nbar_vel_ORIGINAL.dat"
	
	print ("--- now running C code ---")
	# build up the command:
	# syntax is:
	# 	- error_dist		= strtod(argv[1], NULL);		// change pv distance error
    # 	- survey_area[2]	= strtod(argv[2], NULL);		// change survey area overlap
    #	- zmax			= strtod(argv[3], NULL);		// change max redshift
    
    #	- nbar_file[0] 	= argv[4];						// change sample size file
    #	- nbar_file[1] 	= argv[5];						// change RSD file
	#cmd = pv_fisher_exe + " %f %f %f %f %s %s"%(
	#	pv_dist_err, sky_dist, k_max, nparam, example_file, rsd_file)
	#import os
	#os.system(cmd)
	#return
	
	# create a list of the arguments to be passed to the executable
	args = [str(p) for p in [pv_dist_err, sky_dist, k_max, nparam, example_file, rsd_file]]
	
	# run the command
	proc = subprocess.Popen(
		[pv_fisher_exe]+args, 
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE,
		universal_newlines=True)
	out, err = proc.communicate()
	exitcode = proc.returncode
	print (out, err)
	
	# create table file and save stuff there
	#outfile = res_dir+'/fisher_pverr%.2f_skyd%.2f_K_max%.3f_nparm%.2f_ns%d_w_rsd%d.csv'%(
		#pv_dist_err, sky_dist, k_max, nparam, sample_size, w_rsd)
	#with open(outfile, 'w') as outf:
		#outf.write("# running with sample size: %d\n"%sample_size)
		#outf.write("# running with RSD: %s\n"%w_rsd)
		#outf.write(out)
		#outf.write(err)
	#print ("results saved to %s"%outfile)
	

# --- loop over survey parameters --- #
grid_p = 0
for pv_dist_err in pv_dist_errs:
    for k_max in k_maxs:
          for w_rsd in with_rsd:
                for sky_dist in sky_dists:
                        for sample_size in sample_sizes:
                            for nparam in nparams:
                                 print ("---- grid point # %d ----"%grid_p)

                                 run_for_set_of_parameters(
                                                         pv_dist_err=pv_dist_err, 
                                                         k_max=k_max,
                                                         sample_size=sample_size, 
                                                         sky_dist=sky_dist,
                                                         w_rsd=w_rsd,
                                                         nparam=nparam)


                                 grid_p += 1
#input()

		#for z_max in z_maxs:


