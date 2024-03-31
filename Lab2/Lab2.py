import cv2
import numpy as np


def negative(matrix):
	new_matrix = []
	for i in range(len(matrix)):
		lst = []
		for j in range(len(matrix[i])):
			lst.append([255 - matrix[i][j][k] for k in range(3)])
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


def video_modify(video):
	cap = cv2.VideoCapture(video)
	frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = cap.get(cv2.CAP_PROP_FPS)
	
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.mp4', fourcc, fps, (frameWidth,frameHeight))
	
	buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
	new_buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
	
	fc = 0
	ret = True
	
	while (fc < frameCount  and ret):
		ret, buf[fc] = cap.read()
		fc += 1
	
	blur_counter = 0
	third_part = len(new_buf) / 3
	for i in range(len(buf)):
		print(f"Frame {i + 1}/{len(new_buf)}")
		if i < third_part:
			new_buf[i] = brightness(buf[i], 255 - (i * 5))
		elif i < third_part * 2:
			new_buf[i] = negative(buf[i])
		else:
			new_buf[i] = blur(buf[i], 3, blur_counter / third_part)
			blur_counter += 1
	
	for frame in new_buf:
		out.write(frame)
	
	cap.release()
	out.release()
	
	cv2.destroyAllWindows()


def transition(video1, video2):
	cap1 = cv2.VideoCapture(video1)
	cap2 = cv2.VideoCapture(video2)
	frameCount1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
	frameCount2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
	frameWidth = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
	frameHeight = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = cap1.get(cv2.CAP_PROP_FPS)
	
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('transition_output.mp4', fourcc, fps, (frameWidth, frameHeight))
	
	buf1 = np.empty((frameCount1, frameHeight, frameWidth, 3), np.dtype('uint8'))
	buf2 = np.empty((frameCount2, frameHeight, frameWidth, 3), np.dtype('uint8'))
	
	fc1 = 0
	ret1 = True
	while (fc1 < frameCount1 and ret1):
		ret1, buf1[fc1] = cap1.read()
		fc1 += 1

	fc2 = 0
	ret2 = True
	while (fc2 < frameCount2 and ret2):
		ret2, buf2[fc2] = cap2.read()
		fc2 += 1

	transition_frames = min(frameCount1, frameCount2)
	for i in range(transition_frames):
		print(f"Frame {i + 1}/{transition_frames}")
		transition_frame = np.zeros((frameHeight, frameWidth, 3), np.uint8)
		transition_frame[:, :int(frameWidth * (i / transition_frames))] = buf1[i][:, :int(frameWidth * (i / transition_frames))]
		transition_frame[:, int(frameWidth * (i / transition_frames)):] = buf2[i][:, int(frameWidth * (i / transition_frames)):]

		out.write(transition_frame)

	cap1.release()
	cap2.release()
	out.release()

	cv2.destroyAllWindows()


#video_modify("video(10sec).mp4")
transition("video(10sec).mp4", "video2.mp4")
