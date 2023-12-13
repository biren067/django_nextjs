#!/usr/bin/env python
# coding: utf-8

# In[3]:


from fyers_apiv3 import fyersModel
import pandas as pd
import os
client_id = "TNRLEAR9UP-100"
is_token = False
content = ""
if os.path.exists("access_token.txt"):
    with open("access_token.txt","r") as fp:
        access_token = fp.read()
        print("Access token is available in .txt File")
        if access_token:
            is_token = True
if is_token==True:
    print("Token not available")
    client_id = "TNRLEAR9UP-100"
    secret_key = "VCFFWC2WIA"
    redirect_uri = "https://www.elevenunit.com/"
    response_type = "code"
    state = "sample_state"
    grant_type="authorization_code"
    
    session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
    )
    
    response = session.generate_authcode()
    print("Login URL::",response)
    
    auth_code = input("Enter auth code")
    session.set_token(auth_code)
    print(session)
    
    response = session.generate_token()
    print(response)

    
    access_token = response['access_token']
    with open("access_token.txt","w") as f:
        f.write(access_token)


# In[4]:


from datetime import datetime,timedelta
### present date
today_timestamp = datetime.now()
curr_date = today_timestamp.strftime("%Y-%m-%d")

#previous date
prev_date = today_timestamp - timedelta(days = 10)
prev_date = prev_date.strftime("%Y-%m-%d")
print("Start Date:",prev_date)
print("End Date  :",curr_date)


# In[7]:


fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
symbol="NSE:SBIN-EQ"
data = {"symbol":symbol,"resolution":"60","date_format":"1","range_from":prev_date,"range_to":curr_date,"cont_flag":"1"}
data = fyers.history(data)

if data['s']!='ok':
    print("Error is accessing data",data)
else:
    print("Congratulation!! you got the data")


# In[8]:


df = pd.DataFrame(data['candles'],columns=['Date','Open','High','Low','Close','Volume'])
df['Date']=df['Date'].apply(lambda x:datetime.fromtimestamp(x))
df


# In[ ]:




