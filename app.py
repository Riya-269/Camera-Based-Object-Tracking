import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Image as ImageModel

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Camera Based Object Tracking")

st.image('title_img_.jpg')
st.header("Real time object recognition using a webcam and deep learning....")
st.markdown("---")
sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["Project Overwiew", "Upload Image", "Create Mask"]
selOpt = sidebar.selectbox("Choose What to do?", choices)


def intro():
    pass


def saveImage():
    img_name = st.text_input("Enter name of Image")
    img_file = st.file_uploader("Upload your Image")
    if img_file:

        img = Image.open(img_file)
        st.image(img)
        btn = st.button("Save Image")

        if btn:
            try:
                # to save image file in uploads folder
                path = "uploads/"+img_name+".png"
                img.save(path)

                # to save image in database
                img_data = ImageModel(name=img_name, filename=path)
                sess.add(img_data)
                sess.commit()

                st.success("Image Saved")
            except:
                st.error('Something went wrong')


def createMask():
    st.header("Choose the Image to create mask")
    images_data = sess.query(ImageModel).all()

    image_names = [image.name for image in images_data]
    selName = st.selectbox(options=image_names, label="Choose Image")

    create_mask_btn = st.button("Create Mask")


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    saveImage()
elif selOpt == choices[2]:
    createMask()
