import streamlit as st

st.title("Camera Based Object Tracking")

st.image('title_img_.jpg')
st.header("Real time object recognition using a webcam and deep learning....")

sidebar = st.sidebar

sidebar.header("Choose your option")
choises = ["veiw image"]
selopt = sidebar.selectbox("Choices")


def saveImage():
    
