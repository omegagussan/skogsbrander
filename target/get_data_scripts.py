
# coding: utf-8

# In[4]:


import json
import shutil
import os
import requests
import time


# In[5]:


def get_json_data(lat, lng, datum_string_from, datum_string_to):
    api_url = 'https://mtf-sat.synvinkel.org/timeseries?apikey=biscayabukten&fbclid=IwAR0woGRqFpiBML0h03XRs9Uz5ag3Vw834foaHnW4oCyRbRxjVyU8mmKOILE'
    #always whole 2018
    paramters  =' &lng=' + str(lng) + '&lat=' + str(lat) + '&startDate=' + datum_string_from +'&endDate=' + datum_string_to
    req = requests.get(api_url + paramters)
    if req.status_code == 200:
        req_data = req.content
        return json.loads(req_data)
    else:
        return None


# In[7]:


json_data = get_json_data(lng=106.18,lat=54.00, datum_string_from="2018-01-01", datum_string_to="2019-12-30")


# In[ ]:


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

# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to python get_data_scripts.ipynb")


# In[ ]:


get_ipython().system("jupyter nbconvert --output-dir='./target' --to html get_data_scripts.ipynb")

