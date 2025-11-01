# 🎙️ Emotional Speech Generation (Formant-Safe TTS for Indonesian Narration)

## 🧠 Part A — System Design

### 🎯 Goal

Membangun sistem TTS yang mampu menghasilkan **narasi Bahasa Indonesia dengan ekspresi emosional alami**, mirip suara satu pembicara dengan berbagai perasaan (tenang, semangat, sedih, dll).  
Tujuan utamanya: _sekali input teks → hasil suara ekspresif, natural, dan konsisten._

---

### 🧩 1. Pipeline Overview

```
Teks input
   │
   ▼
[1] Text Preprocessing
   │  → normalisasi angka, tanda baca, dan SSML
   ▼
[2] Linguistic Feature Extraction
   │  → fonem, jeda, dan penekanan kata
   ▼
[3] Emotion & Prosody Planner
   │  → menentukan tempo, energi, durasi, intonasi
   ▼
[4] Acoustic Model / TTS Generator
   │  → menghasilkan suara dasar (neutral)
   ▼
[5] Emotion Prosody Modifier (Formant-Safe)
   │  → menyuntikkan emosi tanpa ubah karakter suara
   ▼
Output Audio Emosional
```

---

### 🧠 2. Models & Approach

- **Core TTS Model:**  
  Untuk versi ringan, gunakan `gTTS` (bahasa Indonesia, mudah dijalankan).  
  Untuk versi lanjutan: **FastSpeech 2** atau **VITS** (dengan fine-tuning data narasi Indonesia).
- **Prosody Control:**  
  Menggunakan modul tambahan _Emotion Prosody Modifier_ berbasis DSP untuk menjaga **formant** (timbre) tetap stabil.

---

### 🎭 3. Emotion Control Mechanism (Formant-Safe Prosody)

Alih-alih mengubah pitch formant (yang membuat suara terasa berbeda), sistem ini memodifikasi parameter prosodi mikro:

| Komponen               | Fungsi                      | Efek Emosi                     |
| ---------------------- | --------------------------- | ------------------------------ |
| **Tempo mikro**        | ±5 % perubahan kecepatan    | Memberi kesan energik / lamban |
| **Amplitude Envelope** | Variasi volume antar segmen | Suara lebih hidup              |
| **Dynamic Contrast**   | Beda volume antar kalimat   | Ekspresif tapi natural         |
| **EQ Brightness**      | ±1 dB pada treble           | Kesan cerah vs suram           |

---

### 🎚️ 4. Emotion Profiles (Indonesia Voice)

| Emosi        | Tempo | Volume Dinamis        | EQ Brightness  | Karakteristik  |
| ------------ | ----- | --------------------- | -------------- | -------------- |
| **Netral**   | ×1.00 | 0 dB                  | 0 dB           | Natural, datar |
| **Tenang**   | ×0.97 | −1 dB fade halus      | −0.5 dB treble | Lembut, stabil |
| **Semangat** | ×1.05 | +2 dB variasi mikro   | +1 dB treble   | Cerah, energik |
| **Sedih**    | ×0.94 | −2 dB sustain panjang | −1 dB treble   | Berat, empatik |

---

### 📚 5. Data Requirements

- **Dasar:** Dataset bahasa Indonesia (LibriTTS-ID, Mozilla Common Voice ID).
- **Emosi:** Corpus emosional seperti IEMOCAP + fine-tuning ID samples.
- **Tambahan:** Audiobook atau dokumenter berbahasa Indonesia (bentuk narasi natural).

---

### 🧪 6. Evaluation Metrics

| Aspek                 | Metode                                           |
| --------------------- | ------------------------------------------------ |
| **Kualitas Suara**    | MOS (_Mean Opinion Score_) ≥ 4.0                 |
| **Emotional Clarity** | Uji subjektif (> 80 % responden mengenali emosi) |
| **Intelligibility**   | WER (_Word Error Rate_) < 5 %                    |
| **Consistency**       | Formant Deviation < 3 % antara emosi             |

---

### 🚀 7. Deployment Concept

- **Backend API Python (FastAPI / Flask):**
  - Endpoint `/speak?text=...&emotion=...` → menghasilkan `.wav`
- **Frontend (Simple UI / Streamlit):**
  - Input teks, pilih emosi → putar hasil langsung
- **Containerization:** Docker + Lightweight CPU runtime
  - gTTS + Pydub ⇒ < 150 MB image

---

### ⚠️ 8. Challenges & Mitigation

| Tantangan                                    | Mitigasi                                           |
| -------------------------------------------- | -------------------------------------------------- |
| **Kurangnya dataset emosi Bahasa Indonesia** | Fine-tuning multi-bahasa + crowdsourcing data      |
| **Pitch shift mengubah identitas suara**     | Gunakan formant-safe prosody algoritma             |
| **Ekspresi terlalu artifisial**              | Tambahkan variasi mikro (volume dan tempo)         |
| **Latency tinggi neural TTS**                | Pre-generate voice base + real-time emotion filter |

---

### 🏁 9. Kesimpulan

Desain ini menekankan keseimbangan antara **realitas ekspresi** dan **konsistensi identitas suara**.  
Dengan pipeline modular dan algoritma _Formant-Safe Emotion Prosody_, sistem mampu menghasilkan narasi yang:

- terdengar alami,
- mencerminkan berbagai emosi (tenang, semangat, sedih), dan
- tetap terasa seperti **satu orang yang berbicara**.

# 🎙️ AI Dev Challenge — Emotional Speech Generation (Part B)

## 🧩 Deskripsi

Skrip ini menghasilkan narasi **berbahasa Indonesia dengan ekspresi emosi alami**, tanpa mengubah identitas suara asli.  
Didukung emosi: `netral`, `tenang`, `semangat`, `sedih`.

## 🚀 Cara Menjalankan

```bash
pip install -r requirements.txt
python app.py "Teks narasi Anda di sini" output/id/output.wav [emosi]
```

Contoh:

```bash
python app.py "Selamat datang di dunia AI yang menakjubkan" output/id/semangat.wav semangat
```

## 🎛️ Opsi Emosi

| Emosi      | Ciri Suara               |
| ---------- | ------------------------ |
| `netral`   | Datar, natural           |
| `tenang`   | Lambat dan lembut        |
| `semangat` | Cepat dan bertenaga      |
| `sedih`    | Pelan, lembut, dan dalam |

## ⚙️ Teknologi

- **gTTS** untuk text-to-speech (bahasa Indonesia)
- **pydub** untuk efek audio (tempo, gain, EQ)

## 📦 Output

File `.wav` berisi hasil narasi dengan gaya emosi sesuai pilihan.

---

🧠 _Didesain agar suara tetap terdengar seperti satu orang dengan berbagai ekspresi emosi._
