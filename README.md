# Multilingual Translation Script

This Python script translates text from an input file into a user-selected target language. It automatically detects the input language from the text and allows manual override if needed. The translation of individual lines is performed concurrently using a thread pool, with a semaphore enforcing rate limiting on translation requests. Logging and progress tracking are implemented to monitor the process.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Error Handling](#error-handling)
- [Restart Option](#restart-option)
- [Customization](#customization)
- [License](#license)

---

## Features

- **Automatic Language Detection**: Uses the `langdetect` library to analyze the first 20 lines of the input file.
- **Manual Language Selection**: Provides prompts to select or confirm source and target languages.
- **Concurrent Translation**: Utilizes Python’s `ThreadPoolExecutor` for concurrent processing of text lines.
- **Rate Limiting**: Employs a semaphore to ensure a maximum of 5 concurrent translation requests.
- **Progress Tracking**: Displays a progress bar using `tqdm` during the translation process.
- **Logging**: Records informational and error messages to a specified log file.
- **Interactive Restart**: Offers the option to restart the translation process upon completion.

---

## Prerequisites

- **Python Version**: Python 3.6 or higher.
- **Required Libraries**:
  - `deep_translator`
  - `langdetect`
  - `tqdm`
  - Other standard libraries (`os`, `sys`, `time`, `argparse`, `logging`, `threading`, `concurrent.futures`)

Install the required libraries using pip if they are not already installed.

---

## Installation

Install the necessary Python packages using pip:

```bash
pip install deep-translator langdetect tqdm
```

Ensure that your Python environment meets the version requirements.

---

## Configuration

The script includes several configurable components:

- **File Paths**:
  - **Input File**: Update the path `C:\Users\Username\translations\Input\All_English.txt` to point to the file containing the text to translate.
  - **Output Directory**: Change `C:\Users\Username\translations\Output` to the directory where the translated file will be saved.
  - **Log File**: The log file is set to `C:\Users\Username\translations\Logs\translation_log.txt`. Modify this path as needed.

- **Supported Languages**:  
  The script contains a dictionary mapping language names to their respective codes. Modify or extend this dictionary if additional languages are required.

- **Translation Settings**:
  - The translation function attempts each line translation up to 3 times.
  - The semaphore restricts translation requests to a maximum of 5 concurrent operations.

---

## Usage

1. **Run the Script**: Execute the script using Python.

   ```bash
   python translation_script.py
   ```

2. **Language Detection and Confirmation**:
   - The script reads the first 20 lines from the input file and attempts to detect the language.
   - If detection is unsuccessful or incorrect, the user is prompted to manually select the source language.

3. **Target Language Selection**:
   - A list of available target languages is displayed.
   - Enter the number corresponding to the desired target language.

4. **Translation Process**:
   - Each line of the input file is translated concurrently.
   - A progress bar shows the translation status.

5. **Output**:
   - The translated text is saved in a file named in the format `Translated_To_{TARGET_LANG}.txt` within the specified output directory.
   - Each line in the output file contains the original text and its corresponding translation, separated by a pipe symbol (`|`).

6. **Restart Option**:
   - After completion, the script asks whether to restart the translation process.

---

## How It Works

1. **Language Detection**:
   - The `detect_language` function uses `langdetect.detect` on non-empty lines to determine the most frequent language among the first 20 lines.
   - If detection fails, the user is prompted to manually specify the input language.

2. **User Prompts**:
   - The `choose_target_language` function displays a numbered list of supported languages for the user to choose from.
   - The `get_language_code` function facilitates manual selection for specifying the input language if necessary.

3. **Translation Process**:
   - The `translate_line` function uses the `GoogleTranslator` from `deep_translator` to translate a given line.
   - A semaphore ensures that only 5 translation requests are made concurrently.
   - The function includes retry logic with a delay between attempts to handle transient errors.

4. **Concurrency**:
   - The `ThreadPoolExecutor` manages concurrent translation of lines.
   - Results are collected and written in order to the output file.

5. **Logging**:
   - Logging is configured to record both informational messages and errors in the specified log file.

---

## Error Handling

- **Language Detection**: Errors during language detection are logged, and the user is prompted to enter the correct language manually.
- **Translation Errors**: Each translation attempt is retried up to 3 times. If the maximum number of retries is reached, an error message is logged and included in the output file next to the original text.
- **General Exceptions**: Any unexpected errors during file operations or translation are caught, logged, and displayed to the user.

---

## Restart Option

At the end of the translation process, the script prompts the user to decide whether to restart the translation process. This allows the script to be reused without requiring a complete restart of the program.

---

## Customization

- **Adjusting Concurrency**: Modify the `max_workers` parameter in the `ThreadPoolExecutor` to change the number of concurrent translation tasks.
- **Retry Attempts**: Change the `max_retries` parameter in the `translate_line` function to adjust the number of translation attempts per line.
- **Language Options**: Extend or modify the languages dictionary to include additional languages as needed.
- **File Paths**: Update the hardcoded file paths in the main execution block to suit your directory structure.

---

## License

Include license details here (e.g., MIT License). Specify the terms under which the script is distributed.

---

This documentation provides a factual and detailed explanation of the script's functionality, configuration, and usage.
