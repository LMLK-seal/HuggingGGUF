import tkinter as tk
from tkinter import filedialog, messagebox
from huggingface_hub import snapshot_download
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, 
                             QMessageBox, QTextEdit)
from PyQt5.QtGui import QIcon
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hugging Face Model Converter")
        #self.setWindowIcon(QIcon('your_icon_file.ico'))  # Replace with your icon file
        self.setGeometry(100, 100, 700, 500)  # Adjust window size as needed

        # --- Widgets for Model Downloading ---
        self.download_section_label = QLabel("1. Download Hugging Face Model:")
        self.model_id_label = QLabel("Model ID:")
        self.model_id_entry = QLineEdit()
        self.save_dir_label = QLabel("Save Directory:")
        self.save_dir_entry = QLineEdit()
        self.browse_save_dir_button = QPushButton("Browse")
        self.download_button = QPushButton("Download Model")
        self.download_status_label = QLabel("")

        # --- Widgets for GGUF Conversion ---
        self.convert_section_label = QLabel("2. Convert to GGUF:")
        self.llama_cpp_label = QLabel("Load convert_hf_to_gguf.py File from llama.cpp:")
        self.llama_cpp_entry = QLineEdit()
        self.llama_cpp_button = QPushButton("Browse")
        self.hf_model_label = QLabel("Hugging Face Model Folder (Downloaded):")
        self.hf_model_entry = QLineEdit()
        self.hf_model_button = QPushButton("Browse")
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_entry = QLineEdit()
        self.output_folder_button = QPushButton("Browse")
        self.quant_model_label = QLabel("Quantization Model:")
        self.quant_model_entry = QLineEdit(text="q8_0")  # Default value
        self.output_file_label = QLabel("Output File Name:")
        self.output_file_entry = QLineEdit(text="output_file.gguf")  # Default value
        self.convert_button = QPushButton("Convert to GGUF")
        
        # Using QTextEdit for better display of multi-line output
        self.result_label = QTextEdit()
        self.result_label.setReadOnly(True)  # Make it read-only for output

        # --- Layout ---
        main_layout = QVBoxLayout()

        # Download Section Layout
        download_layout = QVBoxLayout()
        download_layout.addWidget(self.download_section_label)

        model_id_hbox = QHBoxLayout()
        model_id_hbox.addWidget(self.model_id_label)
        model_id_hbox.addWidget(self.model_id_entry)
        download_layout.addLayout(model_id_hbox)

        save_dir_hbox = QHBoxLayout()
        save_dir_hbox.addWidget(self.save_dir_label)
        save_dir_hbox.addWidget(self.save_dir_entry)
        save_dir_hbox.addWidget(self.browse_save_dir_button)
        download_layout.addLayout(save_dir_hbox)

        download_layout.addWidget(self.download_button)
        download_layout.addWidget(self.download_status_label)

        # Convert Section Layout
        convert_layout = QVBoxLayout()
        convert_layout.addWidget(self.convert_section_label)

        llama_cpp_hbox = QHBoxLayout()
        llama_cpp_hbox.addWidget(self.llama_cpp_entry)
        llama_cpp_hbox.addWidget(self.llama_cpp_button)
        convert_layout.addWidget(self.llama_cpp_label)
        convert_layout.addLayout(llama_cpp_hbox)

        hf_model_hbox = QHBoxLayout()
        hf_model_hbox.addWidget(self.hf_model_entry)
        hf_model_hbox.addWidget(self.hf_model_button)
        convert_layout.addWidget(self.hf_model_label)
        convert_layout.addLayout(hf_model_hbox)

        output_folder_hbox = QHBoxLayout()
        output_folder_hbox.addWidget(self.output_folder_entry)
        output_folder_hbox.addWidget(self.output_folder_button)
        convert_layout.addWidget(self.output_folder_label)
        convert_layout.addLayout(output_folder_hbox)

        convert_layout.addWidget(self.quant_model_label)
        convert_layout.addWidget(self.quant_model_entry)
        convert_layout.addWidget(self.output_file_label)
        convert_layout.addWidget(self.output_file_entry)
        convert_layout.addWidget(self.convert_button)

        # --- Add Section Layouts to Main Layout ---
        main_layout.addLayout(download_layout)
        main_layout.addLayout(convert_layout)
        main_layout.addWidget(self.result_label) # Add result display

        # --- Central Widget ---
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Connect Signals to Slots ---
        self.browse_save_dir_button.clicked.connect(self.browse_save_dir)
        self.download_button.clicked.connect(self.download_model)

        self.llama_cpp_button.clicked.connect(self.browse_llama_cpp_file)
        self.hf_model_button.clicked.connect(self.browse_hf_model_folder)
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        self.convert_button.clicked.connect(self.convert_hf_to_gguf)

    # --- Functions for Model Downloading ---
    def browse_save_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        self.save_dir_entry.setText(directory)

    def download_model(self):
        model_id = self.model_id_entry.text()
        save_dir = self.save_dir_entry.text()

        if not model_id or not save_dir:
            QMessageBox.warning(self, "Input Error", "Please enter Model ID and select Save Directory.")
            return

        try:
            snapshot_download(repo_id=model_id, local_dir=save_dir)
            self.download_status_label.setText(f"Model '{model_id}' downloaded to '{save_dir}'")
        except Exception as e:
            error_message = f"Download failed:\n{str(e)}"
            self.download_status_label.setText(error_message)
            QMessageBox.critical(self, "Error", error_message)

    # --- Functions for GGUF Conversion ---
    def browse_llama_cpp_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select llama.cpp File", "", "Python Files (*.py)")
        self.llama_cpp_entry.setText(file_path)

    def browse_hf_model_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Hugging Face Model Folder")
        self.hf_model_entry.setText(folder_path)

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        self.output_folder_entry.setText(folder_path)

    def convert_hf_to_gguf(self):
        llama_cpp_file_path = self.llama_cpp_entry.text()
        hf_model_path = self.hf_model_entry.text()
        output_folder_path = self.output_folder_entry.text()
        quant_model = self.quant_model_entry.text()
        output_file_name = self.output_file_entry.text()

        if not all([llama_cpp_file_path, hf_model_path, output_folder_path]):
            QMessageBox.warning(self, "Input Error", "Please select all required files and folders.")
            return

        command = (
            f"python {llama_cpp_file_path} "
            f"{hf_model_path} --outfile {os.path.join(output_folder_path, output_file_name)} --outtype {quant_model}"
        )

        try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Display stdout and stderr in the QTextEdit
            self.result_label.setPlainText(f"Conversion Output:\n{process.stdout}\n\nError Output (if any):\n{process.stderr}")
        except Exception as e:
            error_message = f"Conversion failed:\n{str(e)}"
            self.result_label.setPlainText(error_message)
            QMessageBox.critical(self, "Error", error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
