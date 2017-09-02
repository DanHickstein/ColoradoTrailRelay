from math import *
import sys, os, glob

open_files = 0
#open_files = 1

#directory = '/Users/danhickstein/Documents/elevation_profiles/10_Crested_Butte/'
directory = sys.argv[1]

def make_gnuplot_string(data_file_name, output_file_name, plot_title, max_elevation, min_elevation, distance):

	if max_elevation >= 10000:
		ylabel_offset = 4.6
	else:
		ylabel_offset = 3.6
	
	tic_interval = 1
	if distance > 10:
		tic_interval = 2
	if distance > 20:
		tic_interval = 5
	if distance > 70:
		tic_interval = 10
		
	
	gnuplot_instructions = """
	data_file_name = 	"{0}"
	output_file_name = 	"{1}"
	plot_title = 		"{2}"
	
	max_elev = 		{3}
	min_elev = 		{4}
	
	distance = 		{5}
	
	pix_per_ft = 	0.0799
	bottom_elev = 	1390
	
	set term postscript enhanced color size 2.63,1.00 font "UniversLTStd-Bold, 8" \\
	fontfile "/Users/danhickstein/Library/Fonts/UniversLTStd-Bold.pfa"\\
	fontfile "/Users/danhickstein/Library/Fonts/UniversLTStd-CnObl.pfa"\\
	fontfile "/Users/danhickstein/Library/Fonts/UniversLTStd-Cn.pfa" \\
	rounded #dl 0.05
	
	set output output_file_name
	
	set tics scale 0
	set border lw 0.35		lc rgb 'gray60'
	set grid front lw 0.70 lt 2 lc rgb 'gray60'
	set xtics font "UniversLTStd-Cn, 6" 	offset -0.2,0.4	tc rgb 'gray20'
	set xlabel font "UniversLTStd-Cn, 6" 	offset 0,1.1	tc rgb 'gray20'
	set ytics font "UniversLTStd-CnObl, 6"  	offset 0.45,0	tc rgb 'gray20'
	set ylabel font "UniversLTStd-CnObl, 6" 	offset {6},0	tc rgb 'gray20'
	set title plot_title 					offset 0,-0.7	tc rgb 'gray20'
	
	set lmargin 0; set rmargin 0; set tmargin 0; set bmargin 0
	
	set yrange[min_elev:max_elev]
	set y2range[(min_elev - bottom_elev)*pix_per_ft:(max_elev-bottom_elev)*pix_per_ft]
	set xlabel 'Distance (miles)'
	set ylabel 'Elevation (feet)'
	unset x2label
	
	set xrange [0:distance]
	
	set xtics {7},{7}
	
	plot '/Users/danhickstein/Documents/elevation_profiles/gradients/808x1045_00795pixperft.raw'\\
		binary array=(808,1045) flipy format='%uchar' with rgbimage axes x2y2 notitle,\\
		data_file_name using 1:2 smooth csplines with filledcurve below y1=max_elev lt rgb "white" notitle axes x1y1,\\
		data_file_name using 1:2 smooth csplines with line lt 1 lw 1  linecolor rgb "gray40" notitle axes x1y1
	""".format(data_file_name, output_file_name, plot_title, str(max_elevation), str(min_elevation), str(distance), str(ylabel_offset), str(tic_interval))
	
	return gnuplot_instructions
	
	


def find_min_max(file_name):
	file = open(file_name)
	print 'Scanning file: ' + file_name
	max_elevation = 0.0
	min_elevation = 30000.0
	distance = 0
	for line in file.readlines():
		if line[0] != '#' and line != '\n':
			elev = float(line.split()[1])
			dist = float(line.split()[0])
			if elev > max_elevation:
				max_elevation = elev
			if elev < min_elevation:
				min_elevation = elev
			if dist > distance:
				distance = dist
	

	max_ceil  = 500*ceil((max_elevation+50)/500.0)
	min_floor = 500*floor((min_elevation-300)/500.0)
		
	print ('Min: %0.2f, Max: %0.2f, Dist: %0.2f  -- Graph: %0.2F to %0.2f' % 
			(min_elevation, max_elevation, distance, min_floor, max_ceil) )
	
	return (min_floor, max_ceil, distance)
	

def modify_postscript(file_name):
	old_line = "/LT1 {PL [4 dl1 2 dl2] LC1 DL} def\n"
	new_line = "/LT1 {PL [0.01 dl1 1 dl2] LC1 DL} def\n"

	file = open(file_name,'r')
	lines = file.readlines()
	for index in range(0,len(lines)-1):
		if lines[index] == old_line:
			#print "Modified postscript file."
			lines[index] = new_line
	
	file.close()
	output_file = open(file_name,'w')
	for line in lines:
		output_file.write(line)
	output_file.close()
	
	
#directory = '/Users/danhickstein/Documents/elevation_profiles/elevation/correct size/'


for data_file_name in glob.glob( os.path.join(directory, '*.dat') ):
	#data_file_name = 'basalt.dat'
	data_file_name = os.path.basename(data_file_name)
	(min_elevation, max_elevation, distance) = find_min_max(os.path.join(directory,data_file_name))
	output_file_name = os.path.join(directory,data_file_name)[:-4] + '.ps'
	plot_title = data_file_name[:-4]
	
	gnuplot_file_name = directory + 'plot.txt'
	gnuplot_file = open(gnuplot_file_name,'w')
	gnuplot_file.write(make_gnuplot_string(directory + data_file_name, output_file_name, plot_title, max_elevation, min_elevation, distance))
	gnuplot_file.close()
	
	os.system('gnuplot \"' + gnuplot_file_name + '\"')
	
	modify_postscript(output_file_name)
	os.system('pstopdf \"' + output_file_name + '\"')
##	if open_files == 1:
##		os.system('open \"' + output_file_name[:-3] + '.pdf\"')



if open_files == 1:
	os.system('open ' + directory + '*.pdf')
	
	
