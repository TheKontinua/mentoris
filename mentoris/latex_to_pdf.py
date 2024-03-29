import os
import subprocess
import string
import random
import shutil
from django.shortcuts import get_object_or_404
from mentapp.models import (
    Chapter,
    Chapter_Loc,
    Quiz_Rendering,
    Blob,
    Question_Attachment,
)


def generateRandomString(hashId):
    random.seed(hashId)
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


# Converts quiz object to volume string (just the number)
def quizToDataString(quiz, type):
    if type == "volume":
        strObject = str(quiz.volume)
    elif type == "chapter":
        strObject = str(quiz.chapter)
    start = strObject.find("(")
    end = strObject.find(")")
    return strObject[start + 1 : end]


def getChapterNum(volume, chapter):
    chapters = Chapter.objects.filter(volume__volume_id=volume).distinct()

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    numChapters = len(chapter_locs)
    chapterNum = -1
    for i in range(numChapters):
        if chapter_locs[i] == chapter:
            chapterNum = i
            break
    if chapterNum != -1:
        return "(" + str(chapterNum) + "/" + str(numChapters) + ")"
    else:
        print("Error: chapter not found")
        return "(X/X)"


# Converts page size to vspace
def pagesRequiredToSpacing(pages):
    centimeters = round(pages * 29.7, 2)
    return str(centimeters) + "cm"


"""
Takes in latex information and saves a pdf quiz in the latex folder

latex_question_list: list of question objects
quiz_data: quiz object
"""


