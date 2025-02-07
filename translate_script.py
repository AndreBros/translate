import os
import sys
import time
import argparse
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
import threading
from langdetect import detect, LangDetectException
from requests.exceptions import Timeout, RequestException

# Setup logging to log into a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=r'C:\Users\AndréBroskij\translations\Logs\translation_log.txt',  # Log file path
    filemode='a'  # Append logs to the file
)
# Semaphore for rate limiting
semaphore = threading.Semaphore(5)

languages = {
    'Bulgarian': 'bg', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl',
    'English': 'en', 'Finnish': 'fi', 'French': 'fr', 'German': 'de', 'Greek': 'el',
    'Hungarian': 'hu', 'Italian': 'it', 'Polish': 'pl', 'Portuguese': 'pt',
    'Romanian': 'ro', 'Slovak': 'sk', 'Spanish': 'es', 'Swedish': 'sv',
    'Albanian': 'sq', 'Armenian': 'hy', 'Azerbaijani': 'az', 'Belarusian': 'be',
    'Bosnian': 'bs', 'Catalan': 'ca', 'Estonian': 'et', 'Faroese': 'fo',
    'Georgian': 'ka', 'Icelandic': 'is', 'Irish': 'ga', 'Kazakh': 'kk',
    'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk',
    'Maltese': 'mt', 'Moldovan': 'mo', 'Montenegrin': 'cnr', 'Norwegian': 'no',
    'Serbian': 'sr', 'Slovenian': 'sl', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Welsh': 'cy'
}

def choose_target_language():
    print("Please choose a target language from the following options:")
    for index, (language, code) in enumerate(languages.items(), start=1):
        print(f"{index}. {language} ({code})")

    while True:
        choice = input("Enter the number corresponding to your desired target language: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(languages):
                selected_language = list(languages.values())[choice - 1]
                return selected_language
        print("Invalid choice. Please try again.")

def detect_language(lines):
    try:
        detected_languages = [detect(line.strip()) for line in lines if line.strip()]
        detected_lang = max(set(detected_languages), key=detected_languages.count)
        return detected_lang
    except LangDetectException as e:
        logging.error(f"Error detecting language: {e}")
        return None

def get_language_code(language_dict, prompt):
    print(prompt)
    for index, (language, code) in enumerate(language_dict.items(), start=1):
        print(f"{index}. {language} ({code})")

    while True:
        choice = input("Enter the number corresponding to your desired language: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(language_dict):
                return list(language_dict.values())[choice - 1]
        print("Invalid choice. Please try again.")

def translate_line(line, source_lang, target_lang, index, max_retries=3):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    for attempt in range(max_retries):
        with semaphore:
            try:
                translated_line = translator.translate(line.strip())
                return index, f"{line.strip()} | {translated_line}\n"
            except Exception as e:
                logging.error(f"Error translating line: {line.strip()}. Attempt {attempt + 1} of {max_retries}. Error: {e}")
                time.sleep(1)  # Wait a bit before retrying
                if attempt == max_retries - 1:
                    return index, f"{line.strip()} | TRANSLATION_ERROR: {e}\n"
        time.sleep(1)  # Ensure only 5 requests per second

def main(input_file_path, output_directory):
    try:
        # Read all lines from the input file
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()
        
        # Detect language from first 20 lines
        detected_language = detect_language(lines[:20])
        if detected_language is None:
            print("Could not detect the language. Please select the input language manually.")
            input_language = get_language_code(languages, "Select the input language:")
        else:
            detected_language_name = [k for k, v in languages.items() if v == detected_language][0]
            print(f"Detected input language: {detected_language_name} ({detected_language})")

            # Prompt the user to confirm the detected language
            user_confirmation = input("Is the detected language correct? (y/n): ").strip().lower()
            if user_confirmation != 'y':
                print("Please specify the correct source language code (e.g., 'en' for English):")
                input_language = input().strip()
            else:
                input_language = detected_language

        # Ask the user to choose a target language from the list
        target_lang = choose_target_language()
        print(f"Target language selected: {target_lang}")
        
        # Define output file path
        output_file_path = fr'{output_directory}\Translated_To_{target_lang.upper()}.txt'
        print(f"Output will be saved to: {output_file_path}")
        
        # Translation process
        total_lines = len(lines)
        with ThreadPoolExecutor(max_workers=5) as executor:  # Max workers is set to 5 to control the rate limit
            future_to_line = {executor.submit(translate_line, line, input_language, target_lang, index): line for index, line in enumerate(lines)}

            results = [None] * total_lines
            for future in tqdm(as_completed(future_to_line), total=total_lines, desc="Translating"):
                try:
                    index, result = future.result()
                    results[index] = result
                except Exception as e:
                    logging.error(f"Error in future result: {e}")

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for result in results:
                    output_file.write(result)
                    output_file.flush()  # Flush the output to the file

        logging.info(f"Translation completed and saved to {output_file_path}")
        print("Translation completed and saved to", output_file_path)

        # Ask the user whether to restart or exit
        restart = input("Would you like to restart the translation process? (y/n): ").strip().lower()
        if restart == 'y':
            logging.info("Restarting the translation process...")
            main(input_file_path, output_directory)
        else:
            logging.info("Translation process finished.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file_path = r'C:\Users\AndréBroskij\translations\Input\All_English.txt'
    output_directory = r'C:\Users\AndréBroskij\translations\Output'
    main(input_file_path, output_directory)
