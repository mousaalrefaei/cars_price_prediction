Here’s the revised version optimized for `.md` formatting:

---

# **Used Cars Price Prediction in Germany**

### **Project Overview**
This end-to-end machine learning project predicts the prices of used cars in Germany. The data was collected from [AutoScout24](https://www.autoscout24.com/), one of the largest used car platforms. The project includes data collection, preprocessing, model training, and deployment, offering a complete pipeline for price prediction.

### **Project Structure**

#### 1. **Data Scraping (`scraping.py`)**
   - Scrapes data from AutoScout24 using the `BeautifulSoup` library.
   - Extracted features include car brand, model, year, mileage, fuel type, and price.
   - Saves the scraped data in a CSV file for further analysis.

#### 2. **Data Preprocessing (`preprocessing.py`)**
   - Cleans and prepares the data for training (handling missing values, feature engineering).
   - Selects relevant features to optimize model performance.

#### 3. **Model Development (`XGBoost_model.py`)**
   - Splits the dataset into training and test sets.
   - Encodes categorical variables and trains an XGBoost regression model.
   - Evaluates the model to ensure accuracy in predicting used car prices.

#### 4. **Serialized Model (`model.pkl`)**
   - Saves the trained XGBoost model in pickle format for later deployment.
   
#### 5. **Model Deployment (`streamlit.py`)**
   - Builds a Minimum Viable Product (MVP) using the Streamlit framework.
   - Users can input car details to get real-time price predictions.

#### 6. **Real-Time Search (`auto_search.py`)**
   - Implements a function that searches AutoScout24 in real-time for similar car listings.
   - Enhances user experience by providing direct comparisons with real-time market prices.

#### 7. **Collected Data (`cars.csv`)**
   - The raw dataset scraped from AutoScout24, used during model training.

### The front-end of the MVP:


<img width="469" alt="image" src="https://user-images.githubusercontent.com/89030524/210172546-37130856-eb70-4dc6-842a-c0b48d8c0b52.png">


### **Key Features**
- **End-to-End Solution**: Covers all steps from data scraping to deployment.
- **Real-Time Search**: Allows users to find similar cars on AutoScout24 directly.
- **Accurate Predictions**: Leverages the XGBoost model for reliable price estimates.
- **Interactive Application**: Deployed using Streamlit for user-friendly interaction.

#### Note:
some of the features and values in the dataset are in German language.
