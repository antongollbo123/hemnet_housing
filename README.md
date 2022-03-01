# hemnet_housing

## Background
Choosing where to live and spend your days can be a difficult thing. With housing prices rising, it is tough for a new venturer into the housing market to decide how much to commit and when. This leads us into this project. Moving to Stockholm has been in my consideration for quite some time, but not knowing the specific areas makes searching for apartments quite difficult. In this project, I wanted to narrow down Stockholm inner city to 6 popular areas and model a regression model to see how the different areas and features can affect the price of apartments in the different areas.  

## Method

The goal of this project is to do the following:
#### Data Gathering
(1) Data Gathering
Scrape Swedish housing market website "Hemnet" for interesting features and price values from 6 areas in Stockholm city. The goal is also to scrape additional features, such as square meters, rooms etc. 
#### Data Cleaning
(2)
a. Clean the data that was scraped in (1).

b. Use the cleaned data to insert into Yelp API. The purpose of this is to "translate" physical adresses to coordinates, so that they are quantifiable and comparable with each other. From Yelp, points of interest will also be gathered to have one more relevant feature present in the data. (ATTN. Using Yelp API was heavily inspired by Gustaf Halvardsson, see his Medium article here: https://towardsdatascience.com/a-data-science-approach-to-stockholms-apartment-prices-part-1-dcee0212596d )

c. Create a local database (through SQLLite) and insert the cleaned data with additional information from Yelp
#### Exploratory Data Analysis
(3) Extract specific data through SQL queries and import them into a notebook environment. Perform exploratory data analysis to find patterns and insights from the different areas and features of the specified apartments. 
#### Regression modelling

(4) After EDA is done, regression modelling is done to see if the price of a location can be somewhat correctly predicted with regression models. The second goal is also to see what featur
