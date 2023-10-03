import cv2
import imutils
import numpy as np
import pandas as  pd
import os

from imutils import perspective
from pdf2image import convert_from_path

poppler_store_path =  os.getcwd() + r'\poppler-23.01.0\Library\bin'


def rotate_img(img_folder):
  rotate_degree = 0
  im1 = cv2.imread(img_folder)
  im1_height,im1_weight = im1.shape[:2]
  im_reg = im1
  #print('im1_height = ',im1_height,'im1_weight',im1_weight) 
  if im1_height < im1_weight :
    im_reg = cv2.rotate(im1, cv2.ROTATE_90_CLOCKWISE) #ROTATE_90
    rotate_degree = 90

  im1 = im_reg
  im1_hsv = cv2.cvtColor(im1,cv2.COLOR_BGR2RGB)
  im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(im1_gray, (3, 3), 0)
  blurred=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,2)
  blurred=cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))
  #cv2_imshow(blurred)
  edged = cv2.Canny(blurred, 10, 100)
  cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy       CV4
  #findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> image, contours, hierarchy   CV3.4
  cnts = cnts[1] if imutils.is_cv2() else cnts[0]
  docCnt = None

  # 确保至少有一个轮廓被找到
  if len(cnts) > 0:
    # 将轮廓按大小降序排序
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # 对排序后的轮廓循环处理
    for c in cnts:
        # 获取近似的轮廓
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        # 如果近似轮廓有四个顶点，那么就认为找到了答题卡
        if len(approx) == 4:
            docCnt = approx
            break
  newim1=im1.copy()

  for i in docCnt:
    #circle函数为在图像上作图，新建了一个图像用来演示四角选取
    cv2.circle(newim1, (i[0][0],i[0][1]), 10, (255, 0, 0), -1)
  #cv2_imshow(newim1)
  paper = perspective.four_point_transform(im1, docCnt.reshape(4, 2))
  warped = perspective.four_point_transform(im1_gray, docCnt.reshape(4, 2))

  im_reg =  paper

  width1 = 2400
  height1 = 2800

  # 对灰度图应用二值化算法
  thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,101,2)
  #重塑可能用到的图像
  thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
  paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
  warped = cv2.resize(warped, (width1, height1), cv2.INTER_LANCZOS4)
  #均值滤波
  ChQImg = cv2.blur(thresh, (23, 23))
  #二进制二值化
  ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]

  cnts,hierarchy  = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #cnts,hierarchy  = cv2.findContours(warped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
  hierarchy = hierarchy[0]
  #cnts = cnts[1] if imutils.is_cv2() else cnts[0]
  rect_count = 0
  #cv2_imshow(ChQImg)
  for component in zip(cnts, hierarchy):   ## rotate to correct direction
    currentContour = component[0] 
    currentHierarchy = component[1] 
    (x,y,w,h) = cv2.boundingRect(currentContour) 
    
    if currentHierarchy[2] < 0 and x<250 and y>2600 and 200 > w > 100 and 200 > h > 100 :  
    #if x<250 and y>2600 and 200 > w > 100 and 200 > h > 100 : # 因為用主動濾波 adaptiveThreshold 所以全黑的色塊 中間會變成白色
      #print(rotate_degree)
      #cv2_imshow(im_reg)
      rotate_degree = rotate_degree + 180
      # these are the innermost child components 
      #print("site","X=",x,"Y=",y,"W=",w,"H=",h,"rect_count=",rect_count)
      #cv2.rectangle(paper,(x,y),(x+w,y+h),(0,0,255),3)
      #cv2.putText(paper, str(rect_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)
      #im_reg = cv2.rotate(paper, cv2.ROTATE_180)
      #rect_count = rect_count +1 
  #im1 = im_reg
  return rotate_degree


#左側選項1左邊框X245 右側選項1左邊框X1345
#學號選項1上邊框Y185 答案選項1上邊框Y715

#X間距78.63
#Y間距69.07

student_rows = 7 
L_ans_rows = 30 
R_ans_rows = 30 

student_cols = 10 
L_ans_cols = 12 
R_ans_cols = 12 

