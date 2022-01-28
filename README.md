# Hemnet_Housing
The goal of this project is to do the following:

(1) Scrape Hemnet for interesting features and price values from 6 areas in Stockholm city. The goal is also to scrape additional features, such as square meters, rooms etc. 

(2) 
a. Clean the data that was scraped in (1).

b. Use the cleaned data to insert into Yelp API. The purpose of this is to "translate" physical adresses to coordinates, so that they are quantifiable and comparable with each other. From Yelp, points of interest will also be gathered to have one more relevant feature present in the data. (ATTN. Using Yelp API was heavily inspired by Gustaf Halvardsson, see his Medium article here: https://towardsdatascience.com/a-data-science-approach-to-stockholms-apartment-prices-part-1-dcee0212596d )

c. Create a local database (through SQLLite) and insert the cleaned data with additional information from Yelp

(3) When the data has been cleaned and additional data has been added through the Yelp API, EDA begins

(4) After EDA is done, regression modelling is done to see if the price of a location can be somewhat correctly predicted with regression models
