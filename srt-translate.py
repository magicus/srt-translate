# Copyright 2024 Magnus Ihse Bursie <mag@icus.se>
#
# Licensed under the MIT License, see LICENSE for details

# This script uses the OpenAI API to translate the content of an SRT file from
# English to Swedish. The script reads the content of the input file, sends it
# to the OpenAI API, and saves the translated content to the output file.

import time
import os
import sys
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

def translate_srt(input_file_path, output_file_path, category="convert"):
    # The hard-coded prompt
    prompt = """
You are an excellent translator of TV subtitles. You will translate the following
subtitle file from English to Swedish, using the highest possible standards of quality.
The file is in SRT format. You will keep all time codes intact. You will answer
as a complete SRT file, keeping the same format as the input file. Keep line
breaks at the same places. Make sure you match up translated lines correctly.

As a professional translator, you will correctly identify all English idioms in
the input text, and replace them with corresponding Swedish idioms, instead of
translating them word by word.  For instance, translate "Screw traditions!"
with "Åt helvete med traditioner". If no corresponding Swedish idiom exists,
you will try to capture the meaning of the phrase in your translation.

Remember that the SRT format can capture multi-line sentences, even if they are
interrupted by time codes. So make sure that if several consecutive lines makes
sense as a whole sentence in English, the corresponding lines must make sense
as a whole sentence in Swedish, too. Often, but not always, the punctuation will
help you determine this.

Every sentence should be translated as accurately as possible. Try to understand
each sentence in the context of the dialogue surrounding it, and make a sane and
logical translation. If a sentence is ambiguous, provide the most likely
translation based on the context.

Good luck!
"""

    print(f"Translating {input_file_path}")

    # Read the content of the input file
    with open(input_file_path, 'r') as input_file:
        user_message = input_file.read()

    # Send the task to the OpenAI API
    completion = client.chat.completions.create(
        messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
        ],
        model="gpt-4o-2024-08-06"
    )

    # Extract the response text
    response_text = completion.choices[0].message.content

    # Save the response to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(response_text)

    print(f"Response saved to {output_file_path}")


# Main

# Get input file name from command line arguments
input_file = sys.argv[1]

output_file = input_file + "-out"

translate_srt(input_file, output_file)
