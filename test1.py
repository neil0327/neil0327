from reportlab.pdfgen import canvas
from PIL import Image
import qrcode
from PyPDF2 import PdfFileMerger
import streamlit as st
import base64
import os
first_list=['42','44','45','46','01','02']
folder_path = 'folder'
try:
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 处理 PDF 文件
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)  # 删除文件
    
    st.title('Registration QR codes')
    input_i = st.text_input("Input serial numbers or UDI (e.g. 42220001,44230010-44230020,45210001)")
    input=input_i.replace(" ", "")
    def create_pdf(begin,final):

        merger = PdfFileMerger()
        tp=0
        mode=0
        ModelName = ""
        if len(begin)==8:
            mode=1
            begin_prefix = begin[:2]
            
            if begin_prefix == '42':
                ModelName = "MVR Lite"
            elif begin_prefix == '44':
                ModelName = "MVR Pro"
            elif begin_prefix == '45':
                ModelName = "MVC Pro SDI to HDMI"
            elif begin_prefix == '46':
                ModelName = "MVR"
            elif begin_prefix == '01':
                ModelName = "MTS101"
            elif begin_prefix == '02':
                ModelName = "MTS156"
            else:
                #print("wrong")
                tp=1
        elif len(begin)>=29:
            mode=2
            begin_prefix = begin[13:16]
            if begin_prefix == '057':
                ModelName = "MTS156"
            elif begin_prefix == '286':
                ModelName = "MTS101"
            elif begin_prefix == '132':
                ModelName = "MVR"
            elif begin_prefix == '156':
                ModelName = "MVC Pro SDI to HDMI"
            elif begin_prefix == '101':
                ModelName = "MVR Pro"
            elif begin_prefix == '033':
                ModelName = "MVR Lite"
            else:
                tp=1
        elif len(begin)==3:
            mode=3
            ModelName="MTS101"
        #print("ModelName:", ModelName)
    
    
        begin_num = int(begin) 
        final_num = int(final) 
    
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
            if mode==1:
                data = f"www.medicapture.com/register/?serial={begin_num+i}"
                if begin_prefix == '01' or begin_prefix == '02':
                    data = f"www.medicapture.com/register/?serial=0{begin_num+i}"
                else:
                    data = f"www.medicapture.com/register/?serial={begin_num+i}"
            elif mode==2:
                data = f"www.medicapture.com/register/?serial=0{begin_num+i}"
            elif mode==3:
                if begin_num+i<10:
                    data = f"www.medicapture.com/register/?serial=00{begin_num+i}"
                elif begin_num+i<100:
                    data = f"www.medicapture.com/register/?serial=0{begin_num+i}"
                elif begin_num+i<1000:
                    data = f"www.medicapture.com/register/?serial={begin_num+i}"








            
            qr.add_data(data)
            qr.make(fit=True)
            # 生成图像
            qr_image = qr.make_image(fill_color="black", back_color="white")
        
            # 保存图像到文件
            qr_image.save(f"qrcode{begin_num+i}.png")
        
            pdf = canvas.Canvas(f"{begin_num+i}.pdf")
        
            # 设置字体样式和大小
            pdf.setFont("Helvetica", 45)
        
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
        
            pdf.setFont("Helvetica", 32)
            pdf.drawString(text_x, text_y - 50*5, "Unlock 2 Months of Extra Warranty")
        
            pdf.setFont("Helvetica", 13)
            pdf.drawString(text_x, text_y - 50*6.5, "Scan the QR Code to register your new")
            pdf.drawString(text_x, text_y - 50*6.5-20, f"MediCapture {ModelName}")
            pdf.drawString(text_x, text_y - 50*6.5-20*3, "or browse to the link below:")
            if mode==1:
                if begin_prefix == '01' or begin_prefix == '02':
                    pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial=0{begin_num+i}")
                else:
                    pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial={begin_num+i}")
                
            elif mode==2:
                pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial=")
                pdf.drawString(text_x, text_y - 50*6.5-20*5, f"0{begin_num+i}")
            elif mode==3:
                if begin_num+i<10:
                    pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial=00{begin_num+i}")
                elif begin_num+i<100:
                    pdf.drawString(text_x, text_y - 50*6.5-20*4, f"www.medicapture.com/register/?serial=0{begin_num+i}")
                elif begin_num+i<1000:
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
        merger_filename = f"{begin}-{final}.pdf"
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
    
    
        with open(f'{begin}-{final}.pdf', 'rb') as file:
            pdf_data = file.read()
    
    # Convert the PDF data to base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        return pdf_base64


    begin_list=[]
    final_list=[]
    pdf_list=[]


    # Create a download button
    st.write("")
    if st.button('Generate'):
        temp1=input.split(',')
        for i in temp1:
            if (len(i)==8 or len(i)>=29 or len(i)==3) and i.isdigit() and ((i[:2] in first_list and len(i)==8) or i[0:13]=='0100859151005' or len(i)==3):
                begin=i
                final=i
                begin_list.append(begin)
                final_list.append(final)
                pdf_list.append(create_pdf(begin,final))
            elif '-' in i:
                i_split=i.split('-')
                if len(i_split) == 2 and i_split[0].isdigit() and i_split[1].isdigit() and ((len(i_split[0]) == 8 or len(i_split[0])>=29) and (len(i_split[1]) == 8 or len(i_split[1])>=29) and ((i_split[0][:4]==i_split[1][:4] and i_split[0][:2] in first_list and len(i_split[0])==8) or i_split[0][0:13]=='0100859151005') or (len(i_split[0])==3 and len(i_split[1])==3)):
                    if int(i_split[1])-int(i_split[0])<=200 and int(i_split[1])-int(i_split[0])>0:
                        begin=i_split[0]
                        final=i_split[1]
                        begin_list.append(begin)
                        final_list.append(final)
                        pdf_list.append(create_pdf(begin,final))
                    elif int(i_split[0])-int(i_split[1])<=200 and int(i_split[1])-int(i_split[0])<=0:
                        begin=i_split[1]
                        final=i_split[0]
                        begin_list.append(begin)
                        final_list.append(final)
                        pdf_list.append(create_pdf(begin,final))
                    else:
                        st.write(f'Exceeding the maximum of 200 serial numbers: {i_split[0]}-{i_split[1]}')
                else:
                    st.write(f'Wrong serial number: {i_split[0]}-{i_split[1]}')
            else:
                st.write(f'Wrong serial number: {i}')
        
            # Generate download link
        for j in range(len(begin_list)):
            if begin_list[j]!=final_list[j]:
                href = f'<a href="data:application/pdf;base64,{pdf_list[j]}" download="{begin_list[j]}-{final_list[j]}.pdf">Download {begin_list[j]}-{final_list[j]}.pdf</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                href = f'<a href="data:application/pdf;base64,{pdf_list[j]}" download="{begin_list[j]}.pdf">Download {begin_list[j]}.pdf</a>'
                st.markdown(href, unsafe_allow_html=True)
except Exception as e:
    st.error(e)
