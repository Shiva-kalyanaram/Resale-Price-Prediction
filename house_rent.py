import numpy as np
import pickle
import streamlit as st
import pandas as pd
import json


# Load the trained model
with open('best_lgbm_model.pkl', 'rb') as f:
    bgm = pickle.load(f)

# Load the data used during training for encoding
with open(r'encoded_data.json', 'r') as f:
    data = json.load(f)

# Load the manually encoded mappings
type_encoding = {
    'BHK1': 1,
    'BHK2': 2,
    'BHK3': 3,
    'BHK4': 4,
    'RK1': 0
}

furnishing_encoding = {
    'SEMI_FURNISHED': 2,
    'FULLY_FURNISHED': 1,
    'NOT_FURNISHED': 0
}

lease_encoding = {'FAMILY': 1, 'ANYONE': 2, 'BACHELOR': 3, 'COMPANY': 4}

Negotiation = ['Yes', 'No']
Furnish = ['SEMI_FURNISHED', 'FULLY_FURNISHED', 'NOT_FURNISHED']

water_supply_encoding = {
    'CORP_BORE': 3,
    'CORPORATION': 1,
    'BOREWELL': 2,
}

building_type_encoding = {
    'IF': 3,
    'AP': 1,
    'IH': 2,
    'GC': 4
}

parking_encoding = {
    'BOTH': 3,
    'TWO_WHEELER': 1,
    'FOUR_WHEELER': 2,
    'NONE': 0
}
locality_mapping = dict(zip(data['locality_before'], data['locality_after']))
# Check if 'facing_mapping' is present in the loaded data
facing_mapping = dict(zip(data['facing_before'], data['facing_after']))


