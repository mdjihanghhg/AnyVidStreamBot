import validators

def extract_direct_link(url: str) -> str:
    if "terabox" in url:
        return url  # ভবিষ্যতে scraper যুক্ত করা যাবে
    elif "mediafire" in url:
        return url  # mediafire direct detect placeholder
    elif "drive.google.com" in url and "/d/" in url:
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            return None
    elif validators.url(url) and any(url.endswith(ext) for ext in [".mp4", ".mkv", ".webm", ".m3u8"]):
        return url
    return None
