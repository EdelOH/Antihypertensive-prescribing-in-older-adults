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
from biogeme.expressions import Beta, Variable, log, exp, PanelLikelihoodTrajectory, bioDraws, MonteCarlo


## Read the data
df = pd.read_csv('DCE_Data.csv')
database = db.Database('DCE_Data.csv', df)

# Data organized as panel data. The variable id identifies each individual.
database.panel("id")

## Read the names in the first row of data as variables
globals().update(database.variables)

## Define categorical variables correctly (convert Boolean to numeric)
cv_int_4 = database.DefineVariable('cv_int_4', (cv_int == 4) * 1)
cv_sta_5 = database.DefineVariable('cv_sta_5', (cv_sta == 5) * 1)

age_75=database.DefineVariable('age_75', (age == 75) * 1)
age_80=database.DefineVariable('age_80', (age == 80) * 1)

### Define draws
num_draws = 500  # Reduce the number of draws
cv_int_draws = bioDraws('cv_int_draws', 'NORMAL')
digh_int_draws = bioDraws('digh_int_draws', 'NORMAL')
cv_sta_draws = bioDraws('cv_sta_draws', 'NORMAL')
digh_sta_draws = bioDraws('digh_sta_draws', 'NORMAL')

## Parameters to be estimated
#### Beta(name, default, lower, upper, estimate/not)
#### Fixed parameters
Int = Beta('intensive', 0.507607 ,None,None,0)

Age75 =  Beta('Age75',-0.878198,None,None,0)
Age80= Beta('Age80',-2.048052,None, None,0)

Frail1 = Beta('Frailty',-0.924139,None,None,0)
Fall1= Beta('Fall',-0.925317,None,None,0)



#### Random parameters
## Mean estimates ##

cvev_int4m = Beta('cevent_int4 mean',-0.296611,None,None,0)
cvev_sta5m = Beta('cevent_sta5 mean',-0.665096,None,None,0)


dh_intm = Beta('dig health_int mean',0.224662,None,None,0)
dh_stam = Beta('dig health_sta mean',-0.095683,None,None,0)

## Std dev estimates ##

cvev_int4s = Beta('cevent_int Std Dev',0.0001,None,None,0)
cvev_sta5s = Beta('cevent_sta Std Dev',0.0001,None,None,0)

dh_ints = Beta('dig health_int Std Dev',0.0001,None,None,0)
dh_stas = Beta('dig health_sta Std Dev',0.0001,None,None,0)


cv_eventAgeI = Beta('cardio event_int * Age',0,None,None,0)
cv_eventAgeS = Beta('cardio event_sta * Age',0,None,None,0)
fallAge= Beta('Fall * Age',0,None, None,0)

## Define random parameters using bioDraws
cvev_int4= cvev_int4m + cvev_int4s*cv_int_draws
cvev_sta5 =cvev_sta5m + cvev_sta5s*cv_sta_draws
dh_int  = dh_intm + dh_ints*digh_int_draws
dh_sta = dh_stam + dh_stas*digh_sta_draws

############################## Utility functions ##############################
V1 = (Int +
      cvev_int4 * cv_int_4 +
      dh_int*digh_int+
        Age75*age_75 + Age80*age_80 +
      Frail1*frailty +
      Fall1*fall)     
     
V2 = (cvev_sta5 * cv_sta_5 +
      dh_sta*digh_sta)


## Associate utility functions with the numbering of alternatives
utility = {1: V1, 0: V2}

#### Definition of the model. This is the contribution of each observation to the log likelihood function.
availability = {1: 1, 0: 1}

## Definition of the model. This is the contribution of each observation to the log likelihood function.
prob = models.logit(utility,availability,choice)
condP = PanelLikelihoodTrajectory(prob)

## Create the Biogeme object
biogemeObject = bio.BIOGEME(database, log(MonteCarlo(condP)))
biogemeObject.modelName = 'MMNL Serial 1_V5'

## Estimate the parameters
results = biogemeObject.estimate()

## Print the results
pandasResults = results.getEstimatedParameters(onlyRobust=False)
print(pandasResults)

