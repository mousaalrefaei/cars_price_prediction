
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

df= pd.read_csv('cars.csv')

def load_model():
   with open ('model.pkl','rb') as f:
      model = pickle.load(f)
   return model

model = load_model()


#with st.container():
col1, col2 = st.columns(2)
with col1:

   st.title('Estimate your car price')

   st.write(
      'please fill the fields below:'
   )

   # car brand:

   car_name = st.selectbox('brand:', df['marke'].unique())

   # car model:

   models = df.loc[(df['marke'] == str(car_name))]

   car_model= st.selectbox('car model:',models['modell'].unique())

   # car type:

   types = df.loc[(df['modell'] == str(car_model)) & ((df['marke'] == str(car_name)))]

   car_type = st.selectbox('car type:', types['Karosserieform'].unique())


   # Transmission
   transmission = st.selectbox('transmission:', df['Getriebe'].unique())

   # fuel type:

   fuel = df.loc[(df['modell'] == str(car_model)) & ((df['marke'] == str(car_name)))]

   fuel_type = st.selectbox('fuel type:', fuel['Kraftstoff'].unique())

   # registeration year:

   years = df.loc[(df['modell'] == str(car_model)) & ((df['Karosserieform'] == str(car_type)))]

   registeration_year = st.selectbox('registeration year:',years['Erstzulassung'].unique())

   # mileage:

   mileage = st.number_input('mileage (km):',min_value=1, max_value=750000)
   # mileage = st.slider('mileage (km):', 0, 500000, 2000)

   # power:
   powers = df.loc[(df['modell'] == str(car_model)) & ((df['Karosserieform'] == str(car_type))) & (df['Erstzulassung'] == registeration_year)]
   power = st.selectbox('car engine power (kw): ',powers['Leistung'].unique())

   # predict:
   predict = st.button('predict the price')
   if predict:
      
      X = {'modell':[str(car_model)],'Karosserieform':[str(car_type)], 'Kilometerstand':[mileage], 'Erstzulassung':[registeration_year], 'Leistung': [power], 'Getriebe': [str(transmission)]}#, 'Kraftstoff':[str(fuel_type)]}

      X= pd.DataFrame(data= X)
      X['modell'] = encoder.fit_transform(X['modell'])
      X['Karosserieform'] = encoder.fit_transform(X['Karosserieform'])
      X['Getriebe'] = encoder.fit_transform(X['Getriebe'])
      #X['Kraftstoff'] = encoder.fit_transform(X['Kraftstoff'])
      price = model.predict(X)
      st.subheader(f'The price between: {int(price * 0.9)} and {int(price * 1.1)} €')


# showing some information about the car:
with col2:
   # the average price according to the registration year:
   report = st.button('The average price according to the registration year')

   # the average price according to the transmission:
   report2 = st.button('The average price according to the transmission')
   
   if report:
      sim = df.loc[(df['modell'] == str(car_model)) & ((df['Erstzulassung'] >= (registeration_year - 5)))& ((df['Erstzulassung'] <= (registeration_year + 5)))]
      fig = px.bar(sim.groupby(['Erstzulassung'], as_index= False).median(), x = 'Erstzulassung', y= 'price', title= f'The average price of {car_model} according to the registration year:', text= 'price')
      st.plotly_chart(fig)
   
   if report2:
      trans = df.loc[((df['modell']) == str(car_model)) & (df['Erstzulassung'] == registeration_year)]
      fig = px.bar(trans.groupby(['Getriebe'], as_index=False).median(), x= 'Getriebe', y = 'price', title = f'The average price of {car_model} according to the transmission:', text = 'price' )
      st.plotly_chart(fig)
