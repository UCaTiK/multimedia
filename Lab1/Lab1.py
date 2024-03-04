from matplotlib.image import imread
from PIL import Image
import numpy as np


def black_and_white(matrix):
	new_matrix = []
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			lst.append([sum(matrix[i][j]) / 3] * 3)
		new_matrix.append(lst)
	return new_matrix


def negative(matrix):
	new_matrix = []
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			lst.append([255 - matrix[i][j][k] for k in range(3)])
		new_matrix.append(lst)
	return new_matrix


def sepia(matrix):
	new_matrix = []
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			R = matrix[i][j][0]
			G = matrix[i][j][1]
			B = matrix[i][j][2]
			sepia_r = min(0.393 * R + 0.769 * G + 0.189 * B, 255)
			sepia_g = min(0.349 * R + 0.686 * G + 0.168 * B, 255)
			sepia_b = min(0.272 * R + 0.534 * G + 0.131 * B, 255)
			lst.append([sepia_r, sepia_g, sepia_b])
		new_matrix.append(lst)
	return new_matrix


def brightness(matrix, k):
	new_matrix = []
	average = 0
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			if k > 0:
				lst.append((min(matrix[i][j][0] + k, 255), min(matrix[i][j][1] + k, 255), min(matrix[i][j][2] + k, 255)))
			else:
				lst.append((max(matrix[i][j][0] + k, 0), max(matrix[i][j][1] + k, 0), max(matrix[i][j][2] + k, 0)))
		new_matrix.append(lst)
	return new_matrix
	

# n - количество соседей в сторону
# a - сила размытия (1 - полное размытие)
def blur(matrix, n=1, a=0.5):
	new_matrix = []
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			count = -1
			summary = [-int(matrix[i][j][k]) for k in range(3)]
			for k in range(max(i - n, 0), min(i + n + 1, len(matrix))):
				for l in range(max(j - n, 0), min(j + n + 1, len(matrix[0]))):
					count += 1
					for p in range(3):
						summary[p] += int(matrix[k][l][p])
			for p in range(3):
				summary[p] = int(summary[p] / count * a)
				summary[p] += int(matrix[i][j][p] * (1 - a))
				summary[p] = min(summary[p], 255)
			
			lst.append(summary)
		new_matrix.append(lst)
	return new_matrix


# Загрузка изображения
image = imread("img.jpg")

# Использование фильтров
# image = negative(image)
image = brightness(image, -50)
# image = sepia(image)
# image = blur(image, 5, 1)

# Выгрузка нового изображения
im = Image.fromarray(np.uint8(image))
im.save("result.jpg")
