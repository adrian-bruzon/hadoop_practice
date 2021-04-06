# Libraries
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import json, os

# Set the dimension of the figure
my_dpi = 300
plt.figure(figsize=(5200 / my_dpi, 2600 / my_dpi), dpi=my_dpi)

# read the data (on the web)
data = pd.read_csv(os.path.abspath('./') + '/results.csv', sep=",")

# Make the background map
m = Basemap(llcrnrlon=-130, llcrnrlat=25, urcrnrlon=-57, urcrnrlat=55)
m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
m.fillcontinents(color='grey',lake_color='lightblue', alpha= 0.3)
m.drawcoastlines(linewidth=0.2, color="white")
m.drawstates(linewidth=0.1, linestyle='solid', color='k')
m.drawparallels(np.arange(0.,90.,5.),color='gray',dashes=[1,3],labels=[1,0,0,0])
m.drawmeridians(np.arange(0.,360.,15.),color='gray',dashes=[1,3],labels=[0,0,0,1])
plt.title('Happier States')

# Make the bubbels
plt.scatter(data['homelong'], data['homelat'], label=None, c=data['Score'], cmap='plasma', s=data['Tweets']*50,
            linewidth=0, alpha=1)

#Make the color legend
plt.colorbar(label='Score', fraction=0.02, pad=0.04)

#Make the sizes bubbels legend
for tweets in [2, 10, 20, 50, 80]:
    plt.scatter([], [], c='k', alpha=0.3, s=tweets * 50,
                label=str(tweets) + ' Tweets')
plt.legend(scatterpoints=1, frameon=False, labelspacing=5,
           loc='lower right', ncol=2, columnspacing=3, borderpad=1, handletextpad=2.5)
# Save as png
plt.savefig('happier_states_map.png', bbox_inches='tight')
