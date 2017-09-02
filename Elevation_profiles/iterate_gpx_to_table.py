import os
import glob, sys
 
 
show_plots = 0
#show_plots = 1

#path = '/Users/danhickstein/Documents/elevation_profiles/10_Crested_Butte'
path = sys.argv[1]



for infile in glob.glob( os.path.join(path, '*.GPX') ):
	print "current file is: " + infile
	outfile = infile[:-4] + ".dat"
   	os.system('python gpx_to_table.py -E \"' + infile + '\" > \"' + outfile + '\"' )
	#print 'echo \"plot \\"' + outfile + '\\" using 2:1 w l\" | gnuplot -persist'
	if show_plots == 1:
		os.system('echo \"plot \\"' + outfile + '\\" using 1:2\" | gnuplot -persist')
