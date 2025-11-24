"""File 
:author:
:date:
:data:
"""

## Import libraries necessary for model estimation
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta, Variable, log, exp

## Read the data
df = pd.read_csv('DCE_data.csv')
database = db.Database('DCE_data', df)

## Read the names in the first row of data as variables
globals().update(database.variables)

## Define categorical variables correctly (convert Boolean to numeric)
cv_int_4 = database.DefineVariable('cv_int_4', (cv_int == 4) * 1)
cv_sta_5 = database.DefineVariable('cv_sta_5', (cv_sta == 5) * 1)

age_75=database.DefineVariable('age_75', (age == 75) * 1)
age_80=database.DefineVariable('age_80', (age == 80) * 1)


## Parameters to be estimated
#### Beta(name, default, lower, upper, estimate/not)
Int = Beta('intensive',0,None,None,0)

cvev_int4 = Beta('cvev_int4', 0, None, None, 0)
cvev_sta5 = Beta('cvev_sta5', 0, None, None, 0)

dh_int = Beta('dig health_int',0,None,None,0)
dh_sta = Beta('dig health_sta',0,None,None,0)

Age75 =  Beta('Age75',0,None,None,0)
Age80= Beta('Age80',0,None, None,0)

Frail1 = Beta('Frailty',0,None,None,0)
Fall1= Beta('fevnt',0,None,None,0)

cv_eventAge75I = Beta('cardio event_int * Age75',0,None,None,0)
cv_eventAge80I = Beta('cardio event_int * Age80',0,None,None,0)
cv_eventAge75S = Beta('cardio event_sta * Age75',0,None,None,0)
cv_eventAge80S = Beta('cardio event_sta * Age80',0,None,None,0)
cv_eventFallI= Beta('cardio event_int * fall',0,None, None,0)
cv_eventFallS= Beta('cardio event_sta * fall',0,None, None,0)
cv_eventFrailI=Beta('cardio event_int * frail',0,None, None,0)
cv_eventFrailS=Beta('cardio event_sta * frail',0,None, None,0)



############################## Utility functions ############################## 
V1 = (Int +
      cvev_int4*cv_int_4 +
      dh_int*digh_int+
     Age75*age_75 + Age80*age_80 +
      Frail1*frailty +
      Fall1*fall +
      cv_eventAge75I*cv_int_4*age_75+
      cv_eventAge80I*cv_int_4*age_80+
      cv_eventFallI*cv_int_4*fall+
        cv_eventFrailI*cv_int_4*frailty)     
     
V2 = (cvev_sta5*cv_sta_5 + 
      dh_sta*digh_sta+
      cv_eventAge75S*cv_sta_5*age_75 +
      cv_eventAge80S*cv_sta_5*age_80 +
      cv_eventFallS*cv_sta_5*fall+
        cv_eventFrailS*cv_sta_5*frailty)


## Associate utility functions with the numbering of alternatives
utility = {1: V1, 2: V2}

#### Definition of the model. This is the contribution of each observation to the log likelihood function.
availability = {1: 1, 2: 1}

## Definition of the model. This is the contribution of each observation to the log likelihood function.
prob = models.logit(utility,availability,choice)

## Create the Biogeme object
biogemeObject = bio.BIOGEME(database, log(prob))
biogemeObject.modelName = 'MNL_interactions'

## Estimate the parameters
results = biogemeObject.estimate()

## Print the results
pandasResults = results.getEstimatedParameters(onlyRobust=False)
print(pandasResults)

