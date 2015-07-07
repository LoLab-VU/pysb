import os
from pysb.integrate import odesolve
from pysb.util import load_params
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pysb.tools.visualize import create_png_image_from_dot , create_visualization_bngl
from pysb.examples.tyson_oscillator import model


t = np.linspace(0,100,2000)
x = odesolve(model,t)

# the stride length in which we want to save images for the video
strides = 10

#TODO we remove the first 10 steps for normalization purposes. Need a better way!
equil_period = 10

y = np.zeros(((len(t)-equil_period)/strides,len(model.species)))

# normalize the concentrations of each species from 0 to 1
for i in range(len(model.species)):
    tmp = x['__s'+str(i)]
    tmp = tmp[equil_period::strides]
    max  = np.max(tmp)
    min = np.min(tmp)
    if max - min == 0:
        y[:,i] = 1.
    else:
        tmp = (tmp-min )/ (max - min)
        y[:,i] = tmp

time = t[10::strides]
colors = plt.cm.rainbow(np.linspace(0, 1, len(model.species)))
fontP = FontProperties()
fontP.set_size('small')

for i in range(1,np.shape(y)[0]):
    graph = create_png_image_from_dot(model,y[i,:],'example%05d.png' % i)
    
    ax = plt.subplot(111)
    for j in range(len(model.species)):
        Label=str(model.species[j])
        Label='s%d' % j
        ax.plot(time[:i],y[:i,j],color = colors[j])
        ax.plot(time[i],y[i,j],'o',color = colors[j],label=Label)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop = fontP,ncol=3)
    plt.xlim(0,time[-1])
    plt.savefig('species_all_%05d.png' % (i),dpi=200,bbox_inches='tight')
    plt.clf()


save = False
if save == True:
    video_file_name = 'reaction_network_%s.avi' % model.name
    video_file_name2 = 'xy_species_%s.avi' % model.name
    if os.path.isfile(video_file_name):
        print "removing old video file. Check to see if this is correct"
        os.remove(video_file_name)
    if os.path.isfile(video_file_name2):
        print "removing old video file. Check to see if this is correct"
        os.remove(video_file_name2)    
    os.system('avconv -r 10 -i example%s.png %s' % ('%05d',video_file_name))
    os.system('avconv -r 10 -i species_all_%s.png %s' % ('%05d',video_file_name2))
    os.system('rm example*.png')
    os.system('rm species*.png')
