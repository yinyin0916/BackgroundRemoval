import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from pyecharts.charts import Bar
from pyecharts import options as opts
import streamlit.components.v1 as components
import cv2

st.set_page_config(layout="wide", page_title="Vis Your MoT Model!")

st.write("## 👀Visualize your model performance")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


st.sidebar.write("## Upload and download :gear:")

if 'page' not in st.session_state:
    st.session_state.page = 1 

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload your model outcome", type=["txt"])

video_options = [f'Video{i}' for i in range(1, 15)]
dict_video = {1: 450, 2: 600, 3: 1500, 4: 1050, 5: 837, 6: 1194, 7: 500, 8: 625, 9: 525, 10: 654, 11: 900, 12: 900, 13: 750, 14: 750}



video = st.sidebar.selectbox(
    'Video You Want To Explore',
    video_options,
    index=0,
)
no_frames = dict_video[int(video[5:])]

values = st.slider(
    'Select a range of values',
    0, no_frames, (0, no_frames), key='values'
)

st.write('Values:', values)

# upload:txt file, video_no: video, values: start and end frame
def generate_image(upload, video_no, values):
    train_no = [2,4,5,9,10,11,13]
    test_no = [1,3,6,7,8,12,14]
    text_file_path = f"/MOT16/test/MOT16-{str(video_no[5:]).zfill(2)}/det/det.txt"
    if int(video_no[5:]) in train_no:
        text_file_path = f"/MOT16/train/MOT16-{str(video_no[5:]).zfill(2)}/det/det.txt"
    col1.write("Your Model MoT")
    # col1.image(image)

    # fixed = remove(image)
    col2.write("? MoT")
    # col2.image(fixed)
    st.sidebar.markdown("\n")
    # st.sidebar.download_button("Download visualization", convert_image(fixed), "fixed.png", "image/png")

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    # else:
        # fix_image(upload=my_upload)
# else:
    # fix_image("./zebra.jpg")




c = (Bar()
        # TODO: metric name
.add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
    # TODO: metric value
.add_yaxis('2017-2018 Revenue in (billion $)', [21.2, 20.4, 10.3, 6.08, 4, 2.2])
.set_global_opts(title_opts=opts.TitleOpts(title="Top cloud providers 2018", subtitle="2017-2018 Revenue"),
                    toolbox_opts=opts.ToolboxOpts())
.render_embed() # generate a local HTML file
)
components.html(c, width=1000, height=1000)

