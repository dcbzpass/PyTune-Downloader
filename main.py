import subprocess
import sys
import os
from pathlib import Path
from yt_dlp import YoutubeDL

ASCII_ART = r"""
  _____       _______                  
 |  __ \     |__   __|                 
 | |__) |_   _  | |_   _ _ __   ___    
 |  ___/| | | | | | | | | '_ \ / _ \   
 | |    | |_| | | | |_| | | | |  __/   
 |_|     \__, | |_|\__,_|_| |_|\___|   
          __/ |                        
         |___/                         
   YouTube to MP3 Converter
"""

def clear_console():
    """Clears the command prompt window."""
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def is_ffmpeg_available():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def progress_hook(d):
    if d['status'] == 'downloading':
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            downloaded = d['downloaded_bytes']
            total = d['total_bytes']
            if total > 0:
                percent = downloaded / total * 100
                sys.stdout.write(f"\rDownloading: {percent:.1f}%")
                sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write("\nDownload finished. Converting to MP3 if needed...\n")
    elif d['status'] == 'error':
        sys.stdout.write("\nAn error occurred during download.\n")

def download_audio_to_mp3(url: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': str(out_dir / "%(title)s.%(ext)s"),
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ffmpeg_location': None, 
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            
            mp3_path = None
            
            candidate = out_dir / f"{title}.mp3"
            if candidate.exists():
                mp3_path = candidate
            
            if mp3_path is None:
                for p in out_dir.glob(f"*.mp3"):
                    if title[:10] in p.name: 
                        mp3_path = p
                        break
            
            return mp3_path
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return None

def prompt_save_location(default_name: str) -> Path:
    print("\nWhere would you like to save the MP3 file?")
    user_input = input(f"Enter full path to the folder (or press Enter to use Documents): ").strip()
    
    if user_input == "":
        save_dir = Path.home() / "Documents"
    else:
        save_dir = Path(user_input)
    
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return Path.home() / "Documents"
        
    return save_dir

def main():
    clear_console()
    print(ASCII_ART)
    print("Initializing...")

    if not is_ffmpeg_available():
        print("\n[ERROR] FFmpeg not found!")
        print("Please install FFmpeg and ensure it is in your PATH environment variable.")
        input("\nPress Enter to exit...")
        return

    while True:
        url = input("\n[?] Enter YouTube URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
        if not url:
            print("No URL provided.")
            continue

        downloads_dir = Path.home() / "Downloads" / "yt_mp3_temp"
        mp3_path = download_audio_to_mp3(url, downloads_dir)

        if mp3_path is None or not mp3_path.exists():
            print("Failed to download or convert to MP3.")
            continue

        save_dir = prompt_save_location(str(mp3_path.name))
        final_path = save_dir / mp3_path.name

        try:
            if final_path.exists():
                os.remove(final_path)
            
            if mp3_path.resolve() != final_path.resolve():
                mp3_path.rename(final_path)
            
            print(f"\n[SUCCESS] MP3 saved to: {final_path}")
            
            if sys.platform.startswith("win"):
                os.startfile(str(final_path))
            elif sys.platform.startswith("darwin"):
                subprocess.call(["open", str(final_path)])
            else:
                subprocess.call(["xdg-open", str(final_path)])
                
        except Exception as e:
            print(f"Could not move file or open it: {e}")
        
        try:
            downloads_dir.rmdir()
        except:
            pass

if __name__ == "__main__":
    main()