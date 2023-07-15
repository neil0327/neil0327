from reportlab.pdfgen import canvas
from PIL import Image
import qrcode
from PyPDF2 import PdfFileMerger
import streamlit as st
import base64
import os
import random

first_list = ['42', '44', '45', '46']
folder_path = 'folder'


def create_pdf(begin, final):
    # 省略部分代码

# 在 Streamlit 应用程序中调用雪花特效
def run_snow_effect():
    st.title("Registration QR codes")
    input_i = st.text_input("Input serial numbers (e.g. 42220001,44230010-44230020,45210001)")
    input_val = input_i.replace(" ", "")
    
    if st.button("Generate"):
        with st.spinner("Generating PDF files..."):
            temp1 = input_val.split(',')
            begin_list = []
            final_list = []
            pdf_list = []

            for i in temp1:
                # 省略部分代码

                if begin_list[j] != final_list[j]:
                    href = f'<a href="data:application/pdf;base64,{pdf_list[j]}" download="{begin_list[j]}-{final_list[j]}.pdf">Download {begin_list[j]}-{final_list[j]}.pdf</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    href = f'<a href="data:application/pdf;base64,{pdf_list[j]}" download="{begin_list[j]}.pdf">Download {begin_list[j]}.pdf</a>'
                    st.markdown(href, unsafe_allow_html=True)

# 运行 Streamlit 应用程序
if __name__ == '__main__':
    run_snow_effect()