if 1:
  pdf_mode = 1  #student_num_bound ques_left_bound ques_right_bound
  mode = 3
  x_mod = 77.2
  y_mod = 68.2
  x_left = 245
  x_right = 1330
  y_top = 165
  y_bottom = 690

  left_region_margin = [(x_left),(x_left + x_mod * L_ans_cols)]
  top_region_margin = [(y_top),(y_top + y_mod * student_rows)]
else:
  pdf_mode = 1 #student_num_bound ques_left_bound ques_right_bound
  mode = 3
  x_mod = 79
  y_mod = 70
  x_left = 215
  x_right = 1340
  y_top = 130
  y_bottom = 670

  left_region_margin = [(x_left),(x_left + x_mod * L_ans_cols)]
  top_region_margin = [(y_top),(y_top + y_mod * student_rows)]

def detectXY(x,y,mode): #225 710

  if left_region_margin[0]<x<left_region_margin[1]: 
    if top_region_margin[0]<y<top_region_margin[1]: #return("left","top")
      x_reg = (x - x_left) // x_mod
      y_reg = (y - y_top) // y_mod
      
    else: #return("left","bottom")
      x_reg = (x - x_left) // x_mod
      y_reg = ((y - y_bottom) // y_mod) + 7
  else:
    #if 180<y<583: #return("right","top")
    #  x_reg = (x - x_right) // x_mod
    #  y_reg = (y - y_top) // y_mod
    #else: #return("right","bottom")
      x_reg = (x - x_right) // x_mod
      y_reg = ((y - y_bottom) // y_mod) + 37
  #print("y ->" + str(y))
  #print("y_reg ->" + str(y_reg))
  return(int(y_reg),ans_mode(x_reg,mode))
      
def ans_mode(val,mode):
  val_reg = val
  error_char = -1
  if mode == 0:
    return {
      0:  'a',
      1:  'b',
      2:  'c',
      3:  'd',
      4:  'e',
      5:  'f',
      6:  'g',
      7:  'h',
      8:  'i',
      9:  'j',
      10:  'k',
      11:  'l'
    }.get(val_reg, error_char)
  elif mode == 1 :
    return {
      0:  '1',
      1:  '2',
      2:  '3',
      3:  '4',
      4:  '5',
      5:  '6',
      6:  '7',
      7:  '8',
      8:  '9',
      9:  '0',
      10:  'a', #+
      11:  'b'  #-
    }.get(val_reg, error_char)
  elif mode == 2 :
    return {
      0:  1,
      1:  2,
      2:  3,
      3:  4,
      4:  5,
      5:  6,
      6:  7,
      7:  8,
      8:  9,
      9:  0,
      10:  10,
      11:  11

    }.get(val_reg, error_char)
  elif mode == 3:
    return {
      0:  0,
      1:  1,
      2:  2,
      3:  3,
      4:  4,
      5:  5,
      6:  6,
      7:  7,
      8:  8,
      9:  9,
      10:  10,
      11:  11

    }.get(val_reg, error_char)
    
def show_detect_every_block(img):
  img_reg = img

  for i in range(0,student_rows+1):
    cv2.line(img_reg, (x_left, y_top + round( i * y_mod)),    (x_left +  round(student_cols * x_mod), y_top + round( i * y_mod)), (150, 0, 150), 3) #學生水平線
  for i in range(0,L_ans_rows+1):
    cv2.line(img_reg, (x_left, y_bottom + round( i * y_mod)),  (x_left +  round(L_ans_cols * x_mod), y_bottom + round( i * y_mod)), (150, 0, 150), 3) #ANS_LEFT水平線
  for i in range(0,R_ans_rows+1):
    cv2.line(img_reg, (x_right, y_bottom + round( i * y_mod)), (x_right +  round(R_ans_cols * x_mod), y_bottom + round( i * y_mod)), (150, 0, 150), 3) #ANS_RIGHT水平線
  
  for i in range(0,student_cols+1):
    cv2.line(img_reg, (x_left+ round( i * x_mod), y_top), (x_left + round( i * x_mod), y_top +  round(student_rows * y_mod)), (150, 0, 150), 3) #學生垂直線
  for i in range(0,L_ans_cols+1):
    cv2.line(img_reg, (x_left+ round( i * x_mod), y_bottom), (x_left + round( i * x_mod), y_bottom +  round(L_ans_rows * y_mod)), (150, 0, 150), 3) #ANS_LEFT垂直線
  for i in range(0,R_ans_cols+1):
    cv2.line(img_reg, (x_right + round( i * x_mod), y_bottom), (x_right + round( i * x_mod), y_bottom +  round(R_ans_rows * y_mod)), (150, 0, 150), 3)  #ANS_RIGHT垂直線
  return img_reg

def output_cnts_result(cnts_in,paper_in,scan_in):
  ans_num = list()
  student_num = list()
  cnts = cnts_in
  paper = paper_in
  rect_count = 0
  #塗黑大小range X60 Y30 X45 Y20  
  ##學號 XX250 Y185 X1050 Y640 
  #01_25 XX250 Y720 X1182 Y2716
  #26_50 X1340　Y720 X2280 Y27516 
  anser_size = (30,10,70,50)
  student_num_bound = (250,185,1030,625)
  ques_left_bound  = (250,715,1180,2705) # (250,705,1180,2760)
  ques_right_bound = (1330,715,2260,2705) # (1330,705,2260,2760)
  mode = 3
  circle_cnt = 0
  if pdf_mode == 1:
    student_num_bound = ((x_left),(y_top) ,(x_left  + round((student_cols) * x_mod)) ,(y_top  + round((student_rows) * y_mod)))
    ques_left_bound  = ((x_left),(y_bottom),(x_left + round((L_ans_cols) * x_mod))  ,(y_bottom + round((L_ans_rows) * y_mod))) # (250,705,1180,2760)
    ques_right_bound = ((x_right),(y_bottom),(x_right + round((R_ans_cols) * x_mod))  ,(y_bottom + round((R_ans_rows) * y_mod))) # (1330,705,2260,2760)
  
  for c in cnts:
    # 计算轮廓的边界框，然后利用边界框数据计算宽高比
    (x, y, w, h) = cv2.boundingRect(c) 
    #print(x, y, w, h) ################################################debug
    if  anser_size[0]<w<anser_size[2] and anser_size[1]<h<anser_size[3] and student_num_bound[0]<x<student_num_bound[2] and student_num_bound[1]<y<student_num_bound[3]: 

      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"]) #取得X中點
      cY = int(M["m01"] / M["m00"]) #取得Y中點
      #绘制中心及其轮廓
      cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0) #劃出輪廓
      cv2.circle(paper, (cX, cY), 7, (255, 0, 0), -1)
      
      cv2.drawContours(scan_in, c, -1, (0, 0, 255), 5, lineType=0) #劃出輪廓
      cv2.circle(scan_in, (cX, cY), 7, (255, 0, 0), -1)
      
      #print('student_num', "cX -> ", cX, "cY -> ", cY, detectXY(cX, cY, mode))
      student_num.append(detectXY(cX, cY, mode))
    elif  anser_size[0]<w<anser_size[2] and anser_size[1]<h<anser_size[3] and ques_left_bound[0]<x<ques_left_bound[2] and ques_left_bound[1]<y<ques_left_bound[3]: 
      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      #绘制中心及其轮廓
      cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0)
      cv2.circle(paper, (cX, cY), 7, (0, 255, 0), -1)

      cv2.drawContours(scan_in, c, -1, (0, 0, 255), 5, lineType=0) #劃出輪廓
      cv2.circle(scan_in, (cX, cY), 7, (0, 255, 0), -1)

      #print('1_25',"cX -> ", cX, "cY -> ", cY, detectXY(cX, cY, mode))
      ans_num.append(detectXY(cX, cY, mode))
      #ans_num.sort()
      #print("ans_num -> ", ans_num)
    elif  anser_size[0]<w<anser_size[2] and anser_size[1]<h<anser_size[3] and ques_right_bound[0]<x<ques_right_bound[2] and ques_right_bound[1]<y<ques_right_bound[3]: 
      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      #绘制中心及其轮廓
      cv2.drawContours(paper, c, -1, (0, 0, 255), 5, lineType=0)
      cv2.circle(paper, (cX, cY), 7, (0, 0, 255), -1)

      cv2.drawContours(scan_in, c, -1, (0, 0, 255), 5, lineType=0) #劃出輪廓
      cv2.circle(scan_in, (cX, cY), 7, (0, 0, 255), -1)

      #print('25_50', "cX -> ", cX, "cY -> ", cY, detectXY(cX, cY, mode))
      ans_num.append(detectXY(cX, cY, mode))
    else :
      if 0:
        cv2.drawContours(paper, c, -1, (0, 100, 100), 5, lineType=0) #劃出輪廓
        print(" x ",x," y ",y," w ",w," h ",h)
        cv2.putText(paper, str(circle_cnt), (x,y), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 100, 100), 1, cv2.LINE_AA)
        circle_cnt = circle_cnt + 1
  #cv2_imshow(paper) ################################################debug
  student_num.sort()
  ans_num.sort()
  #print(student_num)
  #print(ans_num)
  return(paper,student_num,ans_num)