st.set_page_config(
    page_title="Resale Flat Prices Predicting",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

st.title(":red[Resale] :blue[Flat Prices] :orange[Prediction]")

col1, col2 = st.columns(2, gap='large')

with col1:
    selected_type = st.selectbox("Select the Flat type", list(type_encoding.keys()))
    selected_locality = st.selectbox("Select the Location", data['locality_before'])
    selected_latitude = st.text_input("Enter Latitude Number")
    selected_longitude = st.text_input("Enter Longitude Number")
    Lease_type = st.selectbox("Product Reference", list(lease_encoding.keys()), key='lease_type')
    GYM = st.text_input('Enter Number of GYM')
    LIFT = st.text_input('Enter Number of Lifts available')
    Swimming_pool = st.text_input('Enter number of Swimming_pool available')
    Negotiable = st.selectbox('Select Negotiation', Negotiation)
    Furnishing = st.selectbox("Furnish type", Furnish, key='furnishing')
    Parking = st.selectbox('Select Parking', list(parking_encoding.keys()))
    Size = st.text_input("Enter Size of Property")
    Property_age = st.text_input("Enter Property_age")

with col2:
    bathroom = st.text_input("Enter No.of Bathrooms")
    Facing = st.selectbox("Side of Facing", data['facing_before'])
    Cup_boards = st.text_input("Cup_boards")
    Floor = st.text_input("No.of Floors")
    Total_floor = st.text_input("Total_Floors")
    Water_supply = st.selectbox("Enter type of water supply", list(water_supply_encoding.keys()))
    Building_type = st.selectbox("Enter type of Building", list(building_type_encoding.keys()))
    Balconies = st.text_input("Enter Balconies")
    Day = st.text_input('Enter day')
    Month = st.text_input('Enter Month')
    Year = st.text_input('Enter Year')

# Button to trigger prediction
if st.button("Get Predicted Price"):
    # Encode User Inputs
    encoded_type = type_encoding.get(selected_type, 0)
    selected_locality_encoded = locality_mapping.get(selected_locality, selected_locality)
    selected_facing_encoded = facing_mapping.get(Facing, Facing)

    # Create a DataFrame for Prediction
    user_input_df = pd.DataFrame({
        'type': [encoded_type],
        'locality': [selected_locality_encoded],
        'latitude': [float(selected_latitude) if selected_latitude and selected_latitude.strip() else 0],
        'longitude': [float(selected_longitude) if selected_longitude and selected_longitude.strip() else 0],
        'lease_type': [lease_encoding.get(Lease_type, 0)],
        'gym': [int(GYM) if GYM and GYM.strip() else 0],
        'lift': [int(LIFT) if LIFT and LIFT.strip() else 0],
        'swimming_pool': [int(Swimming_pool) if Swimming_pool and Swimming_pool.strip() else 0],
        'negotiable': [1 if Negotiable == 'Yes' else 0],  # One-hot encoding 'negotiable'
        'furnishing': [furnishing_encoding.get(Furnishing, 0)],
        'parking': [parking_encoding.get(Parking, 0)],
        'property_size': [float(Size) if Size and Size.strip() else 0],
        'property_age': [float(Property_age) if Property_age and Property_age.strip() else 0],
        'bathroom': [int(bathroom) if bathroom and bathroom.strip() else 0],
        'facing': [selected_facing_encoded],
        'cup_board': [int(Cup_boards) if Cup_boards and Cup_boards.strip() else 0],
        'floor': [int(Floor) if Floor and Floor.strip() else 0],
        'total_floor': [int(Total_floor) if Total_floor and Total_floor.strip() else 0],
        'water_supply': [water_supply_encoding.get(Water_supply, 0)],
        'building_type': [building_type_encoding.get(Building_type, 0)],
        'balconies': [int(Balconies) if Balconies and Balconies.strip() else 0],
        'day': [int(Day) if Day and Day.strip() else 0],
        'month': [int(Month) if Month and Month.strip() else 0],
        'year': [int(Year) if Year and Year.strip() else 0]
    })

    # Make Prediction
    predicted_price = bgm.predict(user_input_df)

    # Display Prediction
    st.write(f"Predicted Flat Price: {predicted_price[0]:,.2f}")





























# import numpy as np
# import streamlit as st
# import pickle
# import pandas as pd
# import json
#
# # Load the trained model
# with open('best_lgbm_model.pkl', 'rb') as f:
#     bgm = pickle.load(f)
#
# with open(r'encoded_data.json', 'r') as f:
#     data = json.load(f)
# df = pd.read_excel('House_Rent_Train.xlsx')
# # print(df)
# st.set_page_config(
#     page_title="Resale Flat Prices Predicting",
#     page_icon="",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items=None
# )
# type_encoding = {
#     'BHK1' : 1,
#     'BHK2' : 2,
#     'BHK3' : 3,
#     'BHK4' : 4,
#     'RK1' : 0
# }
# furnishing_encoding = {
#     'SEMI_FURNISHED' : 2,
#     'FULLY_FURNISHED' : 1,
#     'NOT_FURNISHED' : 0
# }
#
# lease_types = ['FAMILY', 'ANYONE', 'BACHELOR', 'COMPANY']
# Negotiation = ['Yes', 'No']
# Furnish = ['SEMI_FURNISHED', 'FULLY_FURNISHED', 'NOT_FURNISHED']
# Facing_side = []
# st.title(":red[Resale] :blue[Flat Prices] :orange[Prediction]")
#
# # #test_data= ['type', 'locality', 'latitude', 'longitude', 'lease_type', 'gym',
# #        'lift', 'swimming_pool', 'negotiable', 'furnishing', 'parking',
# #        'property_size', 'property_age', 'bathroom', 'facing', 'cup_board',
# #        'floor', 'total_floor', 'water_supply', 'building_type', 'balconies',
# #        'day', 'month', 'year']
# col1, col2 = st.columns(2, gap='large')
#
# with col1:
#     selected_type = st.selectbox("Select the Flat type", df['type'].value_counts().index)
#     selected_locality = st.selectbox("Select the Location", df['locality'].value_counts().index)
#     selected_latitude = st.text_input("Enter Latitude Number")
#     selected_longitude = st.text_input("Enter Longitude Number")
#     Lease_type = st.selectbox("Product Reference", lease_types, key='lease_type')
#     GYM = st.text_input('Enter Number of GYM')
#     LIFT = st.text_input('Enter Number of Lifts available')
#     Swimming_pool = st.text_input('Enter number of Swimming_pool available')
#     Negotiable = st.text_input('Select Negotiation', Negotiation)
#     Furnishing = st.selectbox("Furnish type", Furnish, key='furnishing')
#     Parking = st.text_input("No. of Parking avail")
#     Size =  st.text_input("Enter Size of Property")
#     Property_age = st.text_input("Enter Property_age")
#
#
# with col2:
#     bathroom = st.text_input("Enter No.of Bathrooms")
#     Facing =  st.selectbox("Side of Facing", df['facing'].value_counts().index, key='facing')
#     Cup_boards = st.text_input("Cup_boards")
#     Floor =  st.text_input("No.of Floors")
#     Total_floor = st.text_input("Total_Floors")
#     Water_supply = st.selectbox("Enter type of water supply", df['water_supply'].value_counts().index, key='water_supply')
#     Building_type = st.selectbox("Enter type of Building", df['building_type'].value_counts().index, key='building_type')
#     Balconies =  st.selectbox("Enter type of Building", df['balconies'].value_counts().index, key='balconies')
#
