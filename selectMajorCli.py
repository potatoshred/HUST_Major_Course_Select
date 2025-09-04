
################################################

# 必填，打开浏览器找一下
Cookie = "打开浏览器找一下"

# 想选的课自己改
select_course = [
    ("大数据管理概论", "左琼"),
    ("函数式编程原理", "郑然"),
    ("计算机图形学", "何云峰"),
    ("计算机视觉导论", "刘康"),
]

# 一般不需要动UA
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

#################################################

import requests

cookies = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": Cookie,
    "Host": "wsxk.hust.edu.cn",
    "Pragma": "no-cache",
    "Referer": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": UA,
    "X-Requested-With": "XMLHttpRequest",
}
sess = requests.Session()

def post_select(kcbh, ktbh, fzid, faid, xqh, kcmc, jsxm):
    try:
        cookies["Referer"] = f"https://wsxk.hust.edu.cn/zyxxk/Stuxk/jumpAktxk?fzid={fzid}&kcbh={kcbh}&faid={faid}&sfid="
        data = {
            "kcbh": kcbh,
            "ktbh": ktbh, # 课堂编号
            "fzid": fzid,
            "sfid": "",
            "faid": faid,
            "xqh": xqh, # 学期号
        }
        tst = sess.post("https://wsxk.hust.edu.cn/zyxxk/Stuxk/addStuxkIsxphx", headers=cookies, params=data).json()
        print(kcmc, jsxm, tst)
    except:
        print(kcmc, jsxm, "FAIL")



cookies["Referer"] = "https://wsxk.hust.edu.cn/zyxxk/Stuxk/jumpAkcxk?fzxkfs=&xkgz=1"
data = {
    "page": 1,
    "xkgz": 1, # 选课规则
    "limit": 10,
    "fzxkfs": "", # 分组选课方式
}
tst = sess.post("https://wsxk.hust.edu.cn/zyxxk/Stuxk/getXsFaFZkc",
                headers=cookies, params=data).json()
for kc in tst['data']:
    kcmc, fzid, kcbh, faid, xqh = kc['KCMC'], kc['FZID'], kc['KCBH'], kc['ID'], kc['XQH']
    print(xqh, faid, kcmc, fzid, kcbh)

    cookies["Referer"] = f"https://wsxk.hust.edu.cn/zyxxk/Stuxk/jumpAktxk?fzid={fzid}&kcbh={kcbh}&faid={faid}&sfid="
    data = {
        "page": 1,
        "limit": 10,
        "fzid": fzid, # 分组ID
        "kcbh": kcbh, # 课程编号
        "sfid": "",
        "faid": faid, # 方案ID
        "id": faid,
    }
    tst = sess.post("https://wsxk.hust.edu.cn/zyxxk/Stuxk/getFzkt",
                    headers=cookies, params=data).json()
    for kt in tst['data']:
        ktbh = kt['KTBH'] # 课堂编号
        jsxm = kt['XM']   # 教师姓名
        if (kcmc, jsxm) in select_course:
            post_select(kcbh, ktbh, fzid, faid, xqh, kcmc, jsxm)
            select_course.remove( (kcmc, jsxm) )


for c in select_course:
    print(*c, "未找到课程，请检查是否有拼写错误")