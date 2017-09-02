import os
import glob, sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
 
 
 
 
def make_plot(ax,infile,show=False):
	print 'Infile: ' + infile
	data = np.loadtxt(infile)
	distance = data[:,0]
	elevation = data[:,1]
	m=len(elevation); q = m+np.sqrt(2*m)
	tck = scipy.interpolate.splrep(distance,elevation,s=20*q)
	dist = np.linspace(distance.min(),distance.max(),500)
	elev_smooth = scipy.interpolate.splev(dist,tck,der=0)
	print elev_smooth
	#plt.plot(distance,elevation,color='r')
	ax.plot(dist,elev_smooth,color='b',lw=4)
	ax.fill_between(dist,elev_smooth,alpha=0.1)
	
	ax.set_xlim(0,distance.max())
	
	top  = 500*np.ceil((elev_smooth.max()+50)/500.0)
	bottom = 500*np.floor((elev_smooth.min()-300)/500.0)
	ax.set_ylim(bottom,top)
	
	ax.set_title(os.path.basename(infile)[:-4])
	ax.set_xlabel('Distance (miles)')
	ax.set_ylabel('Elevation (feet)')
	



	
	
 
 


# make_plot('/Users/danhickstein/Documents/Elevation_profiles/Aug 14 - Individual Legs/Leg B01 - Shinglemill.dat', 
#			  show=True)

# show_plots = 0
# #show_plots = 1
# 
# #path = sys.argv[1]
# 
path = "/Users/danhickstein/Documents/Elevation_profiles/Aug 14 - Individual Legs"

for infile in glob.glob( os.path.join(path, '*.dat') ):
	fig = plt.figure(figsize=(8,4))
	ax	= fig.add_subplot(111)
	print "Current file is: " + infile
	outfile = infile[:-4] + '.gif'
	make_plot(ax,infile,outfile)
	fig.subplots_adjust(bottom=.13)
	plt.savefig(outfile,dpi=200)

plt.show()
	