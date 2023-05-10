# Text2Soundscape
# Composer and Sound Designer Assistant

This repository contains an implementation of a Composer and Sound Designer Assistant, powered by OpenAI's ChatGPT. The tool helps users create or edit music and soundscapes based on their given prompts. It interacts with OpenAI's GPT-3.5-turbo model to provide meaningful, detailed, and creative suggestions according to user's requirements for melodies or sound designs.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [How It Works](#how-it-works)
4. [Usage](#usage)
5. [Examples](#examples)
6. [License](#license)

## Prerequisites

- Python 3.x
- OpenAI API key with access to the GPT-3.5-turbo endpoint

## Installation

1. Clone the repository:

```bash
git clone https://github.com/username/composer-and-sound-designer-assistant.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to the script by replacing `<YOUR_API_KEY>`:

```python
openai.api_key = "<YOUR_API_KEY>"
```

4. Run the script:

```bash
python main.py
```

## How It Works

The Composer and Sound Designer Assistant consists of three main components:

1. Component 1: Determine if the user's prompt should create or modify a new sound, or provide further instructions for an existing sound.
2. Component 2: Enhance the user's prompt with additional sound-describing adjectives.
3. Component 3: Identify the best parameters and values to match the user's descriptions (for both melodies and sound design).

The application takes input from the user, processes the prompt, and then interacts with the GPT-3.5-turbo model to provide the desired output.

## Usage

1. Run the script:

```bash
python main.py
```

2. Input your sound or melody description when prompted:

```plaintext
Describe the music or soundscape you want to hear:
```

3. The system will analyze the input, interact with the GPT-3.5-turbo, and provide the relevant output, including:

    - Decision Add Edit
    - Prompt Enhancer Main
    - Prompt Enhancer Melody (if "add" decision selected)
    - Melody
    - Prompt Enhancer Sound Design (if "add" decision selected)
    - ADSR envelope parameter values

## Examples

Example input:

```plaintext
Describe the music or soundscape you want to hear:

Intense, dark battle music
```

Example output:

```plaintext
Decision Add Edit: add

Prompt Enhancer Main: Intense, dark battle music with heavy percussive elements, aggressive brass stabs, and dissonant, suspenseful string ostinatos that create tension and chaos.

Prompt Enhancer Melody: The intense, dark battle melody would likely utilize a combination of rapid, low-register ostinatos and soaring, aggressive melodic lines in the higher registers. The use of brass, orchestral strings, and powerful percussion would create a dramatic, chaotic musical backdrop for the imaginary battle.

Melody: [(52, 60, 250), (54, 60, 250), (56, 60, 250), (58, 100, 500), (56, 60, 250), (54, 60, 250), (52, 60, 250), (50, 60, 250), (49, 80, 750)]

Prompt Enhancer Sound Design: Intense, dark battle music with heavy percussive elements, aggressive brass stabs, and dissonant, suspenseful string ostinatos coupled with a booming, distorted bass that creates a chaotic, tension-filled soundscape.

ADSR envelope parameter values:

  "Attack": 10,
  "Decay": 200,
  "Sustain": 0.5,
  "Release": 500
```

## License

This project is licensed under the [MIT License](LICENSE).
```
