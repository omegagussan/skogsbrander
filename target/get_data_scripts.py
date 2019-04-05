
# coding: utf-8

# In[31]:


import json
import shutil
import os
import requests


# In[5]:


api_url = 'https://mtf-sat.synvinkel.org/timeseries?apikey=biscayabukten&fbclid=IwAR0woGRqFpiBML0h03XRs9Uz5ag3Vw834foaHnW4oCyRbRxjVyU8mmKOILE'
paramters  =' &lng=106.18&lat=53.98&startDate=2018-01-01&endDate=2018-12-30'


# In[27]:


#get list of images for coordinates
req_data = requests.get(api_url + paramters).content
json_data = json.loads(req_data)
json_data


# In[49]:


def toString(long, lat):
    return "lng:" + long + "lat:" + lat

def download_files(rel_dir, json_req):
    if os.path.exists(rel_dir):
        shutil.rmtree(rel_dir)
    os.makedirs(rel_dir)

    name = toString(json_data["location"]["lng"], json_data["location"]["lat"])
    
    for image in json_data["images"]:
        response = requests.get(image["url"], stream=True)
        file_name = rel_dir + name + "time:" + str(image["time"]) + ".png"
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


# In[51]:


download_files("./downloads/", json_data)


# ## Generate versioncontrollable artifacts

# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to python TrailerGeneration.ipynb")


# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to html TrailerGeneration.ipynb")

