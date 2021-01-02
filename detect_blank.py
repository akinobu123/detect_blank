import cv2
import time
import numpy as np

# 白紙画像であるかを検出(白紙ならTrueを返す)
# 引数：cv2形式のフルカラー画像
def detect_blank_page1(image):
	# Grayscale変換 => 二値化(INV...黒=255、白=0)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	bin_image = cv2.threshold(gray_image, 170, 255, cv2.THRESH_BINARY_INV)[1]
	#cv2.imwrite('bin_image.tif', bin_image)							# debug

	# 画像中オブジェクトの輪郭を抽出(contoursにオブジェクトのリスト、各々が外周点の座標リストになっている)
	contours, hierarchy = cv2.findContours(bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#cont_image = cv2.drawContours(image, contours, -1, (0,255,0), 1)	# debug
	#cv2.imwrite('cont_image.png', cont_image)							# debug

	is_blank = True
	for i in range(0, len(contours)):			# 各オブジェクトでループ
		x,y,w,h = cv2.boundingRect(contours[i])	# オブジェクトの外接矩形の座標を取得
		#print(w, h)
		if w > 10 or h > 10:					# オブジェクトの縦横幅でチェック
			is_blank = False
			break

	return is_blank


def detect_blank_page2(image):
	# Grayscale変換 => 二値化
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	bin_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)[1]
	#cv2.imwrite('bin_image.tif', bin_image)							# debug

	#print(np.sum(bin_image, axis=0)//255)
	#print(np.sum(bin_image, axis=1)//255)
	sum_x_max = np.max(np.sum(bin_image, axis=0))
	sum_y_max = np.max(np.sum(bin_image, axis=1))
	#print(sum_x_max//255, sum_y_max//255)

	#v = np.array([1, 1, 1, 1, 1])
	#sum_conv_x = np.convolve(np.sum(bin_image, axis=0)//255,v, mode='valid')
	#sum_conv_y = np.convolve(np.sum(bin_image, axis=1)//255,v, mode='valid')
	#print(sum_conv_x)

	if sum_x_max > (10*255) or sum_y_max > (10*255):	# 縦横いずれか10pix以上なら...
		return False									# 白紙ではないとする
	else:
		return True


def main():
	# 画像の読み込み
	img = cv2.imread("../image/blank2.png")

	start_time = time.time() * 1000

	# 白紙の検知
	is_blank = detect_blank_page1(img)

	end_time = time.time() * 1000
	elapse_time = end_time - start_time
	print("execute time : {} ms".format(elapse_time))

	if is_blank:
		print("it's blank page!")
	else:
		print("it's not blank page!")

main()
