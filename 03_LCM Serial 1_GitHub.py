"""File 
:author: John Rose, ITLS
:date: May 2023
:data: MurrayD.txt
"""

## Import libraries necessary for model estimation
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
from biogeme import models
from biogeme.expressions import Beta, Variable, PanelLikelihoodTrajectory, log, exp

## Read the data
df = pd.read_csv('DCE_Data20250310.csv')
database = db.Database('DCE_Data20250310.csv', df)

## Read the names in the first row of data as variables
globals().update(database.variables)

# Data organized as panel data. The variable Resp identifies each individual.
database.panel("id")

## Define categorical variables correctly (convert Boolean to numeric)
cv_int_4 = database.DefineVariable('cv_int_4', (cv_int == 4) * 1)
cv_sta_5 = database.DefineVariable('cv_sta_5', (cv_sta == 5) * 1)

age_75=database.DefineVariable('age_75', (age == 75) * 1)
age_80=database.DefineVariable('age_80', (age == 80) * 1)


## Parameters to be estimated
#### Beta(name, default, lower, upper, estimate/not)
#### Class Assignment ####
ConA = Beta('Class A Constant',0,None,None,0)
Part_AgeA = Beta('Class A Part_Age',0,None,None,0)
Part_FemA = Beta('Class A Part_Fem',0,None,None,0)
Part_DigA = Beta('Class A Part_Dig',0,None,None,0)

#### Class A ####
IntA = Beta('intensive A',0.507607,None,None,0)

cvev_int4A = Beta('cevent_int4_A',-0.296611,None,None,0)
cvev_sta5A = Beta('cvev_sta5_A', -0.665096, None, None, 0)

dh_intA = Beta('dig_health_int_A', 0.224662, None, None, 0)
dh_staA = Beta('dig_health_sta_A', -0.095683, None, None, 0)

Age75A =  Beta('Age75_A',-0.878198,None,None,0)
Age80A= Beta('Age80_A',-2.048052,None, None,0)

Frail1A = Beta('Frailty_A',-0.924139,None,None,0)
Fall1A= Beta('fevnt_A',-0.925317,None,None,0)

#### Class B ####
IntB = Beta('intensive B',0.507607,None,None,0)

cvev_int4B = Beta('cevent_int4_B',-0.296611,None,None,0)
cvev_sta5B = Beta('cvev_sta5_B', -0.665096, None, None, 0)

dh_intB = Beta('dig_health_int_B', 0.224662, None, None, 0)
dh_staB = Beta('dig_health_sta_B', -0.095683, None, None, 0)

Age75B =  Beta('Age75_B',-0.878198,None,None,0)
Age80B= Beta('Age80_B',-2.048052,None, None,0)

Frail1B = Beta('Frailty_B',-0.924139,None,None,0)
Fall1B= Beta('fevnt_B',-0.925317,None,None,0)


############################## Utility functions ############################## 
#### Class Assignment ####
VcA = ConA + Part_AgeA*part_age + Part_FemA*part_fem + Part_DigA*part_dig

#### Class A ####
V1A = (IntA +
       cvev_int4A * cv_int_4 +
      dh_intA*digh_int+
      Age75A*age_75 + Age80A*age_80 +
      Frail1A*frailty +
      Fall1A*fall)     
     

V2A = (cvev_sta5A * cv_sta_5 + 
      dh_staA*digh_sta)


#### Class B ####
V1B = (IntB +
       cvev_int4B * cv_int_4 +
      dh_intB*digh_int+
      Age75B*age_75 + Age80B*age_80 +
      Frail1B*frailty +
      Fall1B*fall)     
     

V2B = (cvev_sta5B * cv_sta_5 + 
      dh_staB*digh_sta)


## Associate utility functions with the numbering of alternatives
utilityA = {1: V1A, 0: V2A}
utilityB = {1: V1B, 0: V2B}

#### Definition of the model. This is the contribution of each observation to the log likelihood function.
availability = {1: 1, 0: 1}

## Definition of the model. This is the contribution of each observation to the log likelihood function.
probA = models.logit(utilityA,availability,choice)
probB = models.logit(utilityB,availability,choice)

### Class Assignment Probability
PcA = exp(VcA)/(exp(VcA) + 1)
PcB = 1 - PcA

### Conditional probability
condP = PanelLikelihoodTrajectory(probA*(PcA**(1/12))) + PanelLikelihoodTrajectory(probB*(PcB**(1/12)))

## Create the Biogeme object
biogemeObject = bio.BIOGEME(database, log(condP))
biogemeObject.modelName = 'LCM Serial 1_V3'

## Estimate the parameters
results = biogemeObject.estimate()

## Print the results
pandasResults = results.getEstimatedParameters(onlyRobust=False)
print(pandasResults)
