
# coding: utf-8

# In[3]:


import geopandas as gp


# In[5]:


df = gp.read_file("./skogsbrander/UngefarligtBrandomradeSKS_181108.shp")


# In[17]:


brand = df[df["Kommentar"].str.contains('brand', na=False, case=False)]
inteBrand  = ~df.index.isin(brand.)

