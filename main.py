import os
import subprocess
import yt_dlp

def buat_klip_otomatis(url_video: str, mulai_detik: int = 15, durasi: int = 45, output_file: str = "klip_viral_9x16.mp4"):
    temp_video = "source_temp.mp4"

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': temp_video,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    if os.path.exists("cookies.txt") and os.path.getsize("cookies.txt") > 10:
        print("Menggunakan cookies.txt...")
        ydl_opts['cookiefile'] = "cookies.txt"
    else:
        print("PERINGATAN: cookies.txt tidak ditemukan atau kosong!")

    print(f"Mengunduh video dari: {url_video}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_video])

    print("Memotong dan mengubah rasio ke 9:16...")
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(mulai_detik),
        "-i", temp_video,
        "-t", str(durasi),
        "-vf", "crop=ih*(9/16):ih,scale=1080:1920",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        output_file
    ]
    subprocess.run(cmd, check=True)
    print(f"Selesai! Output tersimpan di: {output_file}")

if __name__ == "__main__":
    url = os.environ.get("VIDEO_URL")
    mulai = int(os.environ.get("MULAI_DETIK", "15"))
    durasi = int(os.environ.get("DURASI", "45"))
    
    if not url:
        raise ValueError("VIDEO_URL wajib diisi!")
        
    buat_klip_otomatis(url_video=url, mulai_detik=mulai, durasi=durasi)
