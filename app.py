import streamlit as st
from PIL import Image

st.title("Camera Based Object Tracking")

st.image('title_img_.jpg')
st.header("Real time object recognition using a webcam and deep learning....")
st.markdown("---")
sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["veiw image"]
selOpt = sidebar.selectbox("Choose What to do?", choices)

def saveImage():
    img_name = st.text_input("Enter name of Image")
    img_file = st.file_uploader("Upload your Image")
    if img_file:

        img = Image.open(img_file)
        st.image(img)

    btn = st.button("Save Image")

    if btn:
        try:
            img.save("uploads/"+img_name+".png")
            st.success("Image Saved")
        except:
            st.error('Something went wrong')

            
if selOpt == choices[0]:
    saveImage()    