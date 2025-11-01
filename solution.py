import sys
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize

def apply_emotion(sound: AudioSegment, emotion: str) -> AudioSegment:
    emotion = emotion.lower()

    # === Default parameter ===
    tempo_scale = 1.0
    base_gain = 0.0
    brightness = 0.0
    fade = (200, 200)

    # === Parameter per emosi ===
    if emotion == "tenang":
        tempo_scale = 0.97
        base_gain = -1.0
        brightness = -0.5    
        fade = (300, 300)
    elif emotion == "semangat":
        tempo_scale = 1.05
        base_gain = 2.0
        brightness = 1.0    
        fade = (150, 150)
    elif emotion == "sedih":
        tempo_scale = 0.94
        base_gain = -2.0
        brightness = -1.0   
        fade = (400, 400)

    # === 1. Tempo adjustment (tanpa ubah pitch) ===
    sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * tempo_scale)
    }).set_frame_rate(sound.frame_rate)

    # === 2. Volume dasar ===
    sound = sound + base_gain

    # === 3. Mikro dinamika (simulasi penekanan kalimat) ===
    chunk_ms = 500
    chunks = [sound[i:i + chunk_ms] for i in range(0, len(sound), chunk_ms)]
    for i, c in enumerate(chunks):
        if emotion == "semangat" and i % 4 == 0:
            chunks[i] = c + 1.0
        elif emotion == "tenang" and i % 5 == 0:
            chunks[i] = c - 0.3
        elif emotion == "sedih" and i % 6 == 0:
            chunks[i] = c - 0.5
    sound = sum(chunks)

    # === 4. EQ Brightness Simulation ===
    if brightness > 0:
        bright_part = sound.high_pass_filter(2500).apply_gain(brightness)
        sound = sound.overlay(bright_part - 3)  # campur agar halus
    elif brightness < 0:
        dark_part = sound.low_pass_filter(3000).apply_gain(brightness / 2)
        sound = sound.overlay(dark_part - 2)

    # === 5. Fade dan normalisasi ===
    sound = sound.fade_in(fade[0]).fade_out(fade[1])
    sound = normalize(sound)

    return sound

def main():
    if len(sys.argv) < 3:
        print("Usage: python solution.py 'teks' output.wav [emosi]")
        print("Emosi: netral | tenang | semangat | sedih")
        return

    text, output = sys.argv[1], sys.argv[2]
    emotion = sys.argv[3] if len(sys.argv) > 3 else "netral"

    if not text.strip():
        print("❌ Error: teks kosong.")
        return

    print(f"🎙️ Membuat narasi '{emotion}' dengan karakter konsisten...")

    # Langkah 1: generate suara dasar
    tts = gTTS(text=text, lang="id")
    temp_mp3 = "temp.mp3"
    tts.save(temp_mp3)

    # Langkah 2: terapkan ekspresi emosional tanpa ubah timbre
    sound = AudioSegment.from_mp3(temp_mp3)
    sound = apply_emotion(sound, emotion)

    # Langkah 3: ekspor hasil
    sound.export(output, format="wav")
    print(f"✅ Tersimpan: {output} (emosi: {emotion})")

if __name__ == "__main__":
    main()