def latex_to_pdf(latex_question_list, quiz_data):
    script_path = os.path.dirname(__file__)
    file_location = os.path.join(script_path, r"..\docs\latex\output_quiz.tex")
    abs_file_location = os.path.abspath(file_location)
    output_file = open(abs_file_location, "w")
    output_file.write(r"\documentclass[letterpaper,12pt,addpoints]{exam}" + "\n")
    output_file.write(r"\usepackage[utf8]{inputenc}" + "\n")
    output_file.write(r"\usepackage[english]{babel}" + "\n\n")
    output_file.write(
        r"\usepackage[top=0.5in, bottom=1in, left=0.75in, right=0.75in]{geometry}"
        + "\n"
    )
    output_file.write(r"\usepackage{amsmath,amssymb}" + "\n")
    output_file.write(r"\usepackage{mdframed}" + "\n")
    output_file.write(r"\usepackage{graphicx}" + "\n\n")
    output_file.write(r"\pagestyle{headandfoot}" + "\n")
    output_file.write(r"\firstpageheader{}{}{}" + "\n")

    rendering = Quiz_Rendering()
   
    recent_id = 0
    try:
        recent_id = Quiz_Rendering.objects.latest("date_created").rendering_id
    except Quiz_Rendering.DoesNotExist:
        pass

    rendering.rendering_id = recent_id + 1

    string_id = generateRandomString(rendering.rendering_id)
    output_file.write(
        r"\firstpagefooter{}{\fontfamily{phv}\selectfont\thepage\ of \numpages}{\fontfamily{phv}\selectfont "
        + string_id
        + r"}"
        + "\n"
    )
    volume_id_str = quizToDataString(quiz_data, "volume")
    volume_id_num = int(volume_id_str)

    chapter_obj = get_object_or_404(Chapter_Loc, chapter=quiz_data.chapter)
    chapter_name = chapter_obj.title
    chapterFraction = getChapterNum(volume_id_num, chapter_obj)

    output_file.write(
        r"\runningfooter{\fontfamily{phv}\selectfont Kontinua "
        + volume_id_str
        + " "
        + chapterFraction
        + r"}{\fontfamily{phv}\selectfont\thepage\ of \numpages}{\fontfamily{phv}\selectfont "
        + string_id
        + r"}"
        + "\n\n\n"
    )

    output_file.write(r"\begin{document}" + "\n\n")
    output_file.write(r"{\fontfamily{phv}\selectfont" + "\n")
    output_file.write(r"\noindent \parbox{0.65\textwidth}{" + "\n")
    output_file.write(r"Name: \hrulefill \\" + "\n\n")
    output_file.write(r"\vspace{0.2cm}" + "\n\n")
    output_file.write(r"Date:\ \hrulefill" + "\n\n")
    output_file.write(r"\vspace{1.0cm}" + "\n\n\n\n")

    output_file.write(
        r"\textbf{Kontinua " + volume_id_str + " " + chapterFraction + r"}" + "\n\n"
    )
    output_file.write(r"\Large \textbf{" + chapter_name + r"}" + "\n\n" + r"}" + "\n")

    output_file.write(r"\parbox{0.35\textwidth}{" + "\n\n")

    output_file.write(r"\begin{flushright}" + "\n")
    output_file.write(r"\bgroup" + "\n")
    output_file.write(r"\def\arraystretch{1.8}" + "\n")
    output_file.write(r"\begin{tabular}{c|c|c}" + "\n")
    output_file.write(r"\hline" + "\n")
    output_file.write(r"Question & Points & Score \\" + "\n")
    output_file.write(r"\hline" + "\n")
    question_number = 1
    total = 0
    for question_loc in latex_question_list:
        point = int(question_loc.question.point_value)
        total += point
        output_file.write(str(question_number) + r" & " + str(point) + r" & \\" + "\n")
        output_file.write(r"\hline" + "\n")
        question_number += 1
    output_file.write(r"\hline" + "\n")
    output_file.write(r"Total & " + str(total) + r" & \\" + "\n")
    output_file.write(r"\hline" + "\n")
    output_file.write(r"\end{tabular}" + "\n")
    output_file.write(r"\egroup" + "\n")
    output_file.write(r"\medskip" + "\n\n")

    time_required = str(quiz_data.time_required_mins)
    output_file.write(r"Duration: " + time_required + r" minutes" + "\n\n")

    calculator = quiz_data.calculator_allowed
    computer = quiz_data.computer_allowed
    internet = quiz_data.internet_allowed
    book = quiz_data.book_allowed
    if calculator:
        output_file.write(r"Calculator allowed" + "\n\n")
    if computer:
        output_file.write(r"Computer allowed" + "\n\n")
    if internet:
        output_file.write(r"Internet allowed" + "\n\n")
    if book:
        output_file.write(r"Book allowed" + "\n\n")

    output_file.write(r"\end{flushright}" + "\n")
    output_file.write(r"}" + "\n")
    output_file.write(r"} %Ends helvetica" + "\n")

    # TODO: Supports here

    output_file.write(r"\begin{enumerate}" + "\n\n")
    # output_file.write(r"\clearpage" + "\n")
    output_file.write(r"\vspace{0.25cm}" + "\n")

    for question_loc in latex_question_list:
        latex_question = question_loc.question_latex
        point = int(question_loc.question.point_value)
        plural = "" if point == 1 else "s"
        output_file.write(
            r"\item ("
            + str(point)
            + r" point"
            + plural
            + r") "
            + latex_question
            + "\n\n"
        )

        attachment_list = Question_Attachment.objects.filter(question=question_loc)
        for attachment in attachment_list:
            blob = attachment.blob_key
            temp_path = os.path.join(script_path, r"..\media", str(blob.file))
            blob_path = os.path.abspath(temp_path)

            final_path = os.path.join(script_path, blob.filename)

            shutil.copy(blob_path, final_path)

            output_file.write(r"\vspace{0.2cm}" + "\n")
            output_file.write(r"\begin{center}" + "\n")
            output_file.write(
                r"\includegraphics[width=2cm]{" + blob.filename + r"}" + "\n"
            )
            output_file.write(r"\end{center}" + "\n")

            os.remove(final_path)

        pages_required = question_loc.question.pages_required
        spacingString = pagesRequiredToSpacing(pages_required)
        output_file.write(r"\vspace{" + spacingString + r"}" + "\n\n")

    output_file.write(r"\end{enumerate}" + "\n")
    output_file.write(r"\end{document}" + "\n")

    output_file.close()

    success_flag = 0  # will be set to 2 if both generations succeed

    # Path to pdflatex command
    temp_path = os.path.join(script_path, r"..\tex-live\bin\windows\pdflatex")
    pdflatex_path = os.path.abspath(temp_path)

    # Path to LaTeX file
    temp_path = os.path.join(script_path, r"..\docs\latex\output_quiz.tex")
    latex_file_path = os.path.abspath(temp_path)

    # set current process running directory to latex folder
    temp_path = os.path.join(script_path, "..\docs\latex")
    process_path = os.path.abspath(temp_path)

    os.chdir(process_path)

    # Run pdflatex command
    process = subprocess.Popen(
        [pdflatex_path, latex_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    output, error = process.communicate()

    if error:
        print("Error occurred:")
        print(error.decode("utf-8"))
    else:
        print("PDF 1 generated successfully.")
        success_flag += 1

    # Run twice to get the page numbers to load correctly
    process = subprocess.Popen(
        [pdflatex_path, latex_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    if error:
        print("Error occurred:")
        print(error.decode("utf-8"))
    else:
        print("PDF 2 generated successfully.")
        success_flag += 1
    if success_flag == 2:
        blob = save_pdf_blob(string_id)
        rendering.quiz = quiz_data
        rendering.blob_key = blob
        rendering.save()


def save_pdf_blob(string_id):
    # rename output_quiz.pdf to new file_name
    script_path = os.path.dirname(__file__)

    temp_path = os.path.join(script_path, "..\docs\latex")
    file_temp = os.path.join(temp_path, "output_quiz.pdf")
    file_path = os.path.abspath(file_temp)

    new_name = r"..\..\media\pdfs" + "\\" + string_id + ".pdf"
    pdf_temp = os.path.join(temp_path, new_name)
    pdf_path = os.path.abspath(pdf_temp)

    if os.path.isfile(pdf_path):
        os.remove(pdf_path)

    os.rename(file_path, pdf_path)

    blob = Blob(file=pdf_path, content_type="pdf", filename=string_id + ".pdf")
    blob.save()

    return blob
