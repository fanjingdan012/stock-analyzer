import matplotlib.pyplot as plt
import squarify    # pip install squarify (algorithm for treemap)
import pandas as pd
root_dir = __file__[:__file__.rfind("/")]
date_str='2021-06-28'
# Create a data frame with fake data
df = pd.read_csv(root_dir+'/../data/industry_quote/'+date_str+'.csv')

# plot it
squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8 )
plt.axis('off')
plt.savefig(root_dir+'/../data/charts/industry_quote_'+date_str+'.jpg')
plt.show()