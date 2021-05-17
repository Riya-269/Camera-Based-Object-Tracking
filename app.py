import streamlit as st

st.title("Camera Based Object Tracking")

st.image('title_img_.jpg')
st.header("Real time object recognition using a webcam and deep learning....")

sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["veiw image"]
selOpt = sidebar.selectbox("Choices")

def saveImage():
    img_name = st.text_input("Enter name of Image")
    img_file = st.file_uploader("Upload your Image")


    img = Image.open(img_file)

    btn = st.button("Save Image")


if selOpt == choices[0]:
    saveImage()    