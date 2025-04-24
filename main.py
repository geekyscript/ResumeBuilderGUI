import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from textwrap import wrap

profile_photo_path = None

def upload_photo():
    global profile_photo_path
    profile_photo_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    messagebox.showinfo("Photo Selected", f"Selected: {profile_photo_path}")

def generate_pdf_resume():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    summary = text_summary.get("1.0", tk.END).strip()
    education = text_education.get("1.0", tk.END).strip()
    skills = text_skills.get("1.0", tk.END).strip()
    experience = text_experience.get("1.0", tk.END).strip()
    languages = text_languages.get("1.0", tk.END).strip()
    certificates = text_certificates.get("1.0", tk.END).strip()
    awards = text_awards.get("1.0", tk.END).strip()
    interests = text_interests.get("1.0", tk.END).strip()
    template = template_choice.get()

    if not name or not email or not phone:
        messagebox.showerror("Missing Info", "Name, Email, and Phone are required!")
        return

    file_name = f"{name}_Resume.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    if template == "Advanced":
        template_advanced(c, name, email, phone, summary, education, skills, experience, languages, certificates, awards, interests)

    c.save()
    messagebox.showinfo("Success", f"PDF resume saved as {file_name}!")

def wrap_text(text, width):
    lines = []
    for line in text.split('\n'):
        lines.extend(wrap(line.strip(), width))
    return lines

def template_advanced(c, name, email, phone, summary, education, skills, experience, languages, certificates, awards, interests):
    width, height = A4
    margin_bottom = 50  # Bottom margin
    sidebar_x = 0
    sidebar_width = width * 0.3
    content_x = sidebar_width + 10

    first_page = True

    def draw_sidebar():
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.rect(sidebar_x, 0, sidebar_width, height, fill=1)

        if profile_photo_path:
            c.drawImage(profile_photo_path, 40, height - 120, width=80, height=80, mask='auto')

        sidebar_y = height - 140
        def draw_sidebar_section(title, content):
            nonlocal sidebar_y
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.white)
            c.drawString(40, sidebar_y, f"• {title}")
            sidebar_y -= 18
            c.setFont("Helvetica", 10)
            for line in wrap_text(content, 32):
                c.drawString(50, sidebar_y, f"- {line}")
                sidebar_y -= 14
            sidebar_y -= 10

        draw_sidebar_section("SKILLS", skills)
        draw_sidebar_section("LANGUAGES", languages)
        draw_sidebar_section("CERTIFICATES", certificates)
        draw_sidebar_section("HONOR AWARDS", awards)
        draw_sidebar_section("INTERESTS", interests)

    def draw_left_bar_background():
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.rect(sidebar_x, 0, sidebar_width, height, fill=1)

    def draw_header():
        nonlocal y
        y = height - 60
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(content_x, y, name)
        y -= 20
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#7F8C8D"))
        c.drawString(content_x, y, f"Email: {email} | Phone: {phone}")
        y -= 30

    def draw_footer(page_num):
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#7F8C8D"))
        footer_text = f"Page {page_num}"
        text_width = c.stringWidth(footer_text, "Helvetica", 9)
        c.drawString((width - text_width) / 2, 20, footer_text)

    page_number = 1  # start at 1

    def check_page_break(extra_space_needed=60):
        nonlocal y, first_page, page_number
        if y < margin_bottom + extra_space_needed:
            draw_footer(page_number)
            c.showPage()
            page_number += 1
            if first_page:
                first_page = False
            draw_left_bar_background()
            draw_header()

    def draw_main_block(title, content):
        nonlocal y
        check_page_break()
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(content_x, y, f"• {title}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        for line in wrap_text(content, 75):
            check_page_break()
            c.drawString(content_x + 10, y, line)
            y -= 12
        y -= 10

    def draw_main_section(title, content):
        nonlocal y
        check_page_break()
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#2C3E50"))
        c.drawString(content_x, y, f"• {title}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        for line in content.split('\n'):
            check_page_break()
            if '|' in line:
                parts = line.split('|')
                job_title = parts[0].strip()
                company = parts[1].strip()
                location = parts[2].strip() if len(parts) > 2 else ''
                duration = parts[3].strip() if len(parts) > 3 else ''
                c.setFont("Helvetica-Bold", 10)
                c.drawString(content_x + 10, y, job_title)
                y -= 12
                c.setFont("Helvetica", 9)
                for wrapped_line in wrap(f"{company}, {location} ({duration})", 75):
                    check_page_break()
                    c.drawString(content_x + 12, y, wrapped_line)
                    y -= 12
            else:
                for wrapped_line in wrap(line.strip(), 75):
                    check_page_break()
                    c.drawString(content_x + 10, y, f"- {wrapped_line}")
                    y -= 12
        y -= 10

    # Initial setup for the first page
    y = height - 60
    draw_sidebar()
    draw_header()
    draw_main_block("PROFILE SUMMARY", summary)
    draw_main_section("WORK EXPERIENCE", experience)
    draw_main_section("EDUCATION", education)
    draw_footer(page_number)


# GUI Setup
root = tk.Tk()
root.title("Resume Builder - PDF Export")

entry_name = tk.Entry(root, width=50)
entry_email = tk.Entry(root, width=50)
entry_phone = tk.Entry(root, width=50)
text_summary = tk.Text(root, height=3, width=50, wrap=tk.WORD)
text_education = tk.Text(root, height=4, width=50, wrap=tk.WORD)
text_skills = tk.Text(root, height=4, width=50, wrap=tk.WORD)
text_experience = tk.Text(root, height=6, width=50, wrap=tk.WORD)
text_languages = tk.Text(root, height=2, width=50, wrap=tk.WORD)
text_certificates = tk.Text(root, height=2, width=50, wrap=tk.WORD)
text_awards = tk.Text(root, height=2, width=50, wrap=tk.WORD)
text_interests = tk.Text(root, height=2, width=50, wrap=tk.WORD)

labels = ["Full Name", "Email", "Phone", "Profile Summary", "Education", "Skills", "Experience", "Languages", "Certificates", "Honor Awards", "Interests"]
entries = [entry_name, entry_email, entry_phone, text_summary, text_education, text_skills, text_experience, text_languages, text_certificates, text_awards, text_interests]

for i, (label, widget) in enumerate(zip(labels, entries)):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="e")
    widget.grid(row=i, column=1, padx=10, pady=5)

tk.Button(root, text="Upload Photo", command=upload_photo).grid(row=len(labels), column=0, pady=10)

template_choice = tk.StringVar()
template_choice.set("Advanced")
tk.Label(root, text="Template").grid(row=len(labels), column=1, sticky="w")
tk.OptionMenu(root, template_choice, "Advanced").grid(row=len(labels), column=1, sticky="e")

tk.Button(root, text="Generate PDF Resume", command=generate_pdf_resume).grid(row=len(labels) + 1, column=1, pady=15)

root.mainloop()
