import os
import sys
import streamlit as st
from PIL import Image
from zlai.utils import get_file_encoding

obj_path = __file__
app_path = os.path.dirname(obj_path)
if app_path not in sys.path:
    sys.path.insert(0, app_path)


st.set_page_config(
    page_title="ZLAI",
    page_icon=":robot:",
    layout='centered',
    initial_sidebar_state='expanded',
)


def main():
    path = os.path.join(app_path, './markdown/home.md')
    encoding = get_file_encoding(path)
    with open(path, encoding=encoding) as f:
        home_data = f.read()
    for md in home_data.split("<img>"):
        if "img/" in md:
            img_info = eval(md)
            image_path = img_info.get("path")
            image = Image.open(image_path)
            title = img_info.get("title")
            if img_info.get("expander"):
                with st.expander(title):
                    st.image(image)
            else:
                st.image(image)
        else:
            st.markdown(md, unsafe_allow_html=True)


if __name__ == "__main__":
    st.header('_:blue[模型展示页面]_ :sunglasses:', divider='rainbow')
    main()

# streamlit run ./apply/app.py
# nohup streamlit run Home.py --server.port 6503 --server.headless true --server.fileWatcherType none > app.log 2>&1 &
# nohup streamlit run Home.py --server.port 6503 --server.fileWatcherType none > app.log 2>&1 &
