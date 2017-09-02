import os
import glob, sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
 
 
path = "./"


fig = plt.figure(figsize=(8,4))
ax	= fig.add_subplot(111)


def smooth(distance,elevation):
    dist,elev_smooth = distance,elevation

    return dist,elev_smooth


def plot_dat(ax,infile,color='b',show=False,offset=0):
	print 'Infile: ' + infile
	data = np.loadtxt(infile)
	
	distance = data[:,0]
	elevation = data[:,1]
	
	
	dist,elev_smooth = smooth(distance,elevation)
	
	dist = dist + offset
	
	print dist
	#plt.plot(distance,elevation,color='r')
	ax.plot(dist,elev_smooth,color=color,lw=1,label=infile[:-4],alpha=0.8)
	ax.fill_between(dist,elev_smooth,alpha=0.05,color=color)
	
	ax.set_xlim(0,distance.max())
	
	top  = 500*np.ceil((elev_smooth.max()+50)/500.0)
	bottom = 500*np.floor((elev_smooth.min()-300)/500.0)
	ax.set_ylim(bottom,top)
	

	



	
	
 
 


# make_plot('/Users/danhickstein/Documents/Elevation_profiles/Aug 14 - Individual Legs/Leg B01 - Shinglemill.dat', 
#			  show=True)

# show_plots = 0
# #show_plots = 1
# 
# #path = sys.argv[1]
# 




plot_dat(ax,'CTR 285.dat',color='b')
plot_dat(ax,'CTR Tarryall.dat',color='r',offset=0)
fig.subplots_adjust(bottom=.13)

ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Elevation (feet)')
ax.set_title('CTR Elevation profiles')

leg = ax.legend(fontsize=11)
leg.draw_frame(False)
	
plt.savefig('CTR-compared.png',dpi=200)

plt.show()

# 
# def smooth1(distance,elevation):
# 
#     distance = data[:,0]
# 	elevation = data[:,1]
# 	m=len(elevation); q = m+np.sqrt(2*m)
# 	tck = scipy.interpolate.splrep(distance,elevation,s=20*q)
# 	dist = np.linspace(distance.min(),distance.max(),500)
# 	elev_smooth = scipy.interpolate.splev(dist,tck,der=0)
# 	return elev_smooth

	