def output_mod_result_to_excel_col(student_num_in,ans_num_in):
  
  student_num_ans_num_list = student_num_in + ans_num_in
  out_list = list()
  site = 0
  input_reset = "xxxxxxxxxxxx"
  input_list = list(input_reset)
  input_reg = ""
  for i in range(0,67):
    out_list.append(input_reset)
    #print("out_list[i] -> " +str(i) +"  " + out_list[i])
  
  #print("student_num -> ")
  #print(student_num)
  for i in range(len(student_num_ans_num_list)) :  #0 TO 6
    #print("i -> " + str(i))
    if site != student_num_ans_num_list[i][0]:  #next bit
      for j in range(len(input_list)):
        input_reg = input_reg + input_list[j]
      out_list[site] = input_reg
      input_reg = ""
      input_list = list(input_reset)
      site = student_num_ans_num_list[i][0]
      
      #print("out_list -> ")
      #print(out_list)
    #print("i -> " , i,ans_mode(student_num[i][1],0), student_num[i][1])
    input_list[student_num_ans_num_list[i][1]] = ans_mode(student_num_ans_num_list[i][1],1)
  
  for j in range(len(input_list)):
    input_reg = input_reg + input_list[j]
  out_list[site] = input_reg
  #print(out_list)
  return(out_list)


