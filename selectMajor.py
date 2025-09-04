
## 旧的脚本入口已被GUI替代，逻辑已集成到run_main和on_run中。

# ================= GUI 部分 ===================
import tkinter as tkt
from tkinter import messagebox
from tkinter import ttk as tk

def run_main(Cookie, select_course, UA, result_callback=None):
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
            msg = f"{kcmc} {jsxm} 选课结果: {tst}"
            print(msg)
            if result_callback:
                result_callback(kcmc, jsxm, tst)
        except Exception as e:
            msg = f"{kcmc} {jsxm} 选课失败: {e}"
            print(msg)
            if result_callback:
                result_callback(kcmc, jsxm, f"FAIL: {e}")

    cookies["Referer"] = "https://wsxk.hust.edu.cn/zyxxk/Stuxk/jumpAkcxk?fzxkfs=&xkgz=1"
    data = {
        "page": 1,
        "xkgz": 1, # 选课规则
        "limit": 10,
        "fzxkfs": "", # 分组选课方式
    }
    try:
        tst = sess.post("https://wsxk.hust.edu.cn/zyxxk/Stuxk/getXsFaFZkc",
                        headers=cookies, params=data).json()
    except Exception as e:
        messagebox.showerror("请求失败", f"获取课程列表失败: {e}")
        return
    ret = tst.get('data', [])
    if not ret:
        messagebox.showerror("请求失败", f"获取课程列表失败: {"Cookie错误/失效/选课系统还没开"}")
        return
    for kc in tst.get('data', []):
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
        try:
            tst2 = sess.post("https://wsxk.hust.edu.cn/zyxxk/Stuxk/getFzkt",
                            headers=cookies, params=data).json()
        except Exception as e:
            print(f"获取课堂失败: {e}")
            continue
        for kt in tst2.get('data', []):
            ktbh = kt['KTBH'] # 课堂编号
            jsxm = kt['XM']   # 教师姓名
            if (kcmc, jsxm) in select_course:
                post_select(kcbh, ktbh, fzid, faid, xqh, kcmc, jsxm)
                select_course.remove( (kcmc, jsxm) )
        
    for c in select_course:
        print(*c, "未找到课程，请检查是否有拼写错误")

# --- GUI ---
class CourseRow:
    def __init__(self, master, course_name='', teacher_name='', on_remove=None):
        self.frame = tk.Frame(master)
        self.course_var = tkt.StringVar(value=course_name)
        self.teacher_var = tkt.StringVar(value=teacher_name)
        self.result_var = tkt.StringVar(value='')
        self.course_entry = tk.Entry(self.frame, textvariable=self.course_var, width=24)
        self.teacher_entry = tk.Entry(self.frame, textvariable=self.teacher_var, width=16)
        self.result_label = tk.Label(self.frame, textvariable=self.result_var, width=32, anchor='w')
        self.remove_btn = tk.Button(self.frame, text="删除", command=self.remove, width=5)
        self.on_remove = on_remove
        self.course_entry.grid(row=0, column=0, padx=2, pady=2)
        self.teacher_entry.grid(row=0, column=1, padx=2, pady=2)
        self.result_label.grid(row=0, column=2, padx=2, pady=2, sticky='w')
        self.remove_btn.grid(row=0, column=3, padx=2, pady=2)
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    def remove(self):
        if self.on_remove:
            self.on_remove(self)
        self.frame.destroy()
    def get(self):
        return self.course_var.get().strip(), self.teacher_var.get().strip()
    def set_result(self, msg):
        self.result_var.set(msg)

class CourseListFrame(tk.Frame):
    def __init__(self, master, initial_courses=None):
        super().__init__(master)
        self.rows = []
        self.header = tk.Frame(self)
        tk.Label(self.header, text="课程名", width=24).grid(row=0, column=0)
        tk.Label(self.header, text="教师名", width=16).grid(row=0, column=1)
        tk.Label(self.header, text="选课结果", width=32).grid(row=0, column=2)
        self.header.grid(row=0, column=0, sticky="w")
        self.rows_frame = tk.Frame(self)
        self.rows_frame.grid(row=1, column=0, sticky="w")
        self.add_btn = tk.Button(self, text="添加课程", command=self.add_row)
        self.add_btn.grid(row=2, column=0, sticky="w", pady=4)
        if initial_courses:
            for c, t in initial_courses:
                self.add_row(c, t)
        else:
            self.add_row()
    def add_row(self, course_name='', teacher_name=''):
        row = CourseRow(self.rows_frame, course_name, teacher_name, on_remove=self.remove_row)
        row.grid(row=len(self.rows), column=0, sticky="w")
        self.rows.append(row)
    def remove_row(self, row):
        self.rows.remove(row)
        self.refresh_rows()
    def refresh_rows(self):
        for idx, row in enumerate(self.rows):
            row.grid(row=idx, column=0, sticky="w")
    def get_courses(self):
        return [(c.strip(), t.strip()) for c, t in (row.get() for row in self.rows) if c and t]
    def set_result(self, kcmc, jsxm, msg):
        for row in self.rows:
            c, t = row.get()
            if c == kcmc and t == jsxm:
                row.set_result(msg)
                break
    def clear_results(self):
        for row in self.rows:
            row.set_result("")


# --- 结果显示区 ---
def on_run():
    cookie = cookie_entry.get().strip()
    ua = ua_entry.get().strip()
    courses = course_list_frame.get_courses()
    if not cookie or not ua or not courses:
        messagebox.showwarning("输入不完整", "请填写所有字段并至少输入一门课程且课程名和教师名都不能为空")
        return
    course_list_frame.clear_results()
    def show_result(kcmc, jsxm, result):
        msg = result
        if isinstance(result, dict) and 'msg' in result:
            msg = result['msg']
        else:
            msg = "失败，请重试"
        course_list_frame.set_result(kcmc, jsxm, msg)
    run_main(cookie, courses, ua, result_callback=show_result)

root = tkt.Tk()
# root.configure(bg="#cacaca")  # 设置为浅灰色
style = tk.Style()
style.theme_use('clam')  # 可选: 'clam', 'alt', 'default', 'classic'
root.title("HUST 专选选课助手")

tkt.Label(root, text="Cookie:").grid(row=0, column=0, sticky="e")
cookie_entry = tk.Entry(root, width=80)
cookie_entry.insert(0, "填一下")
cookie_entry.grid(row=0, column=1, padx=5, pady=5)

tkt.Label(root, text="User-Agent:").grid(row=1, column=0, sticky="e")
ua_entry = tk.Entry(root, width=80)
ua_entry.insert(0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
ua_entry.grid(row=1, column=1, padx=5, pady=5)

tkt.Label(root, text="课程列表：").grid(row=2, column=0, sticky="ne")
course_list_frame = CourseListFrame(root, initial_courses=[
    ("大数据管理概论", "左琼"),
    ("函数式编程原理", "郑然"),
    ("计算机图形学", "何云峰"),
    ("计算机视觉导论", "刘康"),
])
course_list_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")


# --- 居中按钮 ---
btn_frame = tk.Frame(root)
btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
run_btn = tk.Button(btn_frame, text="开始选课", command=on_run, width=16)
run_btn.pack(anchor="center")

root.mainloop()

