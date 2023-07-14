from reportlab.pdfgen import canvas
from PIL import Image
import qrcode
from PyPDF2 import PdfFileMerger
import streamlit as st
import base64
import os

folder_path = 'folder'


# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 处理 PDF 文件
    if filename.endswith('.pdf'):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)  # 删除文件



merger = PdfFileMerger()

begin = st.text_input("begin:")
final = st.text_input("final:")

# 提取前两位数字
begin_prefix = begin[:2]
final_prefix = final[:2]
ModelName = ""
tp=0

if begin_prefix == '42':
    ModelName = "MVR Lite"
elif begin_prefix == '44':
    ModelName = "MVR Pro"
elif begin_prefix == '45':
    ModelName = "MVC Pro SDI to HDMI"
elif begin_prefix == '46':
    ModelName = "MVR"
else:
    #print("wrong")
    tp=1

#print("ModelName:", ModelName)


begin_num = int(begin) if begin.isdigit() else 0
final_num = int(final) if final.isdigit() else 0

i=0

# 创建PDF文件对象
while begin_num+i<=final_num and tp==0 :
    #print(begin_num+i)
    
    qr = qrcode.QRCode(
        version=1,  # 控制QR码的大小，范围为1到40
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 控制错误纠正级别
        box_size=10,  # 控制每个“盒子”的像素数
        border=4,  # 控制边框的盒子数
    )
    data = f"www.medicapture.com/register/?serial={begin_num+i}"
    qr.add_data(data)
    qr.make(fit=True)
    # 生成图像
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # 保存图像到文件
    qr_image.save(f"qrcode{begin_num+i}.png")

    pdf = canvas.Canvas(f"{begin_num+i}.pdf")

    # 设置字体样式和大小
    pdf.setFont("Times-Roman", 45)

    # 打开图像
    image = Image.open("medicapture-android-chrome-favicon_512x512.png")

    # 将图像转换为RGBA模式
    image = image.convert("RGBA")

    # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的空白图像，背景为白色
    new_image = Image.new("RGBA", (width, height), (255, 255, 255))

    # 将原始图像粘贴到新的图像上，仅保留不透明部分
    new_image.paste(image, (0, 0), mask=image)

    # 保存处理后的图像为临时文件
    temp_file = "temp.png"
    new_image.save(temp_file)

    # 获取图像在PDF中的大小和位置
    image_width = 200
    image_height = 200
    x = 60  # 左上角的x坐标
    y = 820 - image_height  # 左上角的y坐标

    # 放置处理后的图像
    pdf.drawImage(temp_file, x, y, width=image_width, height=image_height)

    # 放置QR码图像
    qr_x = x + 300
    qr_y = y -50*9-15*4
    pdf.drawImage(f"qrcode{begin_num+i}.png", qr_x, qr_y, width=200, height=200)

    # 写入文本内容
    text_x = x
    text_y = y - 40  # 将文本下移20个单位
    pdf.drawString(text_x, text_y, "Congratulations on")
    pdf.drawString(text_x, text_y - 50, "your new MediCapture")
    pdf.drawString(text_x, text_y - 50*2, ModelName)

    pdf.setFont("Times-Roman", 35)
    pdf.drawString(text_x, text_y - 50*5, "Unlock 2 Months of Extra Warranty")

    pdf.setFont("Times-Roman", 15)
    pdf.drawString(text_x, text_y - 50*6.5, "Scan the QR Code to register your new")
    pdf.drawString(text_x, text_y - 50*6.5-20, f"MediCapture {ModelName}")
    pdf.drawString(text_x, text_y - 50*6.5-20*3, "or browse to the link below:")
    pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial={begin_num+i}")

    pdf.drawImage("bottom.png", 100, 0, 500, 50)


    # 删除临时文件
    import os
    os.remove(temp_file)


    # 删除QR码图像文件
    os.remove(f"qrcode{begin_num+i}.png")

    # 保存并关闭PDF文件
    pdf.save()
    i=i+1

i = 0

while begin_num + i <= final_num and tp == 0:
    # 将PDF文件添加到合并器中
    merger.append(f"{begin_num+i}.pdf")
    i = i + 1


# 合并所有PDF文件
merger_filename = f"{begin}to{final}.pdf"
merger.write(merger_filename)
merger.close()
if begin_num!=0:
    print("PDF files merged successfully into", merger_filename)


i=0
if begin_num!=0 and tp==0:
    while begin_num + i <= final_num :
        import os
        os.remove(f"{begin_num+i}.pdf")
        i=i+1


with open(f'{begin}to{final}.pdf', 'rb') as file:
    pdf_data = file.read()

# Convert the PDF data to base64
pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

# Create a download button
st.write("")
if st.button('Generate Download Link'):
    if begin_num!=0 and final_num!=0:
        # Generate download link
        href = f'<a href="data:application/pdf;base64,{pdf_base64}" download="{begin}to{final}.pdf">Click here to download PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

import os
if begin_num==0 and final_num==0:
    os.remove("to.pdf")
elif begin_num!=0 and final_num==0:
    os.remove(f"{begin}to.pdf")
elif begin_num==0 and final_num!=0:
    os.remove(f"to{final}.pdf")