def image_to_cnts_paper(im1,scan_in):
  im1_hsv = cv2.cvtColor(im1,cv2.COLOR_BGR2RGB)
  im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
  blurred = im1_gray
  #cv2_imshow(blurred)
  edged = cv2.Canny(blurred, 10, 100)
  cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  #findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy       CV4
  #findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> image, contours, hierarchy   CV3.4
  cnts = cnts[1] if imutils.is_cv2() else cnts[0]
  docCnt = None

  im1_h = im1.shape[0] 
  im1_w = im1.shape[1]

  #cv2_imshow(im1_gray)
  # 确保至少有一个轮廓被找到
  if len(cnts) > 0:
    #print(cnts)
    # 将轮廓按大小降序排序
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # 对排序后的轮廓循环处理
    for c in cnts:
        if (cv2.contourArea(c)) > round(im1_h*im1_w*0.8): #找到輪廓佔整頁的八成大小以上
          # 获取近似的轮廓
          peri = cv2.arcLength(c, True)
          approx = cv2.approxPolyDP(c, 0.02 * peri, True)
          # 如果近似轮廓有四个顶点，那么就认为找到了答题卡
          if len(approx) == 4 : 
              docCnt = approx
              break
        else:                   #找不到輪廓佔整頁的八成大小以上
          approx = np.array(
                [[[round( 86/1654*im1_w), round( 60/2339*im1_h)]],
                [[round( 79/1654*im1_w), round(2262/2339*im1_h)]],
                [[round(1582/1654*im1_w), round(2266/2339*im1_h)]],
                [[round(1587/1654*im1_w), round( 64/2339*im1_h)]]]
                )
          docCnt = approx

  newim1=im1.copy()

  for i in docCnt:
      #circle函数为在图像上作图，新建了一个图像用来演示四角选取
      cv2.circle(newim1, (i[0][0],i[0][1]), 10, (255, 0, 0), -1)
  #cv2_imshow(newim1)
  paper = perspective.four_point_transform(im1, docCnt.reshape(4, 2))
  warped = perspective.four_point_transform(im1_gray, docCnt.reshape(4, 2))

  width1 = 2400
  height1 = 2800

  # 对灰度图应用二值化算法
  thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
  #重塑可能用到的图像
  thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
  paper = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)
  warped = cv2.resize(warped, (width1, height1), cv2.INTER_LANCZOS4)
  #均值滤波
  ChQImg = cv2.blur(thresh, (23, 23))
  #二进制二值化
  ChQImg = cv2.threshold(ChQImg, 100, 225, cv2.THRESH_BINARY)[1]

  cnts,hierarchy  = cv2.findContours(ChQImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  scan_in = perspective.four_point_transform(scan_in, docCnt.reshape(4, 2))
  scan_in = cv2.resize(scan_in, (width1, height1), cv2.INTER_LANCZOS4)
  return(cnts, paper, scan_in)

def get_pdf_num(file_name):
    images = convert_from_path(file_name, poppler_path = poppler_store_path) 
    for page_num, image in enumerate(images):  #need mode 1  
       print("")
    return page_num

def scan_pdf(file_name):
    student_num = [] 
    ans_num = []
    data_reg = pd.DataFrame()
    data_out = pd.DataFrame()
    images = convert_from_path(file_name, poppler_path = poppler_store_path)
    file_name_path = os.path.dirname(file_name)
    for page_num, image in enumerate(images):  #need mode 1  
        fname = r"image" + str(page_num) + ".png"
        fname1 = r"image" + str(page_num) + ".jpeg"
        image.save(file_name_path + '/split_png/' + fname, "PNG") 
        im1 = cv2.imread(file_name_path + '/split_png/' + fname)
        rotate_degree = rotate_img(file_name_path + '/split_png/' + fname)
        if rotate_degree == 90:
            im1 = cv2.rotate(im1, cv2.ROTATE_90_CLOCKWISE)
        elif rotate_degree == 180:
            im1 = cv2.rotate(im1, cv2.ROTATE_180)
        elif rotate_degree == 270:
            im1 = cv2.rotate(im1, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(file_name_path + '/split_png/' + fname, im1, [cv2.IMWRITE_PNG_COMPRESSION, 2])
        cv2.imwrite(file_name_path + '/split_jpeg/' + fname1, im1, [cv2.IMWRITE_JPEG_QUALITY, 70])
        scan_in = im1
        #cv2.imshow('', im1) 
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im1 = cv2.medianBlur(im1, 5)
        im1 = cv2.adaptiveThreshold(im1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,23,4)  
        im1 = cv2.cvtColor(im1, cv2.COLOR_GRAY2BGR) 
      ############################################################################################################################# rotate to correct direction
        cnts, paper, scan_in = image_to_cnts_paper(im1, scan_in)
      ############################################################################################################################# find rectangle site debug_use
        paper,student_num,ans_num = output_cnts_result(cnts,paper,scan_in)
      ############################################################################################################################# output student_num ans_num use // %
        out_list = output_mod_result_to_excel_col(student_num,ans_num)
      ############################################################################################################################# trans // % to list[str]
        data_reg = pd.DataFrame(out_list,columns =[("page"+str(page_num))])
        if page_num == 0:
          data_out = data_reg
        else:
          data_out = pd.merge(data_out,data_reg,left_index=True,right_index=True)

        data_reg = pd.DataFrame()



        student_num =  list()
        student_num = list()
        ans_num = list()

        scan_in = show_detect_every_block(scan_in)
        cv2.imwrite(file_name_path + '/result/' + r'result_'+ fname1 ,scan_in, [cv2.IMWRITE_JPEG_QUALITY, 70])
    data_out.to_excel(file_name_path + '/result/out.xlsx') 
    #print(data_out)
    

def add_output_folder(file_name_abs):
    file_name_abs_path = os.path.dirname(file_name_abs)
    #print(file_name_abs_path)
    os.makedirs(file_name_abs_path + '/split_png', exist_ok=True)
    os.makedirs(file_name_abs_path + '/split_jpeg', exist_ok=True)
    os.makedirs(file_name_abs_path + '/result', exist_ok=True)