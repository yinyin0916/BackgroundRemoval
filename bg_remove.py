import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64
from pyecharts.charts import Bar
from pyecharts import options as opts
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Vis Your MoT Model!")

st.write("## 👀Visualize your model performance")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

PAGES = ['Video1', 'Video2']

st.sidebar.write("## Upload and download :gear:")

if 'page' not in st.session_state:
    st.session_state.page = 1 

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload your model outcome", type=["txt"])

page = st.sidebar.radio('Video you Want to Explore', PAGES, index=st.session_state.page)
# st.write(f"{page}")

def fix_image(upload):
    image = Image.open(upload)
    col1.write("Your Model MoT")
    col1.image(image)

    fixed = remove(image)
    col2.write("? MoT")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download visualization", convert_image(fixed), "fixed.png", "image/png")

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(upload=my_upload)
else:
    fix_image("./zebra.jpg")




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
