#!/usr/bin/env python3
# 全自动IPTV：拉取公共源+多源校验+优选+生成 核心脚本
# 无需手动维护，一键执行，全程自动化
import requests
import re
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# ===================== 配置项（可按需微调，默认无需修改）=====================
# 全网优质公共IPTV源仓库（多源备份，拉取m3u8格式源）
PUBLIC_IPTV_SOURCES = [
    "https://raw.githubusercontent.com/imDazui/Tvlist-awesome-m3u8/master/ipTV.m3u8",
    "https://raw.githubusercontent.com/666wcy/TV/main/tv.m3u8",
    "https://raw.githubusercontent.com/wangrongding/IPTV/master/IPTV.m3u8",
    "https://raw.githubusercontent.com/HeiSir2020/IPTV/main/iptv.m3u8",
    "https://raw.githubusercontent.com/caoxinyu/IPTV/master/iptv.m3u8"
]
# 线程数（测速并发，按需调整，默认10）
THREAD_NUM = 10
# 超时时间（秒，过滤超时源）
TIMEOUT = 5
# 同频道优选：保留延迟最低的N个源（默认1，只留最优）
KEEP_BEST_N = 1
# 过滤无效频道关键词（避免广告/无效台）
FILTER_KEYWORDS = ["广告", "测试", "购物", "付费", "VIP", "破解"]
# 输出文件
OUTPUT_FILE = "playlist.m3u8"

# ===================== 工具函数 =====================
# 拉取公共源
def pull_public_source(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        if res.text.startswith("#EXTM3U"):
            print(f"✅ 成功拉取源：{url}")
            return res.text
        else:
            print(f"❌ 非标准m3u8源：{url}")
            return None
    except Exception as e:
        print(f"❌ 拉取源失败 {url}：{str(e)[:50]}")
        return None

# 解析m3u8，提取频道{名称: [地址1, 地址2,...]}
def parse_m3u8(m3u8_content):
    channels = {}
    lines = [line.strip() for line in m3u8_content.split("\n") if line.strip()]
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF:") and i+1 < len(lines) and not lines[i+1].startswith("#"):
            # 提取频道名称
            name_match = re.search(r',(.*)$', lines[i])
            if not name_match:
                continue
            channel_name = name_match.group(1).strip()
            # 过滤无效关键词
            if any(key in channel_name for key in FILTER_KEYWORDS):
                continue
            # 提取播放地址
            play_url = lines[i+1].strip()
            # 只保留http/https/m3u8格式地址
            if play_url.startswith(("http://", "https://")) and (".m3u8" in play_url or "hls" in play_url):
                if channel_name not in channels:
                    channels[channel_name] = []
                if play_url not in channels[channel_name]:
                    channels[channel_name].append(play_url)
    print(f"📌 解析完成，共提取 {len(channels)} 个频道，待校验")
    return channels

# 测速+可用性校验（核心：过滤失效源，计算延迟）
def check_source(channel_name, url):
    try:
        # 1. 网络连通性检测
        parsed = urlparse(url)
        start_time = time.time()
        # 简单GET头校验，避免全量下载
        requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        delay = round((time.time() - start_time) * 1000, 2)  # 延迟(ms)
        print(f"✅ [{channel_name}] 有效 | 延迟：{delay}ms | {url[:50]}...")
        return (channel_name, url, delay)
    except Exception as e:
        # print(f"❌ [{channel_name}] 失效 | {url[:50]}...")
        return None

# ===================== 主逻辑：拉取→解析→校验→优选→生成 =====================
def main():
    print("===== 开始全自动IPTV处理：拉取公共源 =====")
    # 1. 批量拉取所有公共源
    all_m3u8 = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(pull_public_source, url) for url in PUBLIC_IPTV_SOURCES]
        for future in as_completed(futures):
            res = future.result()
            if res:
                all_m3u8.append(res)
    if not all_m3u8:
        print("❌ 所有公共源拉取失败，退出")
        return
    # 合并所有源
    all_m3u8_content = "\n".join(all_m3u8)

    print("===== 解析频道，去重 =====")
    # 2. 解析并去重
    channels = parse_m3u8(all_m3u8_content)
    if not channels:
        print("❌ 未解析到有效频道，退出")
        return

    print("===== 多线程校验源可用性（测速） =====")
    # 3. 多线程校验所有源，过滤失效
    valid_sources = []
    with ThreadPoolExecutor(max_workers=THREAD_NUM) as executor:
        futures = []
        for name, urls in channels.items():
            for url in urls:
                futures.append(executor.submit(check_source, name, url))
        # 收集有效结果
        for future in as_completed(futures):
            res = future.result()
            if res:
                valid_sources.append(res)
    if not valid_sources:
        print("❌ 无有效播放源，退出")
        return
    print(f"📌 校验完成，共筛选出 {len(valid_sources)} 个有效源")

    print("===== 同频道优选（按延迟排序） =====")
    # 4. 同频道按延迟排序，保留最优N个
    optimized_channels = {}
    for name, url, delay in valid_sources:
        if name not in optimized_channels:
            optimized_channels[name] = []
        optimized_channels[name].append((url, delay))
    # 排序+截取最优N个
    for name in optimized_channels:
        # 按延迟升序，再按地址长度降序（优先完整源）
        optimized_channels[name].sort(key=lambda x: (x[1], -len(x[0])))
        optimized_channels[name] = optimized_channels[name][:KEEP_BEST_N]
    print(f"📌 优选完成，最终保留 {len(optimized_channels)} 个可用频道")

    print("===== 生成标准m3u8播放列表 =====")
    # 5. 生成标准m3u8文件（带tvg-logo占位，不影响播放）
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U x-tvg-url=\"https://epg.112114.xyz/epg.xml\"\n\n")  # 带EPG节目单
        for name, sources in sorted(optimized_channels.items(), key=lambda x: x[0]):
            for url, _ in sources:
                f.write(f"#EXTINF:-1 tvg-logo=\"https://p0.ssl.qhimg.com/t01065a244095ef204.png\",{name}\n")
                f.write(f"{url}\n\n")
    # 验证文件
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
        total_lines = sum(1 for _ in open(OUTPUT_FILE, encoding="utf-8"))
        total_channels = int(total_lines / 2) - 1  # 扣除头部
        print(f"✅ 最终生成 {OUTPUT_FILE} | 可用频道：{total_channels} 个 | 文件大小：{os.path.getsize(OUTPUT_FILE)/1024:.2f}KB")
    else:
        print(f"❌ 生成 {OUTPUT_FILE} 失败")

if __name__ == "__main__":
    main()
