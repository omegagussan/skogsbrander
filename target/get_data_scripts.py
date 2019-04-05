
# coding: utf-8

# In[1]:


import json
import shutil
import os
import requests


# In[2]:


def get_json_data(lat, lng):
    api_url = 'https://mtf-sat.synvinkel.org/timeseries?apikey=biscayabukten&fbclid=IwAR0woGRqFpiBML0h03XRs9Uz5ag3Vw834foaHnW4oCyRbRxjVyU8mmKOILE'
    #always whole 2018
    paramters  =' &lng=' + str(lng) + '&lat=' + str(lat) + '8&startDate=2018-01-01&endDate=2018-12-30'
    req = requests.get(api_url + paramters)
    if req.status_code == 200:
        req_data = req.content
        return json.loads(req_data)
    else:
        return None


# In[3]:


json_data = get_json_data(lng=106.20,lat=53.98)
json_data


# In[6]:


def toString(long, lat):
    return "lng:" + long + "lat:" + lat

def download_files(rel_dir, json_req):
    if not os.path.exists(rel_dir):
        os.makedirs(rel_dir)

    name = toString(json_data["location"]["lng"], json_data["location"]["lat"]) + "/"

    if not os.path.exists(rel_dir + name):
        os.makedirs(rel_dir + name)
    
    for image in json_data["images"]:
        response = requests.get(image["url"], stream=True)
        file_name = rel_dir + name + "time:" + str(image["time"]) + ".png"
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


# In[7]:


download_files("./downloads/", json_data)


# ## Generate versioncontrollable artifacts

# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to python get_data_scripts.ipynb")


# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to html get_data_scripts.ipynb")

