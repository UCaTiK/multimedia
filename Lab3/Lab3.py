import wave
import numpy as np

def read_wave_file(filename):
	with wave.open(filename, 'rb') as wf:
		params = wf.getparams()
		frames = wf.readframes(params.nframes)
		audio_data = np.frombuffer(frames, dtype=np.int16)
		return params, audio_data

def write_wave_file(filename, params, audio_data):
	with wave.open(filename, 'wb') as wf:
		wf.setparams(params)
		wf.writeframes(audio_data.tobytes())

def stft(x, fft_size=1024, hop_size=512):
	# Окно Ханнинга
	window = np.hanning(fft_size)
	return np.array([np.fft.rfft(window * x[i:i+fft_size]) for i in range(0, len(x)-fft_size, hop_size)])

def istft(X, fft_size=1024, hop_size=512):
	window = np.hanning(fft_size)
	x = np.zeros(hop_size * (X.shape[0] + 1))
	for n, i in enumerate(range(0, len(x)-fft_size, hop_size)):
		x[i:i+fft_size] += np.fft.irfft(X[n]).real * window
	return x

def phase_vocoder(X, rate):
	num_bins = X.shape[1]
	num_frames = X.shape[0]
	time_steps = np.arange(0, num_frames, rate)
	X_phases = np.angle(X)
	X_magnitudes = np.abs(X)
	
	Y = np.zeros((len(time_steps), num_bins), dtype=np.complex_)
	phase_accumulator = np.zeros(num_bins)
	previous_phase = X_phases[0]
	
	for i, step in enumerate(time_steps):
		current_frame = int(step) % num_frames
		current_phase = X_phases[current_frame]
		phase_difference = current_phase - previous_phase
		phase_difference -= np.round(phase_difference / (2 * np.pi)) * (2 * np.pi)
		phase_accumulator += phase_difference
		Y[i] = X_magnitudes[current_frame] * np.exp(1j * phase_accumulator)
		previous_phase = current_phase
	
	return Y

def change_pitch(input_file, output_file, semitone_shift):
	params, audio_data = read_wave_file(input_file)
	
	# Преобразование Фурье
	X = stft(audio_data)
	
	# Меняем pitch
	pitch_shift_rate = 2 ** (semitone_shift / 12)
	Y = phase_vocoder(X, 1 / pitch_shift_rate)
	
	# Обратное преобразование Фурье
	y = istft(Y)
	
	# Интерпляция для изменения длины аудио до изначальной
	y = np.interp(np.linspace(0, len(y), len(audio_data)), np.arange(len(y)), y)
	
	y = np.int16(y / np.max(np.abs(y)) * 32767)
	
	write_wave_file(output_file, params, y)

input_file = 'sample.wav'
semitone_shift = 5  # полутона
output_file = f'output_pitch_shifted_{semitone_shift}.wav'

change_pitch(input_file, output_file, semitone_shift)
