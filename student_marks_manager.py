# Student Marks Manager - DAA Mini Project
# Algorithms: Merge Sort, Heap Sort (Top-K), Binary Search, Linear Search
# Run: python student_marks_manager.py   (only Python + Tkinter needed)

import math
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------- ALGORITHMS ----------------------------
# A student is a tuple: (roll, name, maths, daa, python)
ROLL, NAME = (lambda s: s[0]), (lambda s: s[1])
TOT = lambda s: sum(s[2:])


def merge_sort(a, key, rev=False):            # Divide and Conquer, O(n log n)
    if len(a) <= 1:
        return a[:]
    m = len(a) // 2
    L, R = merge_sort(a[:m], key, rev), merge_sort(a[m:], key, rev)
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if (key(L[i]) >= key(R[j])) if rev else (key(L[i]) <= key(R[j])):
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    return out + L[i:] + R[j:]


def sift(a, i, n, key):                       # restore max-heap property at i
    while 2 * i + 1 < n:
        c = 2 * i + 1
        if c + 1 < n and key(a[c + 1]) > key(a[c]):
            c += 1
        if key(a[i]) >= key(a[c]):
            break
        a[i], a[c] = a[c], a[i]
        i = c


def heap_sort(a, key):                        # Transform and Conquer, O(n log n)
    a = a[:]
    for i in range(len(a) // 2 - 1, -1, -1):
        sift(a, i, len(a), key)
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift(a, 0, end, key)
    return a


def top_k(a, k, key):                         # k largest: O(n) build + k*O(log n)
    a, n, res = a[:], len(a), []
    for i in range(n // 2 - 1, -1, -1):
        sift(a, i, n, key)
    for _ in range(min(k, n)):
        a[0], a[n - 1] = a[n - 1], a[0]
        res.append(a[n - 1]); n -= 1
        sift(a, 0, n, key)
    return res


def binary_search(a, x, key):                 # a must be sorted, O(log n)
    lo, hi, steps = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2; steps += 1
        if key(a[mid]) == x:
            return mid, steps
        lo, hi = (mid + 1, hi) if key(a[mid]) < x else (lo, mid - 1)
    return -1, steps


def linear_search(a, text, key):              # O(n), partial and case-insensitive
    return [s for s in a if text.lower() in key(s).lower()]


# ------------------------------- UI --------------------------------
FONT, NAVY, BLUE, ORANGE, BG = "Segoe UI", "#0f172a", "#2563eb", "#f97316", "#f1f5f9"
SAMPLE = [(1, "Aarav Sharma", 78, 85, 92), (2, "Diya Verma", 88, 91, 84), (3, "Kabir Singh", 65, 70, 58),
          (4, "Ananya Gupta", 92, 95, 98), (5, "Rohan Mehta", 55, 62, 48), (6, "Ishita Jain", 81, 76, 89),
          (7, "Vihaan Kumar", 70, 68, 74), (8, "Meera Nair", 95, 89, 93), (9, "Arjun Patel", 60, 72, 66),
          (10, "Sneha Reddy", 84, 90, 87), (11, "Yash Malhotra", 47, 53, 61), (12, "Pooja Yadav", 73, 79, 70),
          (13, "Karan Chopra", 89, 82, 91), (14, "Nisha Bansal", 76, 88, 80), (15, "Aditya Rao", 91, 94, 90),
          (16, "Riya Kapoor", 68, 64, 77), (17, "Harsh Tiwari", 82, 75, 85), (18, "Simran Kaur", 97, 92, 96),
          (19, "Manish Saini", 58, 66, 52), (20, "Tanvi Joshi", 86, 83, 79)]


def card(parent, **kw):
    return tk.Frame(parent, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, **kw)


class App:
    def __init__(self, root):
        self.root, self.data = root, SAMPLE[:]
        root.title("Student Marks Manager"); root.geometry("1040x680"); root.configure(bg=BG)
        st = ttk.Style(); st.theme_use("clam")
        st.configure("Treeview", rowheight=27, font=(FONT, 10), background="white", fieldbackground="white", borderwidth=0)
        st.configure("Treeview.Heading", font=(FONT, 10, "bold"), background=NAVY, foreground="white", relief="flat")
        st.map("Treeview.Heading", background=[("active", BLUE)])
        st.configure("TButton", font=(FONT, 10), padding=6)
        st.configure("A.TButton", font=(FONT, 10, "bold"), background=BLUE, foreground="white")
        st.map("A.TButton", background=[("active", "#1d4ed8")])
        self.build()
        self.refresh("Ready. 20 sample students loaded.")

    def build(self):
        head = tk.Frame(self.root, bg=NAVY); head.pack(fill="x")
        tk.Label(head, text="Student Marks Manager", font=(FONT, 20, "bold"), bg=NAVY, fg="white").pack(anchor="w", padx=20, pady=(12, 0))
        tk.Label(head, text="Merge Sort  •  Heap Sort  •  Binary Search  •  Linear Search", font=(FONT, 10),
                 bg=NAVY, fg="#94a3b8").pack(anchor="w", padx=20, pady=(0, 12))

        cards = tk.Frame(self.root, bg=BG); cards.pack(fill="x", padx=16, pady=(14, 8))
        self.stat = {}
        for i, name in enumerate(("Students", "Class Average", "Topper", "Lowest Total")):
            c = card(cards); c.grid(row=0, column=i, sticky="ew", padx=5); cards.columnconfigure(i, weight=1)
            tk.Label(c, text=name.upper(), font=(FONT, 8, "bold"), bg="white", fg="#64748b").pack(anchor="w", padx=14, pady=(10, 0))
            self.stat[name] = tk.Label(c, font=(FONT, 16, "bold"), bg="white", fg=NAVY)
            self.stat[name].pack(anchor="w", padx=14, pady=(0, 10))

        body = tk.Frame(self.root, bg=BG); body.pack(fill="both", expand=True, padx=16)
        form = card(body); form.pack(side="left", fill="y", padx=(5, 10))
        tk.Label(form, text="Add Student", font=(FONT, 12, "bold"), bg="white", fg=NAVY).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 6))
        self.f = []
        for i, lab in enumerate(("Roll No.", "Name", "Maths (0-100)", "DAA (0-100)", "Python (0-100)")):
            tk.Label(form, text=lab, font=(FONT, 9), bg="white", fg="#475569").grid(row=i + 1, column=0, sticky="w", padx=(14, 6), pady=4)
            e = ttk.Entry(form, width=16); e.grid(row=i + 1, column=1, padx=(0, 14)); self.f.append(e)
        for r, (txt, cmd, sty) in enumerate((("Add Student", self.add, "A.TButton"), ("Delete Selected", self.delete, "TButton"),
                                             ("Show All", lambda: self.refresh("Showing all students."), "TButton"),
                                             ("Speed Test", self.speed_test, "TButton"))):
            ttk.Button(form, text=txt, command=cmd, style=sty).grid(row=7 + r, column=0, columnspan=2, sticky="ew", padx=14, pady=(10 if r == 0 else 3, 3))
        tk.Label(form, text="", bg="white").grid(row=11, pady=4)

        right = tk.Frame(body, bg=BG); right.pack(side="left", fill="both", expand=True)
        bar = tk.Frame(right, bg=BG); bar.pack(fill="x", pady=(0, 8))
        ttk.Button(bar, text="Rank All (Merge Sort)", style="A.TButton", command=self.rank).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Top 5 (Heap Sort)", style="A.TButton", command=self.top5).pack(side="left", padx=(0, 6))
        ttk.Button(bar, text="Sort by Roll (Merge Sort)", command=lambda: self.show(merge_sort(self.data, ROLL))).pack(side="left")

        cols = ("Rank", "Roll", "Name", "Maths", "DAA", "Python", "Total", "%")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", selectmode="extended")
        for c, w in zip(cols, (55, 55, 190, 70, 70, 70, 70, 70)):
            self.tree.heading(c, text=c); self.tree.column(c, width=w, anchor="w" if c == "Name" else "center")
        for tag, col in (("odd", "#f8fafc"), ("even", "white"), ("gold", "#fef08a"), ("silver", "#e2e8f0"), ("bronze", "#fed7aa"), ("hit", "#86efac")):
            self.tree.tag_configure(tag, background=col)
        self.tree.pack(fill="both", expand=True)

        sb = card(self.root); sb.pack(fill="x", padx=21, pady=10)
        tk.Label(sb, text="Roll No.", font=(FONT, 9), bg="white").pack(side="left", padx=(14, 4), pady=10)
        self.s_roll = ttk.Entry(sb, width=8); self.s_roll.pack(side="left")
        ttk.Button(sb, text="Binary Search", command=self.find_roll).pack(side="left", padx=(6, 30))
        tk.Label(sb, text="Name", font=(FONT, 9), bg="white").pack(side="left", padx=(0, 4))
        self.s_name = ttk.Entry(sb, width=20); self.s_name.pack(side="left")
        ttk.Button(sb, text="Linear Search", command=self.find_name).pack(side="left", padx=6)
        self.status = tk.Label(self.root, anchor="w", font=(FONT, 9), bg=NAVY, fg="#e2e8f0", padx=16, pady=6)
        self.status.pack(fill="x", side="bottom")
        self.s_roll.bind("<Return>", lambda e: self.find_roll()); self.s_name.bind("<Return>", lambda e: self.find_name())

    def show(self, rows, ranked=False, hit=None):
        self.tree.delete(*self.tree.get_children())
        for i, s in enumerate(rows):
            rank = ""
            if ranked:                                # equal totals share a rank
                rank = 1 + next(j for j, r in enumerate(rows) if TOT(r) == TOT(s))
            tag = {1: "gold", 2: "silver", 3: "bronze"}.get(rank, "odd" if i % 2 else "even")
            self.tree.insert("", "end", iid=str(s[0]), tags=("hit" if s[0] == hit else tag,),
                             values=(rank, s[0], s[1], *s[2:], TOT(s), f"{TOT(s) / 3:.1f}"))

    def refresh(self, msg):
        self.show(self.data); self.say(msg)
        n = len(self.data)
        avg = sum(map(TOT, self.data)) / (3 * n) if n else 0
        self.stat["Students"].config(text=n)
        self.stat["Class Average"].config(text=f"{avg:.1f}%" if n else "-")
        self.stat["Topper"].config(text=top_k(self.data, 1, TOT)[0][1] if n else "-")
        self.stat["Lowest Total"].config(text=min(map(TOT, self.data)) if n else "-")

    def say(self, text):
        self.status.config(text=text)

    def timed(self, fn, *a):
        t = time.perf_counter(); r = fn(*a)
        return r, (time.perf_counter() - t) * 1000

    def add(self):
        try:
            roll, name, marks = int(self.f[0].get()), self.f[1].get().strip(), [int(e.get()) for e in self.f[2:]]
            if not (roll > 0 and name and all(0 <= m <= 100 for m in marks)):
                raise ValueError
        except ValueError:
            return messagebox.showerror("Invalid input", "Roll must be a positive number, name is required and marks must be 0-100.")
        if any(s[0] == roll for s in self.data):
            return messagebox.showerror("Duplicate", f"Roll number {roll} already exists.")
        self.data.append((roll, name, *marks))
        for e in self.f:
            e.delete(0, "end")
        self.refresh(f"Added {name} (roll {roll}).")

    def delete(self):
        sel = {int(i) for i in self.tree.selection()}
        if not sel:
            return messagebox.showinfo("Delete", "Select one or more rows first.")
        self.data = [s for s in self.data if s[0] not in sel]
        self.refresh(f"Deleted {len(sel)} record(s).")

    def rank(self):
        r, ms = self.timed(merge_sort, self.data, TOT, True)
        self.show(r, ranked=True)
        self.say(f"Merge Sort ranked {len(r)} students in {ms:.3f} ms   |   O(n log n)")

    def top5(self):
        r, ms = self.timed(top_k, self.data, 5, TOT)
        self.show(r, ranked=True)
        self.say(f"Heap Sort found the top {len(r)} in {ms:.3f} ms   |   O(n + k log n)")

    def find_roll(self):
        try:
            x = int(self.s_roll.get())
        except ValueError:
            return messagebox.showerror("Invalid roll", "Enter a whole-number roll.")
        a = merge_sort(self.data, ROLL)              # binary search needs sorted data
        i, steps = binary_search(a, x, ROLL)
        self.show(a, hit=x if i >= 0 else None)
        if i < 0:
            return self.say(f"Roll {x} not found after {steps} step(s).")
        self.tree.see(str(x))
        self.say(f"Binary Search found {a[i][1]} in {steps} step(s); "
                 f"linear search may need up to {len(a)}.")

    def find_name(self):
        q = self.s_name.get().strip()
        r = linear_search(self.data, q, NAME) if q else []
        self.show(r)
        self.say(f"Linear Search checked {len(self.data)} records and found {len(r)} "
                 f"match(es) for '{q}'   |   O(n)")

    def speed_test(self):
        win = tk.Toplevel(self.root); win.title("Speed Test: Merge Sort vs Heap Sort"); win.geometry("660x440")
        cv = tk.Canvas(win, bg="white", highlightthickness=0); cv.pack(fill="both", expand=True)
        rows = []
        for n in (1000, 2500, 5000, 10000, 20000):
            d = [(i, "", *(random.randint(0, 100) for _ in range(3))) for i in range(n)]
            rows.append((n, self.timed(merge_sort, d, TOT)[1], self.timed(heap_sort, d, TOT)[1]))
        self.rows = rows
        top = max(max(r[1], r[2]) for r in rows) * 1.2
        cv.create_text(330, 24, text="Sorting time in ms (lower is better)", font=(FONT, 12, "bold"), fill=NAVY)
        for i, (n, a, b) in enumerate(rows):
            x = 60 + i * 115
            for dx, v, col in ((0, a, BLUE), (42, b, ORANGE)):
                h = 280 * v / top
                cv.create_rectangle(x + dx, 360 - h, x + dx + 38, 360, fill=col, outline="")
                cv.create_text(x + dx + 19, 350 - h, text=f"{v:.1f}", font=(FONT, 8))
            cv.create_text(x + 40, 378, text=f"n = {n}", font=(FONT, 9))
        cv.create_line(40, 360, 640, 360, fill="#94a3b8")
        cv.create_rectangle(420, 40, 432, 52, fill=BLUE, outline=""); cv.create_text(438, 46, text="Merge Sort", anchor="w", font=(FONT, 9))
        cv.create_rectangle(520, 40, 532, 52, fill=ORANGE, outline=""); cv.create_text(538, 46, text="Heap Sort", anchor="w", font=(FONT, 9))
        n = rows[-1][0]
        cv.create_text(330, 412, font=(FONT, 9), fill="#475569",
                       text=f"Searching {n} records: Linear Search up to {n} checks, Binary Search only {math.ceil(math.log2(n))} steps")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
