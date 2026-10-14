# -*- coding: utf-8 -*-
# 混元3D资产批量下载器v2：流式落盘+进度日志文件（不依赖管道）
# 用法: python batch_download_hunyuan.py
import os, sys, urllib.request, concurrent.futures, re, time

import argparse as _ap
_p = _ap.ArgumentParser(); _p.add_argument("--base", default=os.environ.get("ZH3D_ASSETS") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "hunyuan"))
BASE = _p.parse_args().base
MANIFEST = os.path.join(BASE, "manifest.tsv")
LOG = os.path.join(BASE, "progress.log")
PREFIX = "https://hunyuan-base-prod-1258344703.cos.ap-guangzhou.myqcloud.com/hunyuan3d/default/"

DATE2DIR = {
    "2026-09-18": "00_期外0918",
    "2026-09-19": "01_居家办公",
    "2026-09-20": "02_城市日常",
    "2026-09-21": "03_商务职场",
    "2026-09-22": "04_餐饮美食",
    "2026-09-23": "05_校园青春",
    "2026-09-28": "10_商店购物",
    "2026-09-29": "11_家庭亲情",
    "2026-09-30": "12_角色卡0930",
    "2026-10-01": "13_节日庆典",
    "2026-10-02": "14_旅行出行",
    "2026-10-03": "15_宠物生活",
}

logf = open(LOG, "w", encoding="utf-8")
def log(msg):
    logf.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    logf.flush()

def sanitize(name):
    return re.sub(r'[\\/:*?"<>|\s]+', "", name)[:24]

tasks = []
counter = {}
for line in open(MANIFEST, encoding="utf-8"):
    line = line.strip()
    if not line or line.count("|") < 3:
        continue
    parts = line.split("|", 4)
    date, title, u1, u2 = parts[:4]
    # 第5列可选=显式归类目录（相对hunyuan/，如16_生肖）
    d = parts[4] if len(parts) == 5 else DATE2DIR.get(date, "00_期外" + date.replace("-", ""))
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
    counter[d] = counter.get(d, 0) + 1
    fn = f"{date.replace('-','')[4:]}_{counter[d]:02d}_{sanitize(title)}.glb"
    out = os.path.join(BASE, d, fn)
    if not os.path.exists(out):
        tasks.append((u1, u2, out))

log(f"待下载 {len(tasks)} 个")

def dl(t):
    u1, u2, out = t
    url = f"{PREFIX}{u1}/{u2}.glb"
    tmp = out + ".part"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
            n = 0
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                n += len(chunk)
        if n < 500:
            os.remove(tmp)
            return ("SMALL", out, n)
        os.replace(tmp, out)
        return ("OK", out, n)
    except Exception as e:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        return ("FAIL", out, str(e)[:80])

ok = fail = small = 0
t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(dl, t) for t in tasks]
    for i, fu in enumerate(concurrent.futures.as_completed(futures), 1):
        st, out, info = fu.result()
        mb = info / 1048576 if isinstance(info, int) else 0
        if st == "OK":
            ok += 1
            log(f"{i}/{len(tasks)} OK {os.path.relpath(out, BASE)} {mb:.1f}MB")
        elif st == "SMALL":
            small += 1
            log(f"{i}/{len(tasks)} SMALL {os.path.basename(out)} {info}B")
        else:
            fail += 1
            log(f"{i}/{len(tasks)} FAIL {os.path.basename(out)}: {info}")
        if i % 20 == 0:
            log(f"== 进度 {i}/{len(tasks)}, 已{ok}失败{fail}, 用时{time.time()-t0:.0f}s")

log(f"完成: OK={ok} SMALL={small} FAIL={fail}")
logf.close()
print(f"DONE OK={ok} FAIL={fail}")
