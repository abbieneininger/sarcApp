import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

prefix = 'Z-'
features = ['Total Number of Myofibrils','Total Number of {}Lines'.format(prefix),
            'Average Myofibril Persistence Length','Average {}Line Length'.format(prefix), 
            'Average {}Line Spacing'.format(prefix),'Average Size of All Puncta', 'Total Number of Puncta',
            'Total Number of MSFs', 'Total Number of Z-Bodies', 'Average MSF Persistence Length', 
            'Average Z-Body Length', 'Average Z-Body Spacing']

df = pd.read_excel("E:/Blebbistatin MYH6-7 Project/Actinin2_24H_BB_Stats_DL/Actinin2_24H_tSNE.xlsx")
df.fillna(0)
df = StandardScaler().fit_transform(df)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(df)
principal_df = pd.DataFrame(data=principalComponents, columns = ['pc 1','pc 2'])
print(principal_df.tail())
#tsne_em = TSNE(n_components=2, perplexity=30.0, n_iter=1000, verbose=1).fit_transform(df)