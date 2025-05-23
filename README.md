* ✅ Project name: **ePub-to-Audio**
* ✅ CUDA note: `gpu=False` if not using GPU
* ✅ Author and org: Daniel Lindenberger, **Thaumazo**
* ✅ Acknowledgment of **GPT-4o** for code assistance

---

````markdown
# 🎧 ePub-to-Audio

Convert `.epub` ebooks into high-quality, humanlike audiobooks — entirely offline — using [Coqui TTS](https://github.com/coqui-ai/TTS).  
This tool turns your ebook library into listenable stories with multi-speaker support, natural pacing, and export to MP3.

Created by **Daniel Lindenberger** for the nonprofit **[Thaumazo](https://thaumazo.org)**, with coding support from **GPT-4o**.

---

## ✨ Features

- 📚 Converts `.epub` files into chapter-by-chapter **MP3 audiobooks**
- 🗣️ Uses **Coqui TTS** (`vctk/vits`) for **expressive, local text-to-speech**
- 👥 Supports **multi-speaker narration** (choose different voices per chapter)
- 🧠 Automatically splits long text into natural, synthesis-friendly chunks
- 🎧 Outputs high-quality `.mp3` using `pydub` and `ffmpeg`
- 🚫 Runs **fully offline** — ideal for privacy and accessibility

---

## ⚙️ Installation

### 1. Requirements

- **Python 3.8 – 3.10** (not 3.12+)
- [FFmpeg](https://ffmpeg.org/download.html)
- [espeak or espeak-ng](https://espeak.sourceforge.net/download.html) — used by Coqui for phoneme tokenization

> 🪟 On Windows:  
> Extract `espeak-1.48.15-win64.zip` and add its path (e.g. `C:\Program Files\espeak`) to your **System Environment Variables → Path**

### 2. Install Python packages

```bash
# Create a virtual environment (recommended)
python -m venv epub_env
epub_env\Scripts\activate  # or source epub_env/bin/activate on macOS/Linux

# Install packages
pip install TTS ebooklib beautifulsoup4 pydub
````

If you have a CUDA-enabled NVIDIA GPU, install GPU-accelerated PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> ❗ **Don’t have a GPU?** Just pass `gpu=False` in your script and Coqui will run on CPU.

---

## 🚀 Usage

```bash
python epub_to_audiobook.py ./epubs ./audiobooks
```

* `./epubs` — folder containing `.epub` files
* `./audiobooks` — output folder for generated `.mp3` files

Each book will get its own folder:

```
audiobooks/
└── Book_Title/
    ├── chapter_001.mp3
    ├── chapter_002.mp3
    └── ...
```

---

## 🎙️ Voice Options

This project uses the **`vctk/vits`** multi-speaker model.

### Set a default speaker:

In your script:

```python
tts.tts_to_file(text=chunk, file_path=chunk_wav, speaker="p225")
```

List all available speakers:

```python
print(tts.speakers)
```

Want to vary speakers by chapter? Use:

```python
speaker = tts.speakers[i % len(tts.speakers)]
```

---

## 🛠️ Roadmap

* [ ] Combine chapters into single audiobook per title
* [ ] GUI frontend with speaker/voice settings
* [ ] Voice cloning from sample `.wav`
* [ ] Optional emotion/prosody control
* [ ] EPUB metadata extraction for tagging

---

## 🤖 AI Acknowledgment

This project was developed with the assistance of **GPT-4o** from OpenAI.

---

## 🤝 Contributing

Pull requests and suggestions welcome. If you find a bug or want to request a feature, feel free to open an issue.

---

## 📜 License

This project is released under the [GPLv3 License](LICENSE).

---

## 🙏 Credits

* [Coqui TTS](https://github.com/coqui-ai/TTS)
* [ebooklib](https://github.com/aerkalov/ebooklib)
* [pydub](https://github.com/jiaaro/pydub)
* [espeak](https://espeak.sourceforge.net/)
