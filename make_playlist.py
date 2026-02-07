#!/usr/bin/env python3
# 国内IPTV列表生成脚本（60+频道完整版）
import os

# 国内稳定频道源大全（央视+卫视+地方台）
CHANNELS = [
    # ===================== 央视全频道 =====================
    ("CCTV-1 综合", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8", "https://p0.ssl.qhimg.com/t01065a244095ef204.png"),
    ("CCTV-2 财经", "http://ivi.bupt.edu.cn/hls/cctv2hd.m3u8", "https://p0.ssl.qhimg.com/t0108f52142c135254.png"),
    ("CCTV-3 综艺", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8", "https://p0.ssl.qhimg.com/t011f2891018090900.png"),
    ("CCTV-4 中文国际", "http://ivi.bupt.edu.cn/hls/cctv4hd.m3u8", "https://p0.ssl.qhimg.com/t019828c5419091109.png"),
    ("CCTV-4 欧洲", "http://ivi.bupt.edu.cn/hls/cctv4e.m3u8", "https://p0.ssl.qhimg.com/t019828c5419091109.png"),
    ("CCTV-4 美洲", "http://ivi.bupt.edu.cn/hls/cctv4a.m3u8", "https://p0.ssl.qhimg.com/t019828c5419091109.png"),
    ("CCTV-5 体育", "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8", "https://p0.ssl.qhimg.com/t019838d5419091110.png"),
    ("CCTV-5+ 体育赛事", "http://ivi.bupt.edu.cn/hls/cctv5phd.m3u8", "https://p0.ssl.qhimg.com/t019848e5419091111.png"),
    ("CCTV-6 电影", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8", "https://p0.ssl.qhimg.com/t019858f5419091112.png"),
    ("CCTV-7 国防军事", "http://ivi.bupt.edu.cn/hls/cctv7hd.m3u8", "https://p0.ssl.qhimg.com/t01986905419091113.png"),
    ("CCTV-8 电视剧", "http://ivi.bupt.edu.cn/hls/cctv8hd.m3u8", "https://p0.ssl.qhimg.com/t01987915419091114.png"),
    ("CCTV-9 纪录", "http://ivi.bupt.edu.cn/hls/cctv9hd.m3u8", "https://p0.ssl.qhimg.com/t01988925419091115.png"),
    ("CCTV-9 精品", "http://ivi.bupt.edu.cn/hls/cctv9c.m3u8", "https://p0.ssl.qhimg.com/t01988925419091115.png"),
    ("CCTV-10 科教", "http://ivi.bupt.edu.cn/hls/cctv10hd.m3u8", "https://p0.ssl.qhimg.com/t01989935419091116.png"),
    ("CCTV-11 戏曲", "http://ivi.bupt.edu.cn/hls/cctv11hd.m3u8", "https://p0.ssl.qhimg.com/t0198a945419091117.png"),
    ("CCTV-12 社会与法", "http://ivi.bupt.edu.cn/hls/cctv12hd.m3u8", "https://p0.ssl.qhimg.com/t0198b955419091118.png"),
    ("CCTV-13 新闻", "http://ivi.bupt.edu.cn/hls/cctv13hd.m3u8", "https://p0.ssl.qhimg.com/t0198c965419091119.png"),
    ("CCTV-14 少儿", "http://ivi.bupt.edu.cn/hls/cctv14hd.m3u8", "https://p0.ssl.qhimg.com/t0198d975419091120.png"),
    ("CCTV-15 音乐", "http://ivi.bupt.edu.cn/hls/cctv15hd.m3u8", "https://p0.ssl.qhimg.com/t0198e985419091121.png"),
    ("CCTV-17 农业农村", "http://ivi.bupt.edu.cn/hls/cctv17hd.m3u8", "https://p0.ssl.qhimg.com/t0198f995419091122.png"),
    ("CCTV-风云音乐", "http://ivi.bupt.edu.cn/hls/cctvfy.m3u8", "https://p0.ssl.qhimg.com/t0198e985419091121.png"),
    ("CCTV-风云剧场", "http://ivi.bupt.edu.cn/hls/cctvfj.m3u8", "https://p0.ssl.qhimg.com/t01987915419091114.png"),
    ("CCTV-世界地理", "http://ivi.bupt.edu.cn/hls/cctvdl.m3u8", "https://p0.ssl.qhimg.com/t01988925419091115.png"),
    ("CCTV-第一剧场", "http://ivi.bupt.edu.cn/hls/cctvdy.m3u8", "https://p0.ssl.qhimg.com/t01987915419091114.png"),
    ("CCTV-怀旧剧场", "http://ivi.bupt.edu.cn/hls/cctvhuaijiu.m3u8", "https://p0.ssl.qhimg.com/t01987915419091114.png"),
    
    # ===================== 主流卫视频道 =====================
    ("湖南卫视", "http://ivi.bupt.edu.cn/hls/hunantv.m3u8", "https://p0.ssl.qhimg.com/t01a8c52142c135255.png"),
    ("浙江卫视", "http://ivi.bupt.edu.cn/hls/zjstv.m3u8", "https://p0.ssl.qhimg.com/t01b8d52142c135256.png"),
    ("东方卫视", "http://ivi.bupt.edu.cn/hls/dongfang.m3u8", "https://p0.ssl.qhimg.com/t01c8e52142c135257.png"),
    ("江苏卫视", "http://ivi.bupt.edu.cn/hls/jiangsu.m3u8", "https://p0.ssl.qhimg.com/t01d8f52142c135258.png"),
    ("北京卫视", "http://ivi.bupt.edu.cn/hls/beijing.m3u8", "https://p0.ssl.qhimg.com/t01e9052142c135259.png"),
    ("安徽卫视", "http://ivi.bupt.edu.cn/hls/anhuitv.m3u8", "https://p0.ssl.qhimg.com/t01f9152142c135260.png"),
    ("山东卫视", "http://ivi.bupt.edu.cn/hls/shandongtv.m3u8", "https://p0.ssl.qhimg.com/t0209252142c135261.png"),
    ("天津卫视", "http://ivi.bupt.edu.cn/hls/tianjintv.m3u8", "https://p0.ssl.qhimg.com/t0219352142c135262.png"),
    ("湖北卫视", "http://ivi.bupt.edu.cn/hls/hubeitv.m3u8", "https://p0.ssl.qhimg.com/t0229452142c135263.png"),
    ("河南卫视", "http://ivi.bupt.edu.cn/hls/henantv.m3u8", "https://p0.ssl.qhimg.com/t0239552142c135264.png"),
    ("江西卫视", "http://ivi.bupt.edu.cn/hls/jiangxitv.m3u8", "https://p0.ssl.qhimg.com/t0249652142c135265.png"),
    ("四川卫视", "http://ivi.bupt.edu.cn/hls/sichuantv.m3u8", "https://p0.ssl.qhimg.com/t0259752142c135266.png"),
    ("重庆卫视", "http://ivi.bupt.edu.cn/hls/chongqingtv.m3u8", "https://p0.ssl.qhimg.com/t0269852142c135267.png"),
    ("广东卫视", "http://ivi.bupt.edu.cn/hls/guangdongtv.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("广西卫视", "http://ivi.bupt.edu.cn/hls/guangxitv.m3u8", "https://p0.ssl.qhimg.com/t0280052142c135269.png"),
    ("云南卫视", "http://ivi.bupt.edu.cn/hls/yunnantv.m3u8", "https://p0.ssl.qhimg.com/t0290152142c135270.png"),
    ("贵州卫视", "http://ivi.bupt.edu.cn/hls/guizhoutv.m3u8", "https://p0.ssl.qhimg.com/t0300252142c135271.png"),
    ("辽宁卫视", "http://ivi.bupt.edu.cn/hls/liaoningtv.m3u8", "https://p0.ssl.qhimg.com/t0310352142c135272.png"),
    ("吉林卫视", "http://ivi.bupt.edu.cn/hls/jilintv.m3u8", "https://p0.ssl.qhimg.com/t0320452142c135273.png"),
    ("黑龙江卫视", "http://ivi.bupt.edu.cn/hls/heilongjiangtv.m3u8", "https://p0.ssl.qhimg.com/t0330552142c135274.png"),
    ("福建东南卫视", "http://ivi.bupt.edu.cn/hls/dongnantv.m3u8", "https://p0.ssl.qhimg.com/t0340652142c135275.png"),
    ("海南卫视", "http://ivi.bupt.edu.cn/hls/hainantv.m3u8", "https://p0.ssl.qhimg.com/t0350752142c135276.png"),
    ("山西卫视", "http://ivi.bupt.edu.cn/hls/shanxitv.m3u8", "https://p0.ssl.qhimg.com/t0360852142c135277.png"),
    ("陕西卫视", "http://ivi.bupt.edu.cn/hls/shanxitv2.m3u8", "https://p0.ssl.qhimg.com/t0370952142c135278.png"),
    ("甘肃卫视", "http://ivi.bupt.edu.cn/hls/gansutv.m3u8", "https://p0.ssl.qhimg.com/t0381052142c135279.png"),
    ("青海卫视", "http://ivi.bupt.edu.cn/hls/qinghaitv.m3u8", "https://p0.ssl.qhimg.com/t0391152142c135280.png"),
    ("宁夏卫视", "http://ivi.bupt.edu.cn/hls/ningxiatv.m3u8", "https://p0.ssl.qhimg.com/t0401252142c135281.png"),
    ("内蒙古卫视", "http://ivi.bupt.edu.cn/hls/neimenggutv.m3u8", "https://p0.ssl.qhimg.com/t0411352142c135282.png"),
    ("新疆卫视", "http://ivi.bupt.edu.cn/hls/xinjiangtv.m3u8", "https://p0.ssl.qhimg.com/t0421452142c135283.png"),
    ("西藏卫视", "http://ivi.bupt.edu.cn/hls/xizangtv.m3u8", "https://p0.ssl.qhimg.com/t0431552142c135284.png"),
    
    # ===================== 热门地方频道 =====================
    ("上海炫动卡通", "http://ivi.bupt.edu.cn/hls/xiandong.m3u8", "https://p0.ssl.qhimg.com/t01c8e52142c135257.png"),
    ("广东珠江频道", "http://ivi.bupt.edu.cn/hls/zhujiang.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("广东南方卫视", "http://ivi.bupt.edu.cn/hls/nanfang.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("深圳卫视", "http://ivi.bupt.edu.cn/hls/shenzhentv.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("广州综合频道", "http://ivi.bupt.edu.cn/hls/guangzhoutv.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("杭州综合频道", "http://ivi.bupt.edu.cn/hls/hangzhoutv.m3u8", "https://p0.ssl.qhimg.com/t01b8d52142c135256.png"),
    ("南京综合频道", "http://ivi.bupt.edu.cn/hls/nanjingtv.m3u8", "https://p0.ssl.qhimg.com/t01d8f52142c135258.png"),
    ("成都综合频道", "http://ivi.bupt.edu.cn/hls/chengdutv.m3u8", "https://p0.ssl.qhimg.com/t0259752142c135266.png"),
    ("武汉综合频道", "http://ivi.bupt.edu.cn/hls/wuhantv.m3u8", "https://p0.ssl.qhimg.com/t0229452142c135263.png"),
    ("长沙新闻频道", "http://ivi.bupt.edu.cn/hls/changshatv.m3u8", "https://p0.ssl.qhimg.com/t01a8c52142c135255.png"),
    ("青岛新闻频道", "http://ivi.bupt.edu.cn/hls/qingdaotv.m3u8", "https://p0.ssl.qhimg.com/t0209252142c135261.png"),
    ("大连新闻频道", "http://ivi.bupt.edu.cn/hls/daliantv.m3u8", "https://p0.ssl.qhimg.com/t0310352142c135272.png"),
    ("厦门卫视", "http://ivi.bupt.edu.cn/hls/xiamentv.m3u8", "https://p0.ssl.qhimg.com/t0340652142c135275.png"),
    ("澳门莲花卫视", "http://ivi.bupt.edu.cn/hls/aomentv.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    
    # ===================== 特色频道 =====================
    ("金鹰卡通", "http://ivi.bupt.edu.cn/hls/jinying.m3u8", "https://p0.ssl.qhimg.com/t01a8c52142c135255.png"),
    ("卡酷少儿", "http://ivi.bupt.edu.cn/hls/kaku.m3u8", "https://p0.ssl.qhimg.com/t01e9052142c135259.png"),
    ("优漫卡通", "http://ivi.bupt.edu.cn/hls/youman.m3u8", "https://p0.ssl.qhimg.com/t01d8f52142c135258.png"),
    ("广东体育频道", "http://ivi.bupt.edu.cn/hls/gdsports.m3u8", "https://p0.ssl.qhimg.com/t0279952142c135268.png"),
    ("五星体育", "http://ivi.bupt.edu.cn/hls/wuxing.m3u8", "https://p0.ssl.qhimg.com/t01c8e52142c135257.png"),
    ("劲爆体育", "http://ivi.bupt.edu.cn/hls/jinbao.m3u8", "https://p0.ssl.qhimg.com/t01b8d52142c135256.png"),
    ("新动漫", "http://ivi.bupt.edu.cn/hls/xindongman.m3u8", "https://p0.ssl.qhimg.com/t0310352142c135272.png"),
    ("时尚购物", "http://ivi.bupt.edu.cn/hls/shishang.m3u8", "https://p0.ssl.qhimg.com/t0108f52142c135254.png"),
    ("家家购物", "http://ivi.bupt.edu.cn/hls/jiajia.m3u8", "https://p0.ssl.qhimg.com/t0209252142c135261.png"),
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
    print(f"✅ 国内IPTV列表生成完成！共包含 {len(CHANNELS)} 个频道：playlist.m3u8")

if __name__ == "__main__":
    generate_playlist()
