import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2

# -------- DB CONNECTION -------- #
try:
    conn = psycopg2.connect(
        host="localhost",
        database="lab_management",
        user="postgres",
        password="Postgres"
    )
    cur = conn.cursor()
except Exception as e:
    print("DB Error:", e)

# -------- MAIN WINDOW -------- #
root = tk.Tk()
root.title("Research Lab Manager")
root.geometry("1100x700")

from PIL import Image, ImageTk

# -------- GIF BACKGROUND -------- #
frames = []
gif = Image.open("lab.gif")

try:
    while True:
        frame = gif.copy().resize((1100, 700))
        frames.append(ImageTk.PhotoImage(frame))
        gif.seek(len(frames))
except EOFError:
    pass

bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def animate(index):
    frame = frames[index]
    bg_label.configure(image=frame)
    root.after(100, animate, (index + 1) % len(frames))

animate(0)

# -------- Animated TITLE -------- #

def animate_heading():
    text = "RESEARCH LAB MANAGER"

    canvas = tk.Canvas(root, height=90, bg="black", highlightthickness=0)
    canvas.pack(fill="x")

    x = 550
    y = 45

    current = ""

    def typing(i=0):
        nonlocal current
        if i < len(text):
            current += text[i]

            canvas.delete("all")
            canvas.create_text(
                x, y,
                text=current,
                fill="#FFD700",   # GOLD
                font=("Segoe UI Black", 32)   # 🔥 bold font
            )

            root.after(80, typing, i+1)
        else:
            glow()

    def glow():
        def blink(on=True):
            color = "#FFD700" if on else "#b89600"  # gold ↔ dark gold
            canvas.delete("all")
            canvas.create_text(
                x, y,
                text=text,
                fill=color,
                font=("Segoe UI Black", 32)
            )
            root.after(600, blink, not on)

        blink()

    typing()

animate_heading()


# -------- OUTPUT -------- #
output = tk.Text(root, height=8, bg="#0f172a", fg="white")
output.pack(side="bottom", fill="x")

def show(data):
    output.delete(1.0, tk.END)
    for row in data:
        output.insert(tk.END, str(row) + "\n")

# -------- FRAME -------- #
content = tk.Frame(root, bg="#e5e7eb")
content.place(relx=0.5, rely=0.55, anchor="center",
              width=750, height=420)
content.place_forget()

def clear():
    for w in content.winfo_children():
        w.destroy()

def section(name):
    content.place(relx=0.5, rely=0.55, anchor="center")
    clear()
    if name == "p": projects()
    elif name == "e": equipment()
    elif name == "r": reports()

# -------- MENU -------- #
menu = tk.Frame(root, bg="black")
menu.pack(fill="x")

def mbtn(t, s):
    btn = tk.Button(
        menu,
        text=t,
        command=lambda: section(s),

        bg="#FBCFE8",          # 💖 light pink box
        fg="#1E293B",          # dark text

        activebackground="#F9A8D4",
        activeforeground="#111827",

        font=("Segoe UI Semibold", 13),
        padx=18,
        pady=8,

        bd=0,
        relief="flat",
        cursor="hand2"
    )

    btn.pack(side="left", padx=12, pady=6)

    # hover effect
    def on_enter(e):
        btn.config(bg="#F9A8D4")

    def on_leave(e):
        btn.config(bg="#FBCFE8")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


mbtn("Projects & Members", "p")
mbtn("Equipment", "e")
mbtn("Reports", "r")

# -------- BUTTON -------- #
def btn(p, t, c, col):
    return tk.Button(p, text=t, command=c,
                     bg=col, fg="white", width=18)

