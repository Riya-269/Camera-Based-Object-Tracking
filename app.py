from altair.vegalite.v4.api import value
import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Image as ImageModel
import cv2

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

    col1, col2 = st.beta_columns(2)
    org_img = col1.image([])

    col3, col4 = st.beta_columns(2)
    col3.slider(label="v1_min", max_value=255)
    col3.slider(label="v2_min", max_value=255)
    col3.slider(label="v3_min", max_value=255)

    col4.slider(label="v1_max", max_value=255, value=255)
    col4.slider(label="v2_max", max_value=255, value=255)
    col4.slider(label="v3_max", max_value=255, value=255)

    if selName:
        path = sess.query(ImageModel).filter_by(name=selName).first().filename
        org_img.image(path)
    create_mask_btn = st.checkbox("Create Mask")

    if create_mask_btn:
        pass
        # thresh = cv2.inRange(
        #     frame_to_thresh,
        #     (sliders["v1_min"], sliders["v2_min"], sliders["v3_min"]),
        #     (sliders["v1_max"], sliders["v2_max"], sliders["v3_max"]),
        # )


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    saveImage()
elif selOpt == choices[2]:
    createMask()
