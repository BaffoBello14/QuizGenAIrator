from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader
from tkinter import Tk, filedialog, Button, Entry, Frame, Label, StringVar, IntVar, Text, Scrollbar


# Funzione per l'output nel widget di testo
def output(message=""):
    formatted_message = f"{message}\n"
    output_box.config(state="normal")
    output_box.insert("end", formatted_message)
    output_box.see("end")
    output_box.config(state="disabled")


# Funzione per selezionare il file PDF
def select_pdf_file():
    file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, "end")
        pdf_entry.insert("end", file_path)


# Funzione per generare il quiz
def generate_quiz():
    bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]
    num_questions_level = [
        remembering_var.get(),
        understanding_var.get(),
        applying_var.get(),
        analyzing_var.get(),
        evaluating_var.get()
    ]

    tot_questions = 0
    for value in num_questions_level:
        tot_questions += value

    if tot_questions <= 0:
        return

    file_path = pdf_entry.get()

    if not file_path:
        return

    # PDFReader object declaration passing to it the pdf from which extract the text
    pdf_reader = PDFReader(file_path)
    pdf_reader.process_pdf()

    # QuizGenerator object declaration passing to it the number of questions for each level and the Bloom's levels
    quiz_generator = QuizGenerator(num_questions_level, bloom_levels, output)
    # quiz_generator.generate()

    # Quiz object declaration passing to it the language in which the quiz is written
    quiz = Quiz(quiz_generator.get_language(), output)

    # QuizAnalyzer declaration passing to it the generated quiz and the starting text
    quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text(), output)
    quiz_analyzer.calculate_weighted_standing()

    output("Number of available questions for each Revised Bloom's Taxonomy level, before the selection.")
    quiz.print_num_questions_for_each_level(bloom_levels)

    # selection of desired number of questions for each level from the quiz (selecting the best ones)
    quiz.select_questions(num_questions_level, bloom_levels)

    output("Number of questions for each Revised Bloom's Taxonomy level for the final quiz.")
    quiz.print_num_questions_for_each_level(bloom_levels)

    quiz.generate_files()


# Creazione della finestra principale
window = Tk()
window.title("Quiz Generation")

# Frame per il percorso del file PDF
pdf_frame = Frame(window)
pdf_frame.pack(pady=10)

# Casella di testo per il percorso del file PDF
pdf_label = Label(pdf_frame, text="Select PDF")
pdf_label.pack(side="left")
pdf_entry = Entry(pdf_frame, width=50)
pdf_entry.pack(side="left")

# Pulsante per selezionare il file PDF
select_pdf_button = Button(pdf_frame, text="Select PDF", command=select_pdf_file)
select_pdf_button.pack(side="left")

# Frame per la selezione dei livelli di Bloom
bloom_frame = Frame(window)
bloom_frame.pack(pady=10)

# Variabili per i livelli di Bloom
remembering_var = IntVar()
understanding_var = IntVar()
applying_var = IntVar()
analyzing_var = IntVar()
evaluating_var = IntVar()

# Etichette per i livelli di Bloom
remembering_label = Label(bloom_frame, text="Remembering:")
remembering_label.grid(row=0, column=0, padx=10)
understanding_label = Label(bloom_frame, text="Understanding:")
understanding_label.grid(row=1, column=0, padx=10)
applying_label = Label(bloom_frame, text="Applying:")
applying_label.grid(row=2, column=0, padx=10)
analyzing_label = Label(bloom_frame, text="Analyzing:")
analyzing_label.grid(row=3, column=0, padx=10)
evaluating_label = Label(bloom_frame, text="Evaluating:")
evaluating_label.grid(row=4, column=0, padx=10)

# Caselle di testo per i livelli di Bloom
remembering_entry = Entry(bloom_frame, width=5, textvariable=remembering_var)
remembering_entry.grid(row=0, column=1, padx=10)
understanding_entry = Entry(bloom_frame, width=5, textvariable=understanding_var)
understanding_entry.grid(row=1, column=1, padx=10)
applying_entry = Entry(bloom_frame, width=5, textvariable=applying_var)
applying_entry.grid(row=2, column=1, padx=10)
analyzing_entry = Entry(bloom_frame, width=5, textvariable=analyzing_var)
analyzing_entry.grid(row=3, column=1, padx=10)
evaluating_entry = Entry(bloom_frame, width=5, textvariable=evaluating_var)
evaluating_entry.grid(row=4, column=1, padx=10)

# Pulsante per generare il quiz
generate_quiz_button = Button(window, text="Generate Quiz", command=generate_quiz)
generate_quiz_button.pack(pady=10)

# Etichetta per il risultato del generatore del quiz
result_label = StringVar()
result_label.set("")
result_display = Label(window, textvariable=result_label)
result_display.pack()

# Box di output
output_frame = Frame(window)
output_frame.pack(pady=10)

output_label = Label(output_frame, text="Output:")
output_label.pack()

output_box = Text(output_frame, width=80, height=10)
output_box.pack(side="left", fill="both", expand=True)

output_scrollbar = Scrollbar(output_frame, command=output_box.yview)
output_scrollbar.pack(side="right", fill="y")

output_box.config(yscrollcommand=output_scrollbar.set)
output_box.config(state="disabled")

# Esecuzione della finestra principale
window.mainloop()
