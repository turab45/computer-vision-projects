import streamlit as st
import mediapipe as mp 
import cv2
from PIL import Image 
import numpy as np
import tempfile
import time

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

DEMO_IMAGE = 'demo.jpg'
DEMO_VIDEO = 'demo.mp4'

st.title('Face Mesh App using MediaPipe')

st.markdown('''
    <style>
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
        }
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
            margin-left:-350px;
        }
    </style>
''', unsafe_allow_html=True)

st.sidebar.title('FaceMesh Sidebar')
st.sidebar.subheader('parameters')

@st.cache()
def resize(image, width=None, height=None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image
    
    if width is None:
        r = width/float(w)
        dim = (int(w*r), height)
    else:
        r = width/float(w)
        dim = (width, int(h*r))
    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

app_mode = st.sidebar.selectbox('Choose the app mode',
                                ['About App', 'Run on Image', 'Run on Video'])

if app_mode == 'About App':
    st.markdown('''
    <style>
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
        }
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
            margin-left:-350px;
        }
    </style>
''', unsafe_allow_html=True)
    st.markdown('In this app we are using **MediaPipe** for creating **FaceMesh** application.')
elif app_mode == 'Run on Image':
    st.markdown('''
    <style>
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
        }
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
            margin-left:-350px;
        }
    </style>
''', unsafe_allow_html=True)
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')
    st.markdown('**Detected Faces**')
    kpi1_text = st.markdown('8')
    max_faces = st.sidebar.number_input('Number of faces to detect', min_value=1, value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Detection confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')
    
    img_file_buffer = st.sidebar.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))
    else:
        image = np.array(Image.open(DEMO_IMAGE))
    
    st.sidebar.text('Original image')
    st.sidebar.image(image)

    # Dashboard
    face_count = 0

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=max_faces,
        min_detection_confidence=detection_confidence,
    ) as face_mesh:

        results = face_mesh.process(image)
        out_image = image.copy()
    # Face landmarks drawing
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                face_count += 1

                mp_drawing.draw_landmarks(
                    image=out_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec)
            
                kpi1_text.write(f'<h1 style="text-align:center;color:red">{face_count}</h1>', unsafe_allow_html=True)
            st.subheader('Output image')
            st.image(out_image, use_column_width=True)
        else:
            kpi1_text.write('<h1 style="text-align:center;color:red">No faces detected.</h1>', unsafe_allow_html=True)

elif app_mode == 'Run on Video':
    st.markdown('''
    <style>
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
        }
        [data-tested="stSidebar"][aria-expanded="true"] > div.first-child{
            width:350px;
            margin-left:-350px;
        }
    </style>
''', unsafe_allow_html=True)
    st.set_option('deprecation.showfileUploaderEncoding', False)

    user_webcam = st.sidebar.button('Use webcam')
    record = st.sidebar.checkbox(label='Record video')
    if record:
        st.checkbox('Recording', value=True)
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')
    
    max_faces = st.sidebar.number_input('Number of faces to detect', min_value=1, value=5)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Detection confidence', min_value=0.0, max_value=1.0, value=0.5)
    tracking_confidence = st.sidebar.slider('Tracking confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    st.markdown('## Output')

    stframe = st.empty()
    video_file_buffer = st.sidebar.file_uploader('Upload a video', type=['mp4','mov','avi','asf','m4v'])
    tffile = tempfile.NamedTemporaryFile(delete=False)

    if not video_file_buffer:
        if user_webcam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tffile.name = DEMO_VIDEO
    else:
        tffile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tffile.name)
    
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

    # Recording part
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('output1.mp4', codec, fps_input,(width, height))

    st.sidebar.text('Input Video')
    st.sidebar.video(tffile.name)

    fps = 0
    i = 1

    # columns to show the fps, no of faces & iterations
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown('**Frame Rate**')
        kpi1_text = st.markdown('0')
    with kpi2:
        st.markdown('**Frame Rate**')
        kpi2_text = st.markdown('0')
    with kpi3:
        st.markdown('**Frame Rate**')
        kpi3_text = st.markdown('0')

    # FaceMesh predictor

    with mp_face_mesh.FaceMesh(
        max_num_faces=max_faces,
        min_detection_confidence=detection_confidence,
        min_tracking_confidence=tracking_confidence
    ) as face_mesh:
        prevTime = 0

        while vid.isOpened():
            i+=1
            ret, frame = vid.read()
            if not ret:
                continue

            results = face_mesh.process(frame)
            frame.flags.writeable = True

            face_count = 0                
        # Face landmarks drawing
            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    face_count += 1

                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
                
            currentTime = time.time()
            fps = 1/(currentTime - prevTime)
            prevTime = currentTime

            if record:
                out.write(frame)
            
            # Dashboard
            kpi1_text.write(f'<h1 style="text-align:center;color:red">{int(fps)}</h1>', unsafe_allow_html=True)
            kpi2_text.write(f'<h1 style="text-align:center;color:red">{face_count}</h1>', unsafe_allow_html=True)
            kpi3_text.write(f'<h1 style="text-align:center;color:red">{width}</h1>', unsafe_allow_html=True)

            frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
            frame = resize(frame, width=648)
            stframe.image(frame, channels='BGR', use_column_width=True)

    st.text('Processed Video')
    output_video = open('output1.mp4','rb')
    out_bytes = output_video.read()
    st.video(out_bytes)

    vid.release()
    out.release()


        #st.image(out_image, use_column_width=True)
        #else:
        #kpi1_text.write('<h1 style="text-align:center;color:red">No faces detected.</h1>', unsafe_allow_html=True)

    
        