# ================= PROJECT ================= #
def projects():
    card = tk.Frame(content, bg="white")
    card.pack(expand=True, fill="both", padx=20, pady=20)

    tk.Label(card, text="Project & Member",
             font=("Segoe UI", 14, "bold"),
             bg="white").pack(pady=10)

    form = tk.Frame(card, bg="white")
    form.pack(pady=10)

    tk.Label(form, text="Project ID", bg="white").grid(row=0, column=0, sticky="w")
    pid = tk.Entry(form); pid.grid(row=0, column=1)

    tk.Label(form, text="Project Title", bg="white").grid(row=1, column=0, sticky="w")
    title = tk.Entry(form); title.grid(row=1, column=1)

    tk.Label(form, text="Member ID", bg="white").grid(row=2, column=0, sticky="w")
    mid = tk.Entry(form); mid.grid(row=2, column=1)

    tk.Label(form, text="Member Name", bg="white").grid(row=3, column=0, sticky="w")
    name = tk.Entry(form); name.grid(row=3, column=1)

    tk.Label(form, text="Member Type", bg="white").grid(row=4, column=0, sticky="w")
    mtype = tk.Entry(form); mtype.grid(row=4, column=1)

    f = tk.Frame(card, bg="white")
    f.pack(pady=10)

    # -------- PROJECT -------- #
    def view():
        try:
            cur.execute("SELECT * FROM PROJECT")
            data = cur.fetchall()

            if data:
                show_project_popup(data)
            else:
                messagebox.showinfo("No Data", "No projects found")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_project_popup(data):
        win = tk.Toplevel()
        win.title("Project List")
        win.geometry("500x300")

        tk.Label(win, text="Projects",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

        for row in data:
            text = f"PID: {row[0]} | {row[1]} | Start: {row[2]} | End: {row[3]} | Budget: {row[4]}"
            tk.Label(win, text=text,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=20)

    def add():
        try:
            cur.execute("INSERT INTO PROJECT VALUES (%s,%s,CURRENT_DATE,NULL,1000)",
                        (pid.get(), title.get()))
            conn.commit()
            messagebox.showinfo("Success", "Project Added Successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update():
        cur.execute("UPDATE PROJECT SET TITLE=%s WHERE PID=%s",
                    (title.get(), pid.get()))
        conn.commit()
        messagebox.showinfo("Success", "Project Updated Successfully")

    def delete():
        cur.execute("DELETE FROM PROJECT WHERE PID=%s", (pid.get(),))
        conn.commit()
        messagebox.showinfo("Success", "Project Deleted Successfully")



    def show_status_popup(data):
        win = tk.Toplevel()
        win.title("Project Status")
        win.geometry("400x300")
        tk.Label(win, text="Project Status",
             font=("Segoe UI", 14, "bold")).pack(pady=10)
        for row in data:
            text = f"PID: {row[0]} | {row[1]} → {row[2]}"
            tk.Label(win, text=text,font=("Segoe UI", 10)).pack(anchor="w", padx=20)

    # -------- MEMBER -------- #
    def add_m():
        try:
            cur.execute("INSERT INTO LAB_MEMBER VALUES (%s,%s,CURRENT_DATE,%s)",
                        (mid.get(), name.get(), mtype.get()))
            conn.commit()
            messagebox.showinfo("Success", "Member Added Successfully")

            mid.delete(0, tk.END)
            name.delete(0, tk.END)
            mtype.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_m():
        cur.execute("UPDATE LAB_MEMBER SET NAME=%s WHERE MID=%s",
                    (name.get(), mid.get()))
        conn.commit()
        messagebox.showinfo("Success", "Member Updated Successfully")

    def delete_m():
        cur.execute("DELETE FROM LAB_MEMBER WHERE MID=%s", (mid.get(),))
        conn.commit()
        messagebox.showinfo("Success", "Member Deleted Successfully")
    
    def status():
        try:
            cur.execute("""
            SELECT PID, TITLE,
            CASE 
                WHEN E_DATE IS NOT NULL AND E_DATE < CURRENT_DATE THEN 'Done'
                ELSE 'Active'
            END
            FROM PROJECT
        """)
            data = cur.fetchall()
            show_status_popup(data)   # ✅ popup call
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def status_all():
        try:
            cur.execute("""
            SELECT PID, TITLE,
            CASE 
                WHEN E_DATE IS NOT NULL AND E_DATE < CURRENT_DATE THEN 'Done'
                ELSE 'Active'
            END
            FROM PROJECT
        """)
            data = cur.fetchall()
            show_status_popup(data)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def status_one():
        try:
            pid_input = simple_input("Enter Project ID")
            if not pid_input:
                messagebox.showwarning("Input Error", "Please enter Project ID")
                return

            cur.execute("""
            SELECT PID, TITLE,
            CASE 
                WHEN E_DATE IS NOT NULL AND E_DATE < CURRENT_DATE THEN 'Done'
                ELSE 'Active'
            END
            FROM PROJECT
            WHERE PID = %s
        """, (pid_input,))

            data = cur.fetchall()

            if data:
                show_status_popup(data)
            else:
                messagebox.showinfo("Not Found", "Project not found")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def grant():
        try:
            gid = simple_input("Enter GID")

            if not gid:
                messagebox.showwarning("Input Error", "Please enter GID")
                return

            cur.execute("""
            SELECT DISTINCT L.NAME
            FROM LAB_MEMBER L
            JOIN WORKS W ON L.MID=W.MID
            JOIN PROJECT P ON W.PID=P.PID
            JOIN FUNDS F ON P.PID=F.PID
            WHERE F.GID=%s
            """, (gid,))

            data = cur.fetchall()

            if data:
                show_grant_popup(data)   # ✅ popup lo show chestundi
            else:
                messagebox.showinfo("No Data", "No members found for this grant")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    def show_grant_popup(data):
        win = tk.Toplevel()
        win.title("Members by Grant")
        win.geometry("350x300")

        tk.Label(win, text="Members under this Grant",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

        for row in data:
            tk.Label(win, text=row[0],
                 font=("Segoe UI", 10)).pack(anchor="w", padx=20)


    def mentor():
        try:
            cur.execute("""
                SELECT M1.NAME, M2.NAME
                FROM LAB_MEMBER M1
                JOIN MENTORS MT ON M1.MID=MT.MENTOR
                JOIN LAB_MEMBER M2 ON M2.MID=MT.MENTEE
            """)

            data = cur.fetchall()

            if data:
                show_mentor_popup(data)   # ✅ popup
            else:
                messagebox.showinfo("No Data", "No mentorship data found")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_mentor_popup(data):
        win = tk.Toplevel()
        win.title("Mentorship")
        win.geometry("400x300")

        tk.Label(win, text="Mentor → Mentee",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

        if not data:
            tk.Label(win, text="No data found").pack()
            return

        for row in data:
            text = f"{row[0]} → {row[1]}"
            tk.Label(win, text=text,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=20)

    # BUTTONS
    btn(f,"View",view,"blue").grid(row=0,column=0)
    btn(f,"Add",add,"green").grid(row=0,column=1)
    btn(f,"Update",update,"orange").grid(row=1,column=0)
    btn(f,"Delete",delete,"red").grid(row=1,column=1)

    btn(f,"Add Member",add_m,"green").grid(row=2,column=0)
    btn(f,"Update Member",update_m,"orange").grid(row=2,column=1)
    btn(f,"Delete Member",delete_m,"red").grid(row=3,column=0)

    btn(f,"All Status", status_all, "blue").grid(row=3, column=1)
    btn(f,"One Status", status_one, "purple").grid(row=5, column=0, columnspan=2)
    btn(f,"By Grant",grant,"purple").grid(row=4,column=0)
    btn(f,"Mentorship",mentor,"gold").grid(row=4,column=1)

# ================= EQUIPMENT ================= #
def equipment():
    card = tk.Frame(content, bg="white")
    card.pack(expand=True, fill="both", padx=20, pady=20)

    tk.Label(card, text="Equipment ID", bg="white").pack()
    eid = tk.Entry(card); eid.pack()

    tk.Label(card, text="Equipment Name", bg="white").pack()
    ename = tk.Entry(card)
    ename.pack()

    tk.Label(card, text="Equipment Type", bg="white").pack()
    etype = tk.Entry(card)
    etype.pack()


    f = tk.Frame(card, bg="white")
    f.pack()


    def view():
        try:
            cur.execute("SELECT * FROM EQUIPMENT")
            data = cur.fetchall()

            if data:
                show_equipment_popup(data)
            else:
                messagebox.showinfo("No Data", "No equipment found")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_equipment_popup(data):
        win = tk.Toplevel()
        win.title("Equipment List")
        win.geometry("450x300")

        tk.Label(win, text="Equipment Details",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

        for row in data:
            text = f"ID: {row[0]} | {row[1]} | {row[2]} → {row[3]}"
            tk.Label(win, text=text,
                     font=("Segoe UI", 10)).pack(anchor="w", padx=20)
            
            

    def add():
        try:
            cur.execute(
                "INSERT INTO EQUIPMENT VALUES (%s,%s,%s,'Available')",
                (eid.get(), ename.get(), etype.get())
            )
            conn.commit()

            messagebox.showinfo("Success", "Equipment Added Successfully")

            # clear fields
            eid.delete(0, tk.END)
            ename.delete(0, tk.END)
            etype.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update():
        try:
            cur.execute("""
              UPDATE EQUIPMENT 
              SET NAME=%s, TYPE=%s 
              WHERE EID=%s
              """, (ename.get(), etype.get(), int(eid.get())))

            conn.commit()
            messagebox.showinfo("Success", "Equipment Updated")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))
    
    

    def delete():
        cur.execute("DELETE FROM EQUIPMENT WHERE EID=%s",(eid.get(),))
        conn.commit()
        messagebox.showinfo("Success", "Equipment Deleted")


    from tkinter import simpledialog, messagebox

    from datetime import date

    def add_usage():
        try:
            eid_val = int(eid.get())

            mid_val = simple_input("Enter Member ID")
            did_val = simple_input("Enter Device ID")
            purpose_val = simple_input("Enter Purpose")

            if not mid_val or not did_val:
                messagebox.showwarning("Input Error", "MID & DID required")
                return

            cur.execute("""
                     INSERT INTO USES (MID, DID, EID, S_DATE, PURPOSE)
                     VALUES (%s, %s, %s, CURRENT_DATE, %s)
                     """, (int(mid_val), int(did_val), eid_val, purpose_val))

            conn.commit()
            messagebox.showinfo("Success", "Usage Added")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

    

    def usage_delete():
        try:
            mid_val = simple_input("Enter Member ID")

            if not mid_val:
                return

            cur.execute(
                "DELETE FROM USES WHERE MID=%s AND EID=%s",
                (int(mid_val), int(eid.get()))
                 )

            conn.commit()
            messagebox.showinfo("Success", "Usage Deleted")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

    def show_status_popup(data):
        win = tk.Toplevel()
        win.title("Project Status")
        win.geometry("400x300")
        tk.Label(win, text="Project Status",
             font=("Segoe UI", 14, "bold")).pack(pady=10)
        for row in data:
            text = f"PID: {row[0]} | {row[1]} → {row[2]}"
            tk.Label(win, text=text,font=("Segoe UI", 10)).pack(anchor="w", padx=20)


    from tkinter import messagebox

    def usage():
        try:
            cur.execute("""
                        SELECT L.NAME, E.NAME, P.TITLE
                        FROM USES U
                        JOIN LAB_MEMBER L ON U.MID = L.MID
                        JOIN EQUIPMENT E ON U.EID = E.EID
                        JOIN WORKS W ON L.MID = W.MID
                        JOIN PROJECT P ON W.PID = P.PID
                        WHERE U.EID=%s
                        """, (eid.get(),))

            rows = cur.fetchall()

            if not rows:
                messagebox.showinfo("Usage", "No usage found")
                return

            result = ""
            for r in rows:
                result += f"{r[0]} using {r[1]} for {r[2]}\n"

                messagebox.showinfo("Usage", result)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

   

    def show_usage_popup(data):
        win = tk.Toplevel()
        win.title("Equipment Usage")
        win.geometry("400x300")

        tk.Label(win, text="Usage Details",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

        for row in data:
            text = f"{row[0]} → {row[1]}"
            tk.Label(win, text=text,
                     font=("Segoe UI", 10)).pack(anchor="w", padx=20)


    def status():
        try:
            cur.execute(
                "SELECT * FROM EQUIPMENT WHERE EID=%s",
                 (int(eid.get()),)
            )
            data = cur.fetchall()

            if data:
                show_equipment_popup(data)
            else:
                messagebox.showinfo("Not Found", "Equipment not found")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

    btn(f,"View",view,"blue").grid(row=0,column=0)
    btn(f,"Add",add,"green").grid(row=0,column=1)
    btn(f,"Update",update,"orange").grid(row=1,column=0)
    btn(f,"Delete",delete,"red").grid(row=1,column=1)
    btn(f,"Add Usage", add_usage, "green").grid(row=2,column=0)
    btn(f,"Delete Usage",usage_delete,"red").grid(row=2,column=1)
    btn(f,"Status",status,"gold").grid(row=3,column=0)
    btn(f,"Usage",usage,"purple").grid(row=3,column=1)

# ================= REPORTS ================= #

def show_report_popup(title, data):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("700x400")

    tk.Label(
        win,
        text=title,
        font=("Segoe UI", 20, "bold")
    ).pack(pady=20)

    if not data:
        tk.Label(win, text="No data found").pack()
        return

    # Display each row properly
    for row in data:
        tk.Label(
            win,
            text=row,
            font=("Segoe UI", 12),
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=40, pady=5)



def reports():
    card = tk.Frame(content, bg="white")
    card.pack(expand=True, fill="both", padx=20, pady=20)

    tk.Label(card, text="Enter Date (YYYY-MM-DD)", bg="white").pack()
    date = tk.Entry(card); date.pack()

    f = tk.Frame(card)
    f.pack()

    
    def top():
        cur.execute("""
            SELECT P.PID,
                P.TITLE,
                SUM(G.BUDGET) AS TOTAL_FUNDING
            FROM PROJECT P
            JOIN FUNDS F ON P.PID = F.PID
            JOIN GRANT_TABLE G ON F.GID = G.GID
            GROUP BY P.PID, P.TITLE
            ORDER BY TOTAL_FUNDING DESC
            LIMIT 5
        """)

        data = cur.fetchall()

        # Proper formatted output
        formatted = []

        for row in data:
            pid = row[0]
            title = row[1]
            funding = row[2]

            formatted.append(
                f"Project ID: {pid} | {title} | Funding: ${funding}"
            )

        show_report_popup("Top 5 Funded Projects", formatted)


    def mentor():
        try:
            cur.execute("""
                    SELECT L.NAME, COUNT(*) AS total
                    FROM MENTORS M
                    JOIN PUBLISHES P ON M.MENTEE = P.MID
                    JOIN LAB_MEMBER L ON L.MID = M.MENTOR
                    GROUP BY L.NAME
                    ORDER BY total DESC
                    LIMIT 1
                    """)

            data = cur.fetchall()

            formatted = []

            for row in data:
                name = str(row[0]).strip()
                count = row[1]

                formatted.append(
                   (name, f"{count} publications")
                    )

            show_report_popup("Top Mentor", formatted)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

        

    def pub():
        cur.execute("""
            SELECT MAJOR,
                EXTRACT(YEAR FROM DATE) AS YEAR,
                COUNT(*) AS TOTAL_PUBLICATIONS
            FROM STUDENT S
            JOIN PUBLISHES P ON S.MID = P.MID
            JOIN PUBLICATION PB ON PB.PUBID = P.PUBID
            GROUP BY MAJOR, EXTRACT(YEAR FROM DATE)
            ORDER BY YEAR DESC
        """)

        data = cur.fetchall()

        formatted = []

        for row in data:
            major = row[0]
            year = int(row[1]) # converts Decimal('2024') → 2024
            total = row[2]

            formatted.append(
                f"Major: {major} | Year: {year} | Publications: {total}"
            )

        show_report_popup("Publications by Major & Year", formatted)

    

    def before():
        try:
            if not date.get():
                messagebox.showwarning("Input Error", "Please enter date")
                return

            cur.execute("""
                        SELECT 
                                P.PID,
                                COUNT(DISTINCT F.GID) AS TOTAL_GRANTS,

                                (
                                    SELECT COUNT(*)
                                    FROM PUBLISHES PB
                                    WHERE PB.MID IN (
                                        SELECT W.MID
                                        FROM WORKS W
                                        WHERE W.PID = P.PID
                                    )
                                ) AS TOTAL_PUBLICATIONS

                            FROM PROJECT P
                            LEFT JOIN FUNDS F ON P.PID = F.PID

                            WHERE P.E_DATE < %s

                            GROUP BY P.PID
                            ORDER BY TOTAL_GRANTS DESC
                        """, (date.get(),))

            data = cur.fetchall()

            formatted = []

            for row in data:
                pid = row[0]
                grants = row[1]
                pubs = row[2]

                formatted.append(
                    f"Project ID: {pid} | Grants Received: {grants}"
                )

            show_report_popup("Projects before given date", formatted)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))


    def years():
        cur.execute("""
            SELECT EXTRACT(YEAR FROM DATE) AS YEAR,
                COUNT(*) AS TOTAL_PUBLICATIONS
            FROM PUBLICATION
            GROUP BY EXTRACT(YEAR FROM DATE)
            ORDER BY COUNT(*) DESC
            LIMIT 3
        """)

        data = cur.fetchall()

        formatted = []

        for row in data:
            year = int(row[0])
            total = row[1]

            formatted.append(
                f"Year: {year} | Total Publications: {total}"
            )

        show_report_popup("Top 3 Publication Years", formatted)

    


    btn(f,"Top",top,"blue").grid(row=0,column=0)
    btn(f,"Mentor",mentor,"green").grid(row=0,column=1)
    btn(f,"Publications",pub,"purple").grid(row=1,column=0)
    btn(f,"Before Date",before,"orange").grid(row=1,column=1)
    btn(f,"Top Years",years,"red").grid(row=2,column=0,columnspan=2)

# -------- INPUT POPUP -------- #
def simple_input(text):
    win = tk.Toplevel()
    tk.Label(win, text=text).pack()
    e = tk.Entry(win); e.pack()

    val = []
    def submit():
        val.append(e.get())
        win.destroy()

    tk.Button(win, text="OK", command=submit).pack()
    root.wait_window(win)
    return val[0]

# -------- RUN -------- #
root.mainloop()