#!/usr/bin/env python
# coding: utf-8

# # Dataset used : No-Show appointments

# ## First of all let's explore the data to check if there is any missing or unlogic values and to get famiiar with it

# In[45]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 


# In[46]:


data = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')


# In[47]:


print(data.head())


# In[48]:


print(data.info())


# In[49]:


print(data.describe())


# In[50]:


print(data.columns)


# In[51]:


data["Age"].value_counts()


# In[52]:


data['Neighbourhood'].value_counts()


# In[53]:


print(data.groupby('No-show')['Alcoholism'].sum())


# In[54]:


print(data.groupby('No-show')['SMS_received'].sum())


# # Assessing Data

# #### 1- Unimportant columns are existed like patientID & appointment ID
# 
# #### 2- ScheduledDay and appoinmenday columns datatypes are inappropiate
# 
# #### 3- Inappropiate values are existed in the Handcap column
# 
# #### 4-Some age values aren't logic
# 
# #### 5-The days which the patient had to wait can be calculated through out the ScheduledDay and appoinmenday columns

# # Cleaning Data

# ## 1.1 - define

# #### Delete patientID & appointment ID Columns

# ## 1.2 - Code 

# In[55]:


data.drop(columns=['PatientId','AppointmentID'],inplace=True)


# ## 1.3 - Test 

# In[56]:


print(data.columns)
print(data.shape)


# ## 2.1 - define

# #### Converting ScheduledDay and appoinmenday column types into dateTime

# ## 2.2 - Code 

# In[57]:


data['ScheduledDay'] = pd.to_datetime(data['ScheduledDay'])
data['AppointmentDay'] = pd.to_datetime(data['AppointmentDay'])


# ## 2.3 - Test 

# In[58]:


print(data.info())


# ## 3.1 - define

# #### Replacing the un valid values which are (2,3,4) with 1 because it makes more sense

# ## 3.2 - Code 

# In[59]:


un_valid_values = [2,3,4] 
for i in un_valid_values :
    data['Handcap'].replace(i,1,inplace=True)


# ## 3.3 - Test 

# In[60]:


data['Handcap'].value_counts()


# ## 4.1 - define

# #### Replacing Ages higher than 100 with mean value, And doing the same with values like 0 and lower than it

# ## 4.2 - Code 

# In[61]:


data['Age'].replace([-1,0,102,115],int(data['Age'].mean()),inplace=True)


# ## 4.3 - Test

# In[62]:


data['Age'].describe()


# ## 5.1 - define

# ### Calculating no of days the patient had to wait by subtracting the ScheduledDay column from the AppointmentDay column and then dropping the two columns

# ## 5.2 - Code

# In[63]:


data['difference_in_days']=(data['AppointmentDay'].dt.date).sub(data['ScheduledDay'].dt.date,axis=0).dt.days
data.drop(columns=['ScheduledDay','AppointmentDay'],inplace=True)


# ## 5.3 - Test

# In[64]:


data.head()


# In[65]:


data['difference_in_days'].describe()


# In[66]:


set(data['difference_in_days'])


# ### There must be some error happened caused the -1,-6 value to exist so i'm gonna drop them

# In[67]:


dropped_data=data[(data['difference_in_days'] == -6) | (data['difference_in_days'] == -1)]


# In[68]:


data.drop(dropped_data.index ,inplace=True)


# In[69]:


data['difference_in_days'].describe()


# ### Now i'm going to take a quick look again to make sure that the data is ready to be used in analysis

# In[70]:


data.describe()


# In[71]:


data.info()


# ### Now, Data is ready for the analysis

# In[72]:


data.head()


# ## Questions 

# #### 1-What is the percent of the people that didn't show up to their appointments ? 
# 
# #### 2-What is the influence of the SMS_received on the patient's showing up situation ?
# 
# #### 3-Is the period between the ScheduledDay & the appoinmentDay has any thing to do with their showing up or not ?
# 
# #### 4-Does the patient's Scholarship affected on their showing up situation ?
# 
# #### 5-Do the patients didn't show up because they had handcaps   ?

# # <font color=red>1-</font>

# ## <font color=red>I'll start with the first question to know the percent of the showing up </font>

# In[73]:


