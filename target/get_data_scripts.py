
# coding: utf-8

# In[17]:


import json
import shutil
import os
import requests
import time


# In[18]:


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


# In[22]:


json_data = get_json_data(lng=106.18,lat=54.00)


# In[23]:


def toString(long, lat):
    return "lng:" + long + "lat:" + lat

def download_files(rel_dir, json_req):
    try:
        if not os.path.exists(rel_dir):
            os.makedirs(rel_dir)

        name = toString(json_data["location"]["lng"], json_data["location"]["lat"]) + "/"

        if os.path.exists(rel_dir + name):
            print("you've already downloaded " + name + ". If you want to redo this, delete this directory.")
            return
        else:
            os.makedirs(rel_dir + name)

        print("downloading " + str(len(json_data["images"])) + " into folder " + name)
        t = time.time()
        for idx, image in enumerate(json_data["images"]):
            if idx % 10 == 0:
                print(str(idx) +  " images downloaded")
            response = requests.get(image["url"], stream=True)
            file_name = rel_dir + name + "time:" + str(image["time"]) + ".png"
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        print("done. took " + str(time.time() - t) + " time")
    except:
        print("something went wrong. removing " + name)
        shutil.rmtree(rel_dir + name)


# In[ ]:


download_files("./downloads/", json_data)


# ## Generate versioncontrollable artifacts

# In[8]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to python get_data_scripts.ipynb")


# In[9]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to html get_data_scripts.ipynb")

