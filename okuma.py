from PyPDF2 import PdfReader
import re


file = "/Users/veliashvili/Desktop/yazlab1.3/metehan-belli-transkript.pdf"
reader = PdfReader(file)
# print(f"Number of Pages: {len(reader.pages)}")
# print(f"Page Number 1 Contains:\n {reader.pages[0].extract_text()}")

# text = reader.pages[0].extract_text()
total_pages = len(reader.pages)

counter = 0
codes = []
courses = []
for page_num in range(total_pages - 1):
    page = reader.pages[page_num]
    text = page.extract_text()
    for line in text.split("\n"):
        matches = re.findall(r"[A-Z]{3}\d{3}", line)
        if matches:
            counter += 1
            for match in matches:
                # print(match)
                codes.append(match)
                courses.append(line)

codes.pop(17)
courses.pop(17)
print(f"Kaç Ders Kodu Buldum: {len(codes)}")

for i in range(len(courses)):
    courses[i] = courses[i][7:]
    # print(courses[i])

counter1 = 0
grades = []
for page_num in range(total_pages - 1):
    page = reader.pages[page]
    text = page.extract_text()
    for line in text.split("\n"):
        matches = re.findall(r"AA|BA|BB|CB|CC|DC|DD|FD|FF", line)
        if matches:
            counter1 += 1
            for match in matches:
                # print(match)
                grades.append(match)
print(f"Kaç Dersin Puanını Buldum: {counter1}")

complatedArray = list(zip(codes, courses, grades))

for row in complatedArray:
    print(row)