showed_up_percent = (data[data['No-show']=="No"]['No-show'].count() / data['No-show'].count() )*100
didnot_show_up_percent = (data[data['No-show']=="Yes"]['No-show'].count() / data['No-show'].count() ) * 100
labels = "People showed up", "People didn't show up" 
sizes = [showed_up_percent,didnot_show_up_percent]
explode = (0, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("People's showing up")
plt.show()


# ### 79.8% of people showed up to their appointment

# # <font color=red>2-</font>

# ## <font color=red>Firstly let's see the effect of recieving on getting to the appointment</font>

# In[74]:


ppl_got_msg_related_data=data.groupby('No-show')['SMS_received'].sum().reset_index()
ppl_got_msg_and_showedup = (ppl_got_msg_related_data.at[0,'SMS_received'] / ppl_got_msg_related_data['SMS_received'].sum())*100
ppl_got_msg_and_didnot_showup = (ppl_got_msg_related_data.at[1,'SMS_received'] / ppl_got_msg_related_data['SMS_received'].sum())*100
labels = ["People showed up", "People didn't show up"]
sizes = [ppl_got_msg_and_showedup , ppl_got_msg_and_didnot_showup]
fig2,ax2 = plt.subplots()
ax2.pie(sizes,explode=(0,.1), labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')
plt.title("People got messages showing up")
plt.show()


# ### It looks that 72.4% of the people that got the message showed up to their meeting but to make sure of the importance of recieving the message let's see what percent of the people that didn't get the message showed up to their appointments 

# In[75]:


ppl_didnot_get_msg_related_data = data[data['SMS_received'] == 0].groupby('No-show')['SMS_received'].count().reset_index()
ppl_didnot_get_msg_and_showedup = (ppl_didnot_get_msg_related_data.at[0,'SMS_received'] / ppl_didnot_get_msg_related_data['SMS_received'].sum())*100
ppl_didnot_get_msg_and_didnot_showup = (ppl_didnot_get_msg_related_data.at[1,'SMS_received'] / ppl_didnot_get_msg_related_data['SMS_received'].sum())*100
labels = ["People showed up", "People didn't show up"]
sizes = [ppl_didnot_get_msg_and_showedup , ppl_didnot_get_msg_and_didnot_showup]
fig3,ax3 = plt.subplots()
ax3.pie(sizes,explode=(0,.1) , labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax3.axis('equal')
plt.title("People didn't get messages showing up")
plt.show()


# ### It turns that 83.3% of the people that didn't recieve a message showed up in their appointments, and based on this the message didn't have the great impact like i thought it would be.

# # <font color=red>3-</font>

# ## <font color=red>Now let's see how the number of the days between tha scheduledDay and the appointmentDay affected on people's showing up`</font>

# In[76]:


data.groupby('No-show')['difference_in_days'].describe()


# ### It looks that the number of the waiting days has a significant effect on people's showing up,people that showed up to their appintment have waited 9 days nearly in average,but the people that didtn't show up nearly waited 16 days in average

# # <font color=red>4-</font>

# ## <font color=red>Does the presence of the Scholarship affect on their situation or not ?</font>

# In[77]:


data.groupby("No-show")['Scholarship'].describe()


# ### As we can see here from the mean column, the presence of the people's scholarship didn't have a big effect on people's showing up

# # <font color=red>5-</font>

# ## <font color=red> Now Let's see if the patients didn't show up due to handcaps or not </font>

# In[78]:


data.groupby("No-show")['Handcap'].sum().reset_index()


# In[79]:


(data[data['No-show'] == "Yes"]['Handcap'].sum() / data.groupby('No-show')['Handcap'].sum().reset_index()['Handcap'].sum() ) *100


# In[80]:


ppl_didnot_showup_without_handcap=(data.groupby('No-show')['Handcap'].sum().reset_index()['Handcap'].sum())-(data[data['No-show'] == "Yes"]['Handcap'].sum())
ppl_didnot_showup_with_handcap=(data[data['No-show'] == "Yes"]['Handcap'].sum())
plt.bar("Without handcap",ppl_didnot_showup_without_handcap,label="People didn't show up without handcap")
plt.bar("With handcap",ppl_didnot_showup_with_handcap,label="People didn't show up with handcap")
plt.ylabel("Human didn't show up")
plt.title("People's handcaps")
plt.legend()


# ### It looks that only 18.16% of the people that didn't show up to their appointments had handcaps this mean that the majority had no handcap and still didn't show up

# ## <font color=orange> Limitaion : </font>

# ### There are handcaps in the rows related to the people that already showed up in the appointments which doesn't make a sense.From what i see here there is handacaps related to the people that already showed up even more that the people that didn't show up which is sure completely wrong. it's either the handcaps got replaced with another column by mistake or the wrong values may be added by mistake.  Sure this will affect the answer of this question beacuse maybe these 1834 also didn't show up in their appintemnts and so the percent will rise. 

# ## <font color=red>Summary  </font>

# ### After assessing and cleaning the data i started the analysis to determine what caused the patients not to show up in their appointments, So i tried ti guess what are the factors that can be most likely affected on them and had a deep look into the data to answer these 5 questions :

# #### 1-What is the percent of the people that didn't show up to their appointments ? 
# 
# #### 2-What is the influence of the SMS_received on the patient's showing up situation ?
# 
# #### 3-Is the period between the ScheduledDay & the appoinmentDay has any thing to do with their showing up or not ?
# 
# #### 4-Does the patient's Scholarship affected on their showing up situation ?
# 
# #### 5-Do the patients didn't show up because they had handcaps   ?

# ### After investigating the dataset and answering these questions i found that the most effective factor was the period that the people had to wait till the appointment Day. I found that if the patient that attended their appointments had to wait 9 days nearly in average while the patients that didn't show up had to wait 16 days in average.
# ### So my conclusion is that the patients don't prefer to wait too much and so the appointment day should be near to the day they schedule their appointment in. 

# ## <font color=orange> Limitaions : </font>

# ### While answering question  i  found that there are handcaps in the rows related to the people that already showed up in the appointments which doesn't make a sense.From what i see here there is handacaps related to the people that already showed up even more that the people that didn't show up which is sure completely wrong. it's either the handcaps got replaced with another column by mistake or the wrong values may be added by mistake.  Sure this will affect the answer of this question beacuse maybe these 1834 also didn't show up in their appintemnts and so the percent will rise much higher than 18.16%. Otherwise there were no null or unlogic values that can affect on the output conclusion so the previous limition was the only one.
