# MULTI-STAR
Multi-label subtyping and advanced recognition of cancer patients

## Description
We developed and offer a computational workflow, named MULTI-STAR, to address current limitations in state-of-the-art similarity-based stratification approaches. 
MULTI-STAR indeed provides machine learning-based multi-label classifiers for more comprehensive and reliable single-sample stratification.

## Steps of the workflow 
For any stratification/subtyping task at hand, MULTI-STAR workflow:  
- defines a comprehensive multi-label reference by extending a similarity-based subtyping method at the state-of-the-art;
- finds a valid multi-label classifier for single-sample subtyping, evaluating several machine learning models and strategies to identify the most suitable one(s).

In the here provided notebooks, we show how to extend state-of-the-art similarity-based techniques to generate multi-label characterizations of patients, given their expression profiles.
Then, we explore alternative base learners for single-label subtyping. The best-performing base learners are combined with several problem transformation strategies
and compared with known adapted algorithms, to obtain multi-label patient subtyping.
Each multi-label classifier is optimized, trained and finally assessed on test samples using many distinct performance measures. 
This wide analysis enables us to find the most promising multi-label classification approaches, 
which can be further evaluated based on relevant clinical properties like the prognostic capability of specific classes.


## Application use cases
The effectiveness of the MULTI-STAR approach was validated and showcased through the development of multi-label classifiers for breast and colorectal cancer subtyping. 
So-obtained classifiers offered not only superior performance but also more comprehensive insights into patient heterogeneity, even surpassing existing methods in terms of prognostic value of predictions and single-sample usability, as required by clinical practice.


