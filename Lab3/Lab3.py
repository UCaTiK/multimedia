import numpy as np
from pydub import AudioSegment
from scipy.interpolate import interp1d


def load_audio(file_path):
	audio = AudioSegment.from_mp3(file_path)
	samples = np.array(audio.get_array_of_samples())
	return audio.frame_rate, samples, audio.sample_width, audio.channels


def save_audio(samples, frame_rate, sample_width, channels, file_path):
	new_audio = AudioSegment(
		samples.tobytes(),
		frame_rate=frame_rate,
		sample_width=sample_width,
		channels=channels
	)
	new_audio.export(file_path, format="mp3")


def speed_up(samples, factor):
	speeded_samples = []

	index = 0.0
	while index < len(samples):
		speeded_samples.append(samples[int(index)])
		index += factor

	return np.array(speeded_samples, dtype=samples.dtype)


def restore_audio(speeded_up_samples, original_length):
	indices = np.linspace(0, len(speeded_up_samples) - 1, original_length)
	interpolator = interp1d(np.arange(len(speeded_up_samples)), speeded_up_samples, kind='linear')
	return interpolator(indices).astype(speeded_up_samples.dtype)


def main(filename, speed_factor):
	input_file = f'{filename}.mp3'
	speeded_file = f'{filename}_speeded_{speed_factor}.mp3'
	file_restored_1 = f'{filename}_restored_1.mp3'
	file_restored_2 = f'{filename}_restored_2.mp3'
	
	# Подгрузка аудиофайла
	frame_rate, samples, sample_width, channels = load_audio(input_file)
	
	# Ускорение аудиофайла
	speeded_samples = speed_up(samples, speed_factor)
	save_audio(speeded_samples, frame_rate, sample_width, channels, speeded_file)
	
	# Возвращение исходного файла с помощью замедления
	speeded_samples = speed_up(speeded_samples, 1 / speed_factor)
	save_audio(speeded_samples, frame_rate, sample_width, channels, file_restored_1)
	
	# Возвращение исходного файла с помощью интерполяции
	restored_samples = restore_audio(speeded_samples, len(samples))
	save_audio(restored_samples, frame_rate, sample_width, channels, file_restored_2)


if __name__ == "__main__":
	main("music", 2)
	main("music", 3)
	main("music", 1.5)
