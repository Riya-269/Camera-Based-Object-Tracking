from altair.vegalite.v4.api import value
from imutils import video
import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Image as ImageModel, Mask as MaskModel, Video as VideoModel
import cv2
import tempfile
from masking import Object_Tracker

engine = create_engine('sqlite:///db.sqlite3?check_same_thread=False')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("CAMERA BASED OBJECT TRACKING")

st.image('title_img_.jpg')
st.header("Real time object recognition using a webcam and deep learning....")
st.markdown("---")
sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["Project Overwiew", "Upload Image",
           "Create Mask", "Upload Video", "Track Object with Video", "Track object with webcam"]
selOpt = sidebar.selectbox("Choose What to do?", choices)


def intro():
    st.subheader("INRODUCTION")
    st.markdown("""Camera based object tracking is the process of locating a moving object  over time using a camera. Video tracking can be a time-consuming process due to the amount of data that is contained in video. Adding further to the complexity is the possible need to use object recognition techniques for tracking, a challenging problem in its own right.The objective of video tracking is to associate target objects in consecutive video frames. The association can be especially difficult when the objects are moving fast relative to the frame rate. Another situation that increases the complexity of the problem is when the tracked object changes orientation over time.""")

    st.subheader("For Example:")

    col1, col2 = st.beta_columns(2)

    col1.image('example.mp5.gif')

    col2.markdown("""
    ### STEP 1. Upload image of the object which you want to track.
    ### STEP 2. Create mask of the image.
    ### STEP 3. Upload the video which have a object to track.
    ### STEP 4. Track the object with the video.
    """)


def saveVideo():
    vid_name = st.text_input("Enter name of Video")                                                                            
    vid_file = st.file_uploader("Upload your Video")
    btn = st.button("Submit")

    if vid_file:
        t_file = tempfile.NamedTemporaryFile(delete=False)
        t_file.write(vid_file.read())

        if btn and vid_name:
            with st.spinner("Saving your Video ..."):
                try:
                    cap = cv2.VideoCapture(t_file.name)
                    ret, frame = cap.read()
                    shape = frame.shape
                    codec = cv2.VideoWriter_fourcc(*"XVID")
                    vid_path = "uploads/"+vid_name+".mp4"
                    out = cv2.VideoWriter(
                        vid_path, codec, 30, (shape[1], shape[0]))
                    while ret:
                        out.write(frame)

                        ret, frame = cap.read()

                    cap.release()
                    out.release()

                    # to save image in database
                    vid_data = VideoModel(name=vid_name, filename=vid_path)
                    sess.add(vid_data)
                    sess.commit()

                    st.success('Video Successfully Saved')
                except Exception as e:
                    print(e)
                    st.error('An error occured')


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
    mask_img = col2.image([])

    if selName:
        path = sess.query(ImageModel).filter_by(name=selName).first().filename

        hsv_image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2HSV)
        org_img.image(path)
        create_mask_btn = st.checkbox("Create Mask")
        mask_name = st.text_input('Mask Name')
        save_btn = st.button('Save Mask')

        if create_mask_btn:
            col3, col4 = st.beta_columns(2)
            v1_min = col3.slider(label="v1_min", max_value=255)
            v2_min = col3.slider(label="v2_min", max_value=255)
            v3_min = col3.slider(label="v3_min", max_value=255)

            v1_max = col4.slider(label="v1_max", max_value=255, value=255)
            v2_max = col4.slider(label="v2_max", max_value=255, value=255)
            v3_max = col4.slider(label="v3_max", max_value=255, value=255)

            while create_mask_btn:
                thresh = cv2.inRange(
                    hsv_image,
                    (v1_min, v2_min, v3_min),
                    (v1_max, v2_max, v3_max),
                )
                mask_img.image(thresh)

                if save_btn:
                    try:
                        # to save image file in uploads folder
                        mask_path = "uploads/mask_"+mask_name+".png"
                        cv2.imwrite(mask_path, thresh)

                        mask_values_string = f"{str(v1_min)} {str(v2_min)} {str(v3_min)} {str(v1_max)} {str(v2_max)} {str(v3_max)}"

                        # to save image in database
                        img_data = MaskModel(
                            name=mask_name, filename=mask_path, orgimage=path, mask_values=mask_values_string)
                        sess.add(img_data)
                        sess.commit()

                        st.success("Masked Image Saved")
                    except Exception as e:
                        st.error('Something went wrong')
                        print(e)
                    break


def trackObject():
    images = sess.query(MaskModel).all()
    videos = sess.query(VideoModel).all()

    col1, col2 = st.beta_columns(2)

    selImage = col1.selectbox(
        options=[image.name for image in images], label="Select Mask")
    selVideo = col2.selectbox(
        options=[video.name for video in videos], label="Select Video")

    imgObj = sess.query(MaskModel).filter_by(name=selImage).first()
    vidObj = sess.query(VideoModel).filter_by(name=selVideo).first()

    mask_values = tuple(map(int, imgObj.mask_values.split()))
    col1.image(imgObj.filename)
    col1.image(imgObj.orgimage)
    btn = st.checkbox('Start Tracking')
    window = st.image([])
    if btn:
        track = Object_Tracker(greenLower=mask_values[:3], greenUpper=mask_values[3:], video=vidObj.filename)

        frameGen = track.trackObject()
        while True:
            try:
                if not next(frameGen).any():
                    print('frames ended')
                    break
                frame = next(frameGen)
                window.image(frame)
            except Exception as e:
                print(e)
                # st.error('Somthing went wrong')
                break


def trackObjectWebcam():
    images = sess.query(MaskModel).all()

    selImage = st.selectbox(
        options=[image.name for image in images], label="Select Mask")

    imgObj = sess.query(MaskModel).filter_by(name=selImage).first()
    st.image(imgObj.filename)

    mask_values = tuple(map(int, imgObj.mask_values.split()))
    st.write(imgObj.mask_values)
    btn = st.checkbox('Start Tracking')
    window = st.image([])
    if btn:
        st.text(imgObj)
        frame = tracker(
            greenLower=mask_values[:3], greenUpper=mask_values[3:])
        while next(frame).any():
            window.image(next(frame))


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    saveImage()
elif selOpt == choices[2]:
    createMask()
elif selOpt == choices[3]:
    saveVideo()
elif selOpt == choices[4]:
    trackObject()
elif selOpt == choices[5]:
    trackObjectWebcam()
