#!/usr/bin/env python3
# 国内IPTV列表生成脚本
import os

# 国内稳定频道源（央视频道示例）
CHANNELS = [
    ("CCTV-1 综合", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8", "https://p0.ssl.qhimg.com/t01065a244095ef204.png"),
    ("CCTV-2 财经", "http://ivi.bupt.edu.cn/hls/cctv2hd.m3u8", "https://p0.ssl.qhimg.com/t0108f52142c135254.png"),
    ("CCTV-3 综艺", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8", "https://p0.ssl.qhimg.com/t011f2891018090900.png"),
    ("CCTV-4 中文国际", "http://ivi.bupt.edu.cn/hls/cctv4hd.m3u8", "https://p0.ssl.qhimg.com/t019828c5419091109.png"),
    ("CCTV-5 体育", "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8", "https://p0.ssl.qhimg.com/t019838d5419091110.png")
]

def generate_playlist():
    # 创建输出文件
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        # 写入m3u8头部
        f.write("#EXTM3U\n\n")
        # 写入频道信息
        for name, url, logo in CHANNELS:
            f.write(f"#EXTINF:-1 tvg-logo=\"{logo}\",{name}\n")
            f.write(f"{url}\n\n")
    print("✅ 国内IPTV列表生成完成：playlist.m3u8")

if __name__ == "__main__":
    generate_playlist()
