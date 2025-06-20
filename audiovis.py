import librosa
import numpy as np
import math

def analyze_audio_for_eq(file_path, interval_ms=500, num_bands=8, num_levels=9, contrast_exponent=1.0, band_type='log'):
    try:
        y, sr = librosa.load(file_path, sr=None)
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

    n_fft = 1024
    hop_length = int(librosa.time_to_samples(interval_ms / 1000.0, sr=sr))

    stft_result = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    spectrogram = np.abs(stft_result)

    fft_freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    if band_type == 'linear':
        max_freq = np.max(fft_freqs)
        band_edges_hz = np.linspace(0, max_freq, num_bands + 1)
    else:  
        mel_bands = librosa.hz_to_mel(fft_freqs)
        mel_band_edges = np.linspace(np.min(mel_bands), np.max(mel_bands), num_bands + 1)
        band_edges_hz = librosa.mel_to_hz(mel_band_edges)

    band_magnitudes = np.zeros((num_bands, spectrogram.shape[1]))
    for i in range(num_bands):
        lower_hz = band_edges_hz[i]
        upper_hz = band_edges_hz[i+1]
        
        band_indices = np.where((fft_freqs >= lower_hz) & (fft_freqs < upper_hz))[0]

        if len(band_indices) > 0:
            band_magnitudes[i, :] = np.max(spectrogram[band_indices, :], axis=0)

    db_bands = librosa.power_to_db(band_magnitudes**2, ref=np.max(band_magnitudes, axis=1, keepdims=True), top_db=80)

    db_min = -80.0
    db_max = 0.0
    normalized_bands = (db_bands - db_min) / (db_max - db_min)
    normalized_bands = np.power(normalized_bands, contrast_exponent) # Pass the new variable here

    level_bands = (normalized_bands * (num_levels - 1))
    level_bands = np.round(level_bands, decimals=1)

    level_bands = np.clip(level_bands, 0.0, num_levels - 1)


    timestamps = librosa.frames_to_time(np.arange(level_bands.shape[1]), sr=sr, hop_length=hop_length)
    output_data = []
    for t_idx, ts in enumerate(timestamps):
        output_data.append({
            "timestamp_ms": int(ts * 1000),
            "bands": level_bands[:, t_idx].tolist() 
        })
        
    return output_data

if __name__ == "__main__":
    AUDIO_FILE = "./audio.mp3"
    ANALYSIS_INTERVAL_MS = 33# 77.319587
    NUM_EQUALIZER_BANDS = 11
    VISUALIZER_LEVELS = 16
    BASE_Y=300 #400
    SCALE_FACTOR = 1.1
    CONTRAST_EXPONENT = 3.0
    BAND_TYPE = 'linear'
    WIDTH = 2
    transition = False

    # --- RUN ANALYSIS ---
    eq_data = analyze_audio_for_eq(
        file_path=AUDIO_FILE,
        interval_ms=ANALYSIS_INTERVAL_MS,
        num_bands=NUM_EQUALIZER_BANDS,
        num_levels=VISUALIZER_LEVELS,
        contrast_exponent=CONTRAST_EXPONENT,
        band_type=BAND_TYPE
    )

    if eq_data:
        print(f"Successfully analyzed '{AUDIO_FILE}'")
        print("\n--- Sample Data ---")
        for i in range(min(5, len(eq_data))):
            print(eq_data[i])

    f = open("eq_data.txt", "w")
    fulldata = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
    for i in eq_data:
        for j in range(len(i["bands"])):
            if i["timestamp_ms"]+13 < 49497:
                continue
            fulldata[j].append([i["timestamp_ms"], i["bands"][j]])
    for i in range(len(fulldata)):
        transition = False
        WIDTH=2
        SCALE_FACTOR=1.1
        f.write(f'''// Band {i}\nSprite,Foreground,Centre,"sb\\band.png",{8+50*(i+1)},{BASE_Y}\n F,49497,{fulldata[0][0][0]},0,0.5\n''')
        if i < 2:
            SCALE_FACTOR = 0.5
        for j in range(len(fulldata[i])-1):
            if fulldata[i][j][0] >= 274652 and not transition:
                transition = True
                WIDTH=2.5
                f.write(f''' M,10,{fulldata[i][j][0]},{fulldata[i][j][0]+500},{8+50*(i+1)},{BASE_Y},{(i*85.4)-107},480\n F,10,{fulldata[i][j][0]},{fulldata[i][j][0]+1000},0.5,1\n''')
            if fulldata[i][j][0] <= 314239:
                f.write(f''' V,0,{fulldata[i][j][0]},{fulldata[i][j][0]+math.ceil(ANALYSIS_INTERVAL_MS)},{WIDTH},{fulldata[i][j][1]*SCALE_FACTOR},{WIDTH},{fulldata[i][j+1][1]*SCALE_FACTOR}\n''')
            #if transition: f.write(f'''MY,0,{fulldata[i][j][0]},{fulldata[i][j][0]+math.ceil(ANALYSIS_INTERVAL_MS)},{BASE_Y+(6*fulldata[i][j][1]*SCALE_FACTOR)},{BASE_Y+(6*fulldata[i][j+1][1]*SCALE_FACTOR)}\n''')