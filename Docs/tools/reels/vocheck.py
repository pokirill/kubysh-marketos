"""Проверка озвучки без ушей (mlx-whisper, локально на Mac): текст реплики и время каждого слова.
python3 vocheck.py файл.wav [ожидаемый текст] — печатает распознанное, слова с таймингами и совпадение с ожидаемым.
Нужен для: голос = подпись дословно; нарезка общего дубля по словам, а не по паузам; ударения и цифры словами."""
import sys, difflib, re
import numpy as np
import audio
import mlx_whisper

MODEL = "mlx-community/whisper-small-mlx"


def words(path):
    s = np.array(audio.load(path), dtype=np.float32)
    s16 = np.interp(np.arange(0, len(s), audio.SR / 16000), np.arange(len(s)), s).astype(np.float32)
    r = mlx_whisper.transcribe(s16, path_or_hf_repo=MODEL, language="ru", word_timestamps=True)
    return r["text"].strip(), [(w["word"].strip(), round(w["start"], 2), round(w["end"], 2)) for sg in r["segments"] for w in sg["words"]]


if __name__ == "__main__":
    text, ws = words(sys.argv[1])
    print(text)
    print(" ".join(f"{w}[{a}-{b}]" for w, a, b in ws))
    if len(sys.argv) > 2:
        norm = lambda x: re.sub(r"[^а-яa-z0-9 ]", "", x.lower().replace("ё", "е"))
        print("совпадение:", round(difflib.SequenceMatcher(None, norm(text), norm(sys.argv[2])).ratio(), 2))
