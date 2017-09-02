import os
import glob, sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

 
 
def make_plot(ax,infile,count=0,show=False,cum_dist=0):
	print 'Infile: ' + infile
	print cum_dist
	data = np.loadtxt(infile)
	distance = data[:,0]
	elevation = data[:,1]
	m=len(elevation); q = m+np.sqrt(2*m)
	tck = scipy.interpolate.splrep(distance,elevation,s=20*q)
	dist = np.linspace(distance.min(),distance.max(),500)
	elev_smooth = scipy.interpolate.splev(dist,tck,der=0)
	#plt.plot(distance,elevation,color='r')
	dist=dist+cum_dist
	
	ax.plot(dist,elev_smooth,color='b',lw=3)
	print 'count: ',
	print count
	if count%2 == 0:
	    print 'even'
	    alph = 0.05
	else: 
	    print 'odd'
	    alph = 0.15
	ax.fill_between(dist,elev_smooth,alpha=alph)
		
	top  = 500*np.ceil((elev_smooth.max()+50)/500.0)
	bottom = 500*np.floor((elev_smooth.min()-300)/500.0)
	
	ax.text((dist.max()+dist.min())/2,6500,str(count))
	
	return distance.max()

	

	



	
	
 
 


# make_plot('/Users/danhickstein/Documents/Elevation_profiles/Aug 14 - Individual Legs/Leg B01 - Shinglemill.dat', 
#			  show=True)

# show_plots = 0
# #show_plots = 1
# 
# #path = sys.argv[1]
# 
path = "/Users/danhickstein/Documents/Elevation_profiles/Aug 14 - Individual Legs"
fig = plt.figure(figsize=(8,4))
ax	= fig.add_subplot(111)
ax.set_ylim(6000,12500)
ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Elevation (feet)')
ax.set_title('Colorado Trail Relay!')

count = 1
cum_dist = 0

for infile in glob.glob( os.path.join(path, '*.dat') ):
    
	print "Current file is: " + infile
	outfile = infile[:-4] + '.gif'
	cum_dist = cum_dist + make_plot(ax,infile,count=count,cum_dist=cum_dist)
	count = count + 1
	fig.subplots_adjust(bottom=.13)
	

ax.set_xlim(0,cum_dist)
plt.savefig('Whole trail.png',dpi=300)
plt.show()
	