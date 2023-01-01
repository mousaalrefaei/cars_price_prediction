## cars_price_prediction

### About:
End-to-End project from the data collection to the model deployment to predict the used cars prices in Germany
The data collected from AutoScout24 website (one of the biggest used cars platforms in Germany).

### Files:
#### 1- scraping:
scrape the data from autoscout24 website using BeautifulSoup library and save it to csv file.
#### 2- preprocessing:
prepare the data to be used to train the model (feature engineering and feature selection).
#### 3- XGBoost_model:
split and encode the data and build an XGBoost model.
#### 4- model:
the model in pickle format to be used later in deployment stage
#### 5- streamlit:
build an MVP (Minimum viable Product) using StreamLit framework.
#### 6- auto_search:
build a function to find the similar cars in AutoScout24 website in real time>
#### 7- cars:
the saved data file from the data collection stage.

### Note:
some of the features and values are in German language.

### The front-end of the MVP:


<img width="469" alt="image" src="https://user-images.githubusercontent.com/89030524/210172546-37130856-eb70-4dc6-842a-c0b48d8c0b52.png">


