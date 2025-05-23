import os
import argparse
import tempfile
import time
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pydub import AudioSegment
from TTS.api import TTS

# Load Coqui TTS model (choose other models later)
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=True)

print(tts.speakers)


def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []

    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')

            for tag in soup(['script', 'style', 'sup']):
                tag.decompose()

            text = soup.get_text(separator=' ', strip=True)
            cleaned = ' '.join(text.split())

            if cleaned and len(cleaned) > 100:
                chapters.append(cleaned)
                print(f"✅ Found chapter with {len(cleaned)} characters.")
            else:
                print("⚠️ Skipping short or empty chapter.")

    print(f"\n🔍 Extracted {len(chapters)} usable chapters.")
    return chapters

def split_text(text, max_length=400):
    chunks = []
    while len(text) > max_length:
        split_at = text.rfind('.', 0, max_length)
        if split_at == -1:
            split_at = max_length
        chunks.append(text[:split_at+1].strip())
        text = text[split_at+1:].strip()
    if text:
        chunks.append(text)
    return chunks

def generate_speech(text, final_wav_path):
    chunks = split_text(text)
    print(f"    🧩 Chapter has {len(chunks)} chunks...")

    combined = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            chunk_wav = tmpfile.name

            tts.tts_to_file(text=chunk, file_path=chunk_wav, speaker="p225")


        if os.path.exists(chunk_wav):
            segment = AudioSegment.from_wav(chunk_wav)
            combined += segment
            os.remove(chunk_wav)
        else:
            print(f"    ⚠️ Skipped missing chunk {i+1}")

    combined.export(final_wav_path, format="wav")

def convert_wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")
    os.remove(wav_path)

def process_epub(epub_path, output_dir):
    book_name = os.path.splitext(os.path.basename(epub_path))[0]
    book_output_path = os.path.join(output_dir, book_name)
    os.makedirs(book_output_path, exist_ok=True)

    print(f"\n📖 Processing: {book_name}")
    chapters = extract_text_from_epub(epub_path)

    if not chapters:
        print("  ⚠️ No readable chapters found.")
        return

    for i, chapter in enumerate(chapters):
        base_filename = f"chapter_{i+1:03}"
        wav_path = os.path.join(book_output_path, base_filename + ".wav")
        mp3_path = os.path.join(book_output_path, base_filename + ".mp3")

        print(f"  🎙️ Generating Chapter {i+1}...")
        try:
            generate_speech(chapter, wav_path)
            convert_wav_to_mp3(wav_path, mp3_path)
        except Exception as e:
            print(f"    ❌ Error converting Chapter {i+1}: {e}")

    print(f"✅ Done: Audiobook saved to {book_output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert EPUBs into audiobooks (MP3).")
    parser.add_argument("input_dir", help="Directory containing .epub files")
    parser.add_argument("output_dir", help="Directory to save audiobook MP3s")
    args = parser.parse_args()

    epub_files = [f for f in os.listdir(args.input_dir) if f.lower().endswith(".epub")]
    if not epub_files:
        print("⚠️ No EPUB files found in input directory.")
        return

    for epub_file in epub_files:
        epub_path = os.path.join(args.input_dir, epub_file)
        process_epub(epub_path, args.output_dir)

if __name__ == "__main__":
    main()
