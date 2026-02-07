#!/usr/bin/env python3
# 国内IPTV列表生成脚本
import os

# 国内稳定频道源（央视+卫视）
CHANNELS = [
    # 央视频道
    ("CCTV-1 综合", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8", "https://p0.ssl.qhimg.com/t01065a244095ef204.png"),
    ("CCTV-2 财经", "http://ivi.bupt.edu.cn/hls/cctv2hd.m3u8", "https://p0.ssl.qhimg.com/t0108f52142c135254.png"),
    ("CCTV-3 综艺", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8", "https://p0.ssl.qhimg.com/t011f2891018090900.png"),
    ("CCTV-4 中文国际", "http://ivi.bupt.edu.cn/hls/cctv4hd.m3u8", "https://p0.ssl.qhimg.com/t019828c5419091109.png"),
    ("CCTV-5 体育", "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8", "https://p0.ssl.qhimg.com/t019838d5419091110.png"),
    ("CCTV-5+ 体育赛事", "http://ivi.bupt.edu.cn/hls/cctv5phd.m3u8", "https://p0.ssl.qhimg.com/t019848e5419091111.png"),
    ("CCTV-6 电影", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8", "https://p0.ssl.qhimg.com/t019858f5419091112.png"),
    ("CCTV-7 国防军事", "http://ivi.bupt.edu.cn/hls/cctv7hd.m3u8", "https://p0.ssl.qhimg.com/t01986905419091113.png"),
    ("CCTV-8 电视剧", "http://ivi.bupt.edu.cn/hls/cctv8hd.m3u8", "https://p0.ssl.qhimg.com/t01987915419091114.png"),
    ("CCTV-9 纪录", "http://ivi.bupt.edu.cn/hls/cctv9hd.m3u8", "https://p0.ssl.qhimg.com/t01988925419091115.png"),
    ("CCTV-10 科教", "http://ivi.bupt.edu.cn/hls/cctv10hd.m3u8", "https://p0.ssl.qhimg.com/t01989935419091116.png"),
    ("CCTV-11 戏曲", "http://ivi.bupt.edu.cn/hls/cctv11hd.m3u8", "https://p0.ssl.qhimg.com/t0198a945419091117.png"),
    ("CCTV-12 社会与法", "http://ivi.bupt.edu.cn/hls/cctv12hd.m3u8", "https://p0.ssl.qhimg.com/t0198b955419091118.png"),
    ("CCTV-13 新闻", "http://ivi.bupt.edu.cn/hls/cctv13hd.m3u8", "https://p0.ssl.qhimg.com/t0198c965419091119.png"),
    ("CCTV-14 少儿", "http://ivi.bupt.edu.cn/hls/cctv14hd.m3u8", "https://p0.ssl.qhimg.com/t0198d975419091120.png"),
    ("CCTV-15 音乐", "http://ivi.bupt.edu.cn/hls/cctv15hd.m3u8", "https://p0.ssl.qhimg.com/t0198e985419091121.png"),
    ("CCTV-17 农业农村", "http://ivi.bupt.edu.cn/hls/cctv17hd.m3u8", "https://p0.ssl.qhimg.com/t0198f995419091122.png"),
    # 卫视频道
    ("湖南卫视", "http://ivi.bupt.edu.cn/hls/hunantv.m3u8", "https://p0.ssl.qhimg.com/t01a8c52142c135255.png"),
    ("浙江卫视", "http://ivi.bupt.edu.cn/hls/zjstv.m3u8", "https://p0.ssl.qhimg.com/t01b8d52142c135256.png"),
    ("东方卫视", "http://ivi.bupt.edu.cn/hls/dongfang.m3u8", "https://p0.ssl.qhimg.com/t01c8e52142c135257.png"),
    ("江苏卫视", "http://ivi.bupt.edu.cn/hls/jiangsu.m3u8", "https://p0.ssl.qhimg.com/t01d8f52142c135258.png"),
    ("北京卫视", "http://ivi.bupt.edu.cn/hls/beijing.m3u8", "https://p0.ssl.qhimg.com/t01e9052142c135259.png"),
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
