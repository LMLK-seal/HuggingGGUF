# Hugging Face Model downloader & GGUF Converter

![LLModel Chat Demo](https://raw.githubusercontent.com/LMLK-seal/HuggingGGUF/refs/heads/main/image.png)

## Description

The Hugging Face Model downloader & GGUF Converter is a user-friendly GUI application that simplifies the process of downloading Hugging Face models and converting them to the GGUF (GPT-Generated Unified Format) format. This tool is particularly useful for researchers, developers, and AI enthusiasts who work with language models and need to convert them for use in different environments or applications.

## Features

- Download Hugging Face models directly from the application
- Convert downloaded models to GGUF format
- User-friendly PyQt5-based interface
- Customizable quantization options
- Integrated error handling and status updates

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Dependencies

Install the required packages using pip:

```bash
pip install tkinter huggingface_hub PyQt5
```

# You will also need to clone the `llama.cpp` repository and ensure that the `convert_hf_to_gguf.py` script is accessible.

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/LMLK-seal/HuggingGGUF.git
   cd huggingface-model-converter
   ```
   or

   Download the main.py code.

3. Run the application:
   ```bash
   python Main.py
   ```

4. Using the application:
   - In the "Download Hugging Face Model" section:
     - Enter the Model ID (e.g., "gpt2")
     - Choose a save directory
     - Click "Download Model"
   - In the "Convert to GGUF" section:
     - Select the `convert_hf_to_gguf.py` file from your `llama.cpp` installation
     - Choose the downloaded Hugging Face model folder
     - Select an output folder for the converted model
     - Specify the quantization model (default is "q8_0" but can work only with q8_0, f16, f32)
     - Enter the desired output file name
     - Click "Convert to GGUF"

5. The application will display the conversion output and any error messages in the result area.

## Contributing

Contributions to improve the Hugging Face Model downloader & GGUF Converter are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses the Hugging Face Hub for model downloading.
- The GGUF conversion is based on the `llama.cpp` project.

## Disclaimer

This tool is provided as-is, and users should ensure they comply with the licensing terms of the models they download and convert.
