#!/usr/bin/env python3
# 全自动IPTV：拉取+校验+优选+生成【播放器友好版】
# 生成的playlist.m3u8可直接导入播放器，显示分类频道列表，一键换台
import requests
import re
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# ===================== 核心配置（无需修改）=====================
# 优质公共IPTV源（已筛选，保证播放器兼容性）
PUBLIC_IPTV_SOURCES = [
    "https://raw.githubusercontent.com/51itgg/IPTV/main/m3u/iptv.m3u8",
    "https://raw.githubusercontent.com/ccf-2012/IPTV/main/IPTV.m3u8",
    "https://raw.githubusercontent.com/zhuhansan666/IPTV/main/iptv.m3u8",
    "https://raw.githubusercontent.com/yuanguozheng/IPTV/main/iptv.m3u8"
]
THREAD_NUM = 15          # 并发校验线程（平衡速度与稳定性）
TIMEOUT = 6              # 源校验超时时间（秒）
KEEP_BEST_N = 1          # 同频道保留最优源数量
FILTER_KEYWORDS = ["广告", "测试", "购物", "付费", "VIP", "破解", "成人"]
OUTPUT_FILE = "playlist.m3u8"

# 频道分类（播放器会识别#EXTGRP标签显示分类列表）
CHANNEL_CATEGORIES = {
    "央视": ["CCTV-", "央视"],
    "卫视": ["湖南卫视", "浙江卫视", "东方卫视", "江苏卫视", "北京卫视", "安徽卫视", "山东卫视", "天津卫视", "湖北卫视", "河南卫视", "江西卫视", "四川卫视", "重庆卫视", "广东卫视"],
    "地方台": ["珠江", "南方", "深圳", "广州", "杭州", "南京", "成都", "武汉", "长沙", "青岛", "大连", "厦门"],
    "特色频道": ["卡通", "体育", "动漫", "新闻", "电影", "综艺"]
}

# ===================== 工具函数 =====================
def pull_public_source(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=12)
        res.raise_for_status()
        if res.text.startswith("#EXTM3U"):
            print(f"✅ 拉取成功：{url}")
            return res.text
        else:
            print(f"❌ 非标准m3u8：{url}")
            return None
    except Exception as e:
        print(f"❌ 拉取失败 {url}：{str(e)[:50]}")
        return None

def parse_m3u8(m3u8_content):
    channels = {}
    lines = [line.strip() for line in m3u8_content.split("\n") if line.strip()]
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF:") and i+1 < len(lines) and not lines[i+1].startswith("#"):
            name_match = re.search(r',(.*)$', lines[i])
            if not name_match:
                continue
            channel_name = name_match.group(1).strip()
            if any(key in channel_name for key in FILTER_KEYWORDS):
                continue
            play_url = lines[i+1].strip()
            if play_url.startswith(("http://", "https://")) and (".m3u8" in play_url or "hls" in play_url or "ts" in play_url):
                if channel_name not in channels:
                    channels[channel_name] = []
                if play_url not in channels[channel_name]:
                    channels[channel_name].append(play_url)
    print(f"📌 解析出 {len(channels)} 个原始频道")
    return channels

def check_source(channel_name, url):
    try:
        start_time = time.time()
        # 轻量校验：只请求头，不下载内容
        requests.head(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        delay = round((time.time() - start_time) * 1000, 2)
        print(f"✅ [{channel_name}] 有效 | 延迟：{delay}ms | {url[:60]}...")
        return (channel_name, url, delay)
    except Exception:
        return None

# 匹配频道分类（给播放器显示分类列表）
def get_channel_category(channel_name):
    for category, keywords in CHANNEL_CATEGORIES.items():
        if any(keyword in channel_name for keyword in keywords):
            return category
    return "其他频道"

# ===================== 主逻辑 =====================
def main():
    print("===== 1. 拉取公共IPTV源 =====")
    all_m3u8 = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(pull_public_source, url) for url in PUBLIC_IPTV_SOURCES]
        for future in as_completed(futures):
            res = future.result()
            if res:
                all_m3u8.append(res)
    if not all_m3u8:
        print("❌ 无有效源，退出")
        return
    all_m3u8_content = "\n".join(all_m3u8)

    print("===== 2. 解析并去重频道 =====")
    channels = parse_m3u8(all_m3u8_content)
    if not channels:
        print("❌ 无有效频道，退出")
        return

    print("===== 3. 校验源可用性（测速） =====")
    valid_sources = []
    with ThreadPoolExecutor(max_workers=THREAD_NUM) as executor:
        futures = []
        for name, urls in channels.items():
            for url in urls:
                futures.append(executor.submit(check_source, name, url))
        for future in as_completed(futures):
            res = future.result()
            if res:
                valid_sources.append(res)
    if not valid_sources:
        print("❌ 无有效播放源，退出")
        return
    print(f"📌 校验出 {len(valid_sources)} 个有效播放源")

    print("===== 4. 同频道优选 =====")
    optimized_channels = {}
    for name, url, delay in valid_sources:
        if name not in optimized_channels:
            optimized_channels[name] = []
        optimized_channels[name].append((url, delay))
    # 按延迟排序，保留最优N个
    for name in optimized_channels:
        optimized_channels[name].sort(key=lambda x: (x[1], -len(x[0])))
        optimized_channels[name] = optimized_channels[name][:KEEP_BEST_N]
    print(f"📌 优选后保留 {len(optimized_channels)} 个可用频道")

    print("===== 5. 生成播放器友好的m3u8 =====")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # 标准头部（带EPG节目单，播放器可显示节目预告）
        f.write("#EXTM3U x-tvg-url=\"https://epg.112114.xyz/epg.xml\",charset=\"utf-8\"\n\n")
        
        # 按分类生成（播放器会识别#EXTGRP显示分类）
        categorized_channels = {}
        for name, sources in optimized_channels.items():
            category = get_channel_category(name)
            if category not in categorized_channels:
                categorized_channels[category] = []
            categorized_channels[category].append((name, sources))
        
        # 写入分类和频道
        for category, channels in sorted(categorized_channels.items()):
            f.write(f"#EXTGRP:{category}\n")  # 播放器分类标签
            for name, sources in sorted(channels, key=lambda x: x[0]):
                for url, _ in sources:
                    # 带logo+分类的标准格式
                    f.write(f"#EXTINF:-1 tvg-id=\"{name}\" tvg-logo=\"https://p0.ssl.qhimg.com/t01065a244095ef204.png\" group-title=\"{category}\",{name}\n")
                    f.write(f"{url}\n\n")

    # 验证生成结果
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        total_lines = sum(1 for _ in open(OUTPUT_FILE, encoding="utf-8"))
        total_channels = int((total_lines - 1) / 3)  # 扣除头部，每3行一个频道
        print(f"✅ 生成完成！{OUTPUT_FILE} | 可用频道：{total_channels} 个 | 文件大小：{os.path.getsize(OUTPUT_FILE)/1024:.2f}KB")
        print(f"✅ 播放器导入链接：https://raw.githubusercontent.com/你的用户名/你的仓库名/main/{OUTPUT_FILE}")
    else:
        print(f"❌ 生成失败")

if __name__ == "__main__":
    main()
