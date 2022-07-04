import streamlit as st
import mediapipe as mp 
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

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
    st.markdown('In this app we are using **MediaPipe** for creating **FaceMesh** application.')
elif app_mode == 'Run on Image':
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')
    st.markdown('**Detected Faces**')

    max_faces = st.sidebar.number_input('Number of faces to detect', min_value=1, value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Detection confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')
    