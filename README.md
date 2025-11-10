This repository contains the code and model specifications for the study: Preferences for antihypertensive prescribing in older adults: A Discrete Choice Experiment.

Contents:
01_Base_MNL_model_Code_GitHub
02_MMNL_model_Serial_1_GitHub
03_LMC_Serial_1_GitHub
04_MNL_model-Interactions_GitHub


Requirements:
Python version: 3.2.11
Libraries:
1. pandas 
2. biogeme.database 
3. biogeme.biogeme 
4. from biogeme import models, 
5. from biogeme.expressions import Beta, Variable, log, exp, PanelLikelihoodTrajectory, bioDraws, MonteCarlo

Default Biogeme Parameters
Second derivatives: 1.0
Tolerance: 6.06273418136464e-06
Max iterations: 100
Monte Carlo draws: 5000
Seed: 0
Optimization algorithm: simple_bounds
Threads: 6


Model Specifications:
Data: 
Source: Self-reported discrete choice experiment (DCE) responses and demographic data from 197 participants.
Recruitment: The DCE survey was distributed via: A closed Facebook group for Australian general practitioners; The Cardiac Society of Australia and New Zealand (CSANZ) newsletter;
Email invitations to tertiary and primary care doctors
Access: Doctors accessed the survey through a link to the Qualtrics platform.
Availability: November 2023 to June 2024. 
Of the 200 doctors who accessed the survey, 197 (98.5%) completed the DCE in full and provided demographic data. Three incomplete responses were excluded from the analysis. 
Structure: Panel data for discrete choice experiment
Missing data code: 99999

Models Implemented
Base MNL: Multinomial Logit model without random parameters
MMNL: Mixed Multinomial Logit with random coefficients
LMC: Latent Class Model for preference heterogeneity
MNL with Interactions: Includes interaction terms for age, sex, and comorbidities

Estimation Details
Algorithm: Trust region with simple bounds
Draws for simulation: 5000 (Monte Carlo)
Convergence tolerance: 6.06e-06
Maximum iterations: 100

Assumptions
Independence of irrelevant alternatives (IIA) for MNL
Random taste variation for MMNL
Latent classes capture unobserved heterogeneity

