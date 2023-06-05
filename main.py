from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader
from tkinter import Tk, filedialog, Button, Entry, Frame, Label, StringVar, IntVar, Text, Scrollbar
import threading
import queue


# Function to select PDF file
def select_pdf_file():
    file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, "end")
        pdf_entry.insert("end", file_path)


def generate_quiz_thread(quiz_generator, num_questions_level, bloom_levels):

    # HERE PARTITION NUMBER

    # quiz_generator.generate(1)

    # Recupera i dati necessari dalla generazione del quiz
    quiz_language = quiz_generator.get_language()
    starting_text = quiz_generator.get_starting_text()

    # Quiz object declaration passing to it the language in which the quiz is written
    quiz = Quiz(quiz_language, output)

    # Schedula l'esecuzione del codice successivo alla generazione del quiz nel thread principale
    window.after(0, process_generated_quiz, quiz, starting_text, bloom_levels, num_questions_level)


# Function to generate the quiz
def generate_quiz():
    bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]
    num_questions_level = [
        remembering_var.get(),
        understanding_var.get(),
        applying_var.get(),
        analyzing_var.get(),
        evaluating_var.get()
    ]

    tot_questions = sum(num_questions_level)
    if tot_questions <= 0:
        output("Please select at least one question")
        return

    file_path = pdf_entry.get()

    if not file_path:
        output("Please select a PDF file")
        return

    openai_key = key_entry.get()  # Get the value entered in the OpenAI key input field

    # Verify if an OpenAI key has been entered
    if not openai_key:
        output("Please enter an OpenAI key")
        return

    # PDFReader object declaration passing to it the pdf from which extract the text
    pdf_reader = PDFReader(file_path)
    pdf_reader.process_pdf()

    # QuizGenerator object declaration passing to it the number of questions for each level, Bloom's levels, output function, and the OpenAI key
    quiz_generator = QuizGenerator(num_questions_level, bloom_levels, output, openai_key)

    # Create a thread for quiz generation
    generate_thread = threading.Thread(target=generate_quiz_thread,
                                       args=(quiz_generator, num_questions_level, bloom_levels,))
    generate_thread.start()

    # Disable buttons and input fields
    select_pdf_button.config(state='disabled')
    remembering_entry.config(state='disabled')
    understanding_entry.config(state='disabled')
    applying_entry.config(state='disabled')
    analyzing_entry.config(state='disabled')
    evaluating_entry.config(state='disabled')
    generate_quiz_button.config(state='disabled')
    key_entry.config(state='disabled')


# Function for thread-safe output to the text widget
def output(message=""):
    if message == "":
        formatted_message = f"{message}\n"
    else:
        formatted_message = f"**{message}**\n"

    # Add the message to the queue
    output_box_queue.put(formatted_message)


# Function to process the generated quiz in the main thread
def process_generated_quiz(quiz, starting_text, bloom_levels, num_questions_level):
    # QuizAnalyzer declaration passing to it the generated quiz and the starting text
    quiz_analyzer = QuizAnalyzer(quiz, starting_text, output)
    quiz_analyzer.calculate_weighted_standing()

    # Selection of desired number of questions for each level from the quiz (selecting the best ones)
    quiz.select_questions(num_questions_level, bloom_levels)

    output()
    output("Number of questions for each Revised Bloom's Taxonomy level.")
    quiz.print_num_questions_for_each_level(bloom_levels)

    quiz.generate_files()

    # Enable buttons and input fields
    select_pdf_button.config(state='normal')
    remembering_entry.config(state='normal')
    understanding_entry.config(state='normal')
    applying_entry.config(state='normal')
    analyzing_entry.config(state='normal')
    evaluating_entry.config(state='normal')
    generate_quiz_button.config(state='normal')
    key_entry.config(state='normal')


# Function for updating the output text box in the user interface
def update_output_box():
    while True:
        # Check if there are messages in the queue
        if not output_box_queue.empty():
            formatted_message = output_box_queue.get()

            # Update the user interface with the output message
            output_box.config(state="normal")
            output_box.insert("end", formatted_message)
            output_box.see("end")
            output_box.config(state="disabled")


# Create the main window
window = Tk()
window.title("Quiz GenAIrator")

# Frame for the PDF file selection
pdf_frame = Frame(window)
pdf_frame.pack(pady=10)

pdf_label = Label(pdf_frame, text="Select PDF")
pdf_label.pack(side="left")
pdf_entry = Entry(pdf_frame, width=50)
pdf_entry.pack(side="left")

select_pdf_button = Button(pdf_frame, text="Select PDF", command=select_pdf_file)
select_pdf_button.pack(side="left")

# Frame for the Bloom's levels selection
bloom_frame = Frame(window)
bloom_frame.pack(pady=10)

remembering_var = IntVar()
understanding_var = IntVar()
applying_var = IntVar()
analyzing_var = IntVar()
evaluating_var = IntVar()

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

generate_quiz_button = Button(window, text="Generate Quiz", command=generate_quiz)
generate_quiz_button.pack(pady=10)

result_label = StringVar()
result_label.set("")
result_display = Label(window, textvariable=result_label)
result_display.pack()

# Frame for OpenAI key input
key_frame = Frame(window)
key_frame.pack(pady=10)

key_label = Label(key_frame, text="OpenAI Key:")
key_label.pack(side="left")
key_entry = Entry(key_frame, width=50)
key_entry.pack(side="left")

output_frame = Frame(window)
output_frame.pack(pady=10)

output_label = Label(output_frame, text="Output:")
output_label.pack()

# Text widget for displaying the output
output_box = Text(output_frame, width=80, height=10)
output_box.pack(side="left", fill="y")

# Scrollbar for the output text widget
output_scrollbar = Scrollbar(output_frame)
output_scrollbar.pack(side="left", fill="y")

# Configure the output text widget to use the scrollbar
output_box.config(yscrollcommand=output_scrollbar.set)
output_scrollbar.config(command=output_box.yview)

# Create a queue for thread-safe communication of output messages
output_box_queue = queue.Queue()

# Create a thread to update the output text box in the user interface
update_output_thread = threading.Thread(target=update_output_box)
update_output_thread.daemon = True
update_output_thread.start()

# Start the main loop
window.mainloop()
