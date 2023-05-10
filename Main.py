import openai 
import os
import json
import tiktoken
#import spatial.distance.cosine
from scipy import spatial
import SimpleUDPClient from python-osc

# Set your secret API key
openai.api_key = "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"

## OSC test
ip = "127.0.0.1"
port = 5005

client = SimpleUDPClient(ip, port)  # Create client
# for this you need to install python-osc
# via pip install python-osc
# then import SimpleUDPClient from python-osc

client.send_message("Velocity", 123)   # Send float message
# Send message with int, float and string
velocities = [1, 2., 127, 80, 90]
pitches = [60, 62, 64, 65, 67, 69, 71, 72]
durations = [1, 1, 1, 1, 1, 1, 1, 1]
client.send_message("Velocities", velocities)
client.send_message("/some/address", ["adDingens"])
client.send_message("/some/bonk", ["bonkDingen"])



# functions
def cosine_similarity_embeddings(embedding1, embedding2):
    return 1 - spatial.distance.cosine(embedding1, embedding2)

def get_embedding_string_jsondump(text, directory=str, filename=str, model="text-embedding-ada-002"):
    embedding = openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
    with open(f"{directory}{filename}.json", "w") as f:
        # dump the embedding and the text to a json file
        json.dump({"text": text, "embedding": embedding}, f)
    return embedding

def get_embedding_string(text, model="text-embedding-ada-002"):
    embedding = openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
    
    return embedding

def truncate_messages(messages, encoder, max_tokens):
    truncated_messages = []
    current_tokens = 0
    for message in messages:
        content = message["content"]
        content_tokens = encoder.encode(content)
        current_tokens += len(content_tokens)

        if current_tokens > max_tokens:
            excess_tokens = current_tokens - max_tokens
            truncated_content = encoder.decode(content_tokens[:-excess_tokens])
            message["content"] = truncated_content
            current_tokens = max_tokens

        truncated_messages.append(message)

        if current_tokens == max_tokens:
            break

    return truncated_messages

def truncate_single_message(message, encoder, max_tokens):
    message_tokens = encoder.encode(message)

    if len(message_tokens) > max_tokens:
        truncated_message = encoder.decode(message_tokens[:max_tokens])
        return truncated_message
    else:
        return message

def send_message_to_chatgpt(message_input, role=None, model="gpt-3.5-turbo", temperature=0, include_beginning=True, is_list=False):

    encoder = tiktoken.encoding_for_model(model)
    max_tokens = 4050 if model == "gpt-3.5-turbo" else 8150 if model == "gpt-4" else None

    if not is_list:
        cleaned_message = message_input.replace("'", "").replace('"', '').replace("’", "")
        truncated_message = truncate_single_message(cleaned_message, encoder, max_tokens)
        message_input = [{"role": role, "content": truncated_message}]
    else:
        message_input = truncate_messages(message_input, encoder, max_tokens)

    final_message = message_intro + message_input if include_beginning else message_input

    response = openai.ChatCompletion.create(
        model=model,
        messages=final_message,
        temperature=temperature,
    )

    response_content = response.choices[0].message.content
    return response_content

def get_melody_sounddesign_deicision(prompt):
    message_melody_sounddesign_decision = [
    {"role": "user", "content": "I am going to provide you with the prompt of a user. You need to decide whether the user wants to create or edit a melody or a sound design. If the user does not specify either option, you must assume that the user wants both. Your response will be 'melody', 'sound' or 'both'. You should only reply with one of these three words, and nothing else. Repeat my instructions so that I can see that you have understood my task. Then wait for the first prompt."},
    {"role": "assistant", "content": "You will provide me with a prompt from a user. I need to determine whether the user wants to create or edit a melody or a sound design. If the user doesn't specify either option, I must assume they want both. My response will be 'melody', 'sound', or 'both', using only one of these words. Now, I am waiting for the first prompt."},
    {"role": "system", "content": "Example 1},"},
    {"role": "user", "content": "Example "},
    {"role": "system", "content": "Great! Let's create a soundscape!"},
    ]

def get_synth_parameters_and_values(prompt):

    synth_parameters = ["[waveform]: sine, tri, sqr, saw, noise", "[Oscillator_Detune]: -100 - 100 (cents)", "[attack]: 10 - 3000 (ms)", "[decay]: 1 - 3000(ms)", "[sustain]: 0-1", "[release]: 10 - 3000(ms)", "[delay]: 0 - 1 (bool)", "[delay_time]: 100 - 2000(ms)", "[delay_feedback]: 0 - 1", "[delay_mix]: 0 - 1", "[reverb]: 0 - 1(bool)", "[reverb_room]: 0 - 1", "[reverb_damp]: 0 - 1", "[reverb_length]: 0.0 - 10.0(s)", "[reverb_mix]: 0 - 1", "[reverb_decay_time]: 0 - 4000 (ms) ","[filter]: 0 - 1", "[filter_type]: lowpass, highpass, bandpass, lowshelf, highshelf, peaking, notch, allpass", "[filter_frequency]: 20 - 20000", "[filter_resonance]: 0 - 1"]
    message_synth_parameters = [
    {"role": "system", "content": f"Given parameters: {synth_parameters}. \n\n Instruction: Given the provided set of parameters decide which ones you want to use and which ones you want to ignore and provide a value for each one of them. \n\n The chat will follow this pattern: \n\n 1. User provides a sound description. \n 2. Assistant responds with a detailed description about what sonic features a synth patch would achieve to fulfill the asked sound description. \n 3. User asks for the parameters and their values. \n 4. Assistant provides the parameters and their values in the format: '[parameter]: value, [parameter2]: value, (...)'. \n\n Example: User: 'a soothing happy sound' \n Assistant: 'A synth patch achieving this sound would have (...)'\n User: 'Please provide the parameters and their values for this sound.' \n Assistant: '[waveform]: sine, (...)'. \n\n Only respond with the parameters and their values (format: [parameter]: value, [parameter2]: value, (...)), nothing else. Make sure to match your choice of parameters and their respective values to the user prompt."},
    {"role": "user", "content": "spherical sad dystopian howling"},
    {"role": "assistant", "content": "A synth patch achieving this sound would have a deep, resonant waveform, slow attack and long release times, low-pass filtering with high resonance, and a large amount of reverb to create an echoing, immersive atmosphere."},
    {"role": "user", "content": "Please provide the parameters and their values for this sound."},
    {"role": "assistant", "content": "[waveform]: sine, [Oscillator_Detune]: 5, [attack]: 0.650, [decay]: 1.0, [sustain]: 0.5, [release]: 3.0, [Filter_Type]: lowpass, [Filter_Cutoff]: 400, [Filter_Resonance]: 22, [Reverb_Amount]: 50, [Reverb_Size]: Large, [reverb_decay_time]: 2000, [Reverb_Dampening]: 59, "},
    {"role": "user", "content": "Create a sound that sounds like shiny strings, happy and virtuous"},
    {"role": "assistant", "content": "A synth patch for this sound would have a bright, harmonically rich waveform with a fast attack, a moderate sustain and a short release time. The high-pass filtering and moderate reverb would give the sound a sense of space, while maintaining a clean, crisp tonality."},
    {"role": "user", "content": "Please provide the parameters and their values for this sound."},
    {"role": "assistant", "content": "[waveform]: Sawtooth, [Oscillator_Detune]: 0, [attack]: 0.1, [decay]: 0.1, [sustain]: 0.35, [release]: 0.1, [Filter_Type]: highpass, [Filter_Cutoff]: 500, [Filter_Resonance]: 10, [Reverb_Amount]: 23, [Reverb_Size]: Medium, [reverb_decay_time]: 370, [Reverb_Dampening]: 28"},
    {"role": "user", "content": prompt + "This time, imidiately respond with a description of the sound you want to create and the parameters and values at once."},
    ]
    

    #response_synth_parameters = send_message_to_chatgpt(message_synth_parameters, role="user", model="gpt-3.5-turbo", temperature=0, include_beginning=False, is_list=True)
    response_synth_parameters = "etst"
    print(response_synth_parameters)
    # message: 
    return response_synth_parameters


### Prerequisites

message_intro = [
    {"role": "system", "content": "You are a composer and sound designer. Your objective is to create a music or soundscape that matches the description given by the user. You must only respond in the format specified by the user, you won't add anything else to your responses."},
    ]

# dictionary. First key is "simple", second key is "complex"
example_prompts = {"prompt1": "A sad slow song","prompt2": "An irish folk melody", "simple3": "gloomy thunder" , "simple4": "sped-up pink panther", "complex1": "mozart, epic strings, heroic and fast"}

### Main Code

# main
def main():
    # get the input from the user

    user_input = input("Describe the music or soundscape you want to hear: \n\n")

    # message: synth parameters and values
    ## POP (prompt-optimization-prompt): 
    # This is a set of messages, forming a fictional chat history, that will be leveraged to ChatGPT. After the last user message with the variable "user_input" (which consists of a prompt describing a sound), ChatGPT will respond with a set of parameters and their respective values.
    # Now, I want to modify this set of messages. I want in between the user prompt and the response with the parameters and values a middle step in which the assistant responds with a detailed description about what sonic features a synth patch would achieve to fulfill the asked sound description in the user prompt. Afterwards the user will ask for the parameters and their values (they will stay the way they are as in the text above) and receive the respective response. Make this for both occasions where a prompt gets a response. The initial system message will anticipate this process and predict it by describing this behavior that will happen in the future chat. 
    
    def get_decision_add_edit(prompt):
        message_decision_add_edit = [
        {"role": "user", "content": "I am going to provide you with the prompt of a user. You will have to choose one of two options: 1- 'add': Use this option if the user's prompt is about creating, discovering, or discussing a new sound without mentioning any modification, manipulation, or follow-up instruction. 2 - 'Edit': Use this option if the user's prompt is about modifying, manipulating, or providing follow-up instruction for a pre-existing sound. You should only reply with one of these two words, and nothing else. Repeat my instructions so that I can see that you have understood my task. Then wait for the first prompt. You should only reply with one of these two words, and nothing else. Repeat my instructions so that I can see that you have understood my task. Then wait for the first prompt."},
        {"role": "assistant", "content": "I will choose one of the two options: 'add' if the user's prompt is about creating, discovering, or discussing a new sound without mentioning any modification, manipulation, or follow-up instruction; or 'Edit' if the user's prompt is about modifying, manipulating, or providing follow-up instruction for a pre-existing sound. I will only reply with one of these two words and nothing else. I have understood your task and am now waiting for the first prompt."},
        {"role": "system", "content": example_prompts["prompt1"]},
        {"role": "user", "content": "add a sound that sounds like a wind in trees"},
        {"role": "system", "content": "add"},
        {"role": "user", "content": "make it more sharp"},
        {"role": "system", "content": "edit"},
        {"role": "user", "content": "a spherical sound with sub-bass frequencies"},
        {"role": "system", "content": "add"},
        {"role": "user", "content": "enhance sub-bass"},
        {"role": "system", "content": "edit"},
        {"role": "user", "content": "add a high-shelf"},
        {"role": "system", "content": "edit"},
        {"role": "user", "content": prompt},
        ]
        response_add_edit = send_message_to_chatgpt(message_decision_add_edit, role="user", model="gpt-3.5-turbo", temperature=0, include_beginning=True, is_list=True)

        return response_add_edit

    def prompt_enhancer (prompt,mode):
        if mode == "sounddesign":
            message_prompt_enhancer = [
                {"role": "user", "content": "Describe a synth patch that that should sound like: 'feeling of a warm, sunny afternoon.'"},
                {"role": "assistant", "content": "To recreate the feeling of a warm, sunny afternoon in a synth patch, we'd focus on generating a bright, uplifting tone with a touch of warmth. This could be achieved by using sawtooth waveforms for their rich, full-bodied sound. The filter cutoff frequency should be set relatively high to allow for a bright timbre, but not overly so, ensuring that the sound isn't harsh. For the 'warmth,' a touch of gentle tube or tape saturation could be applied, and subtle modulation to pitch and filter cutoff via an LFO could be used to emulate the subtle, lazy fluctuations of a summer day. A touch of reverb with a longer decay time could provide a sense of openness and space, mimicking the expansiveness of an outdoor setting."},
                
                {"role": "user", "content": "Create a sound design description for a synth patch that should sound like: 'a cold, desolate winter night.'"},
                {"role": "assistant", "content": "To emulate the cold, desolate nature of a winter night, a synth patch would employ sparse, icy textures. The choice of waveform would likely be a sine or triangle for their clear, simple tones. The filter would be set to a lower cutoff frequency, with a small amount of resonance to create a chilly, cutting sound. Modulation effects like phase shifting or flanging could be used subtly to create a sense of movement and desolation. A longer attack time would be used to give the patch a slow, evolving feel. Lastly, a generous amount of spacious reverb and a bit of delay could evoke the vast, lonely echo of a winter's night."},
                
                {"role": "user", "content": f"Create a sound design description for a synth patch that should sound like: '{prompt}'"},
            ]

        elif mode == "melody":
            message_prompt_enhancer = [
                {"role": "user", "content": f"Create a meaningful, detailed and creative description for a fictional melody described with the words: 'Sad, melancholic melody, muted instrumental tones, slow, conveying a somber atmosphere and steady rhythm'. Only provide a music-theoretical description about how the melody would be written"},
                {"role": "assistant", "content": f"The sad and melancholic melody would likely be composed in a minor key, with long sustained notes and subtle chromatic inflections that create a feeling of emotional tension and unease. The melody would likely be characterized by a slow tempo, with a low BPM, which allows for ample space between each note, creating a somber atmosphere. he melody would be arranged in a way that emphasizes the muted quality of the instrumentation, with gentle dynamics that never rise too high or too low."},
                {"role": "user", "content": f"Create a meaningful, detailed and creative description for a fictional melody described with the words: '{prompt}'"},
                ]
            
        else:

            message_prompt_enhancer = [
                {"role": "user", "content": f"Enhance this prompt with sound-describing adjectives: {example_prompts['prompt1']}"},
                {"role": "assistant", "content": f"Sad, melancholic melody, muted instrumental tones with a low BPM, conveying a somber atmosphere and steady rhythm"},
                {"role": "user", "content": f"Enhance this prompt: seagulls in the wind"},
                {"role": "assistant", "content": f"Seagulls producing mid to high-pitched vocalizations as they navigate moderate wind conditions, with their calls varying in volume and frequency, generating an ambient soundscape."},
                {"role": "user", "content": f"Enhance this prompt: {prompt}"},
                ]
        
        response_prompt_enhancer = send_message_to_chatgpt(message_prompt_enhancer, role="user", model="gpt-3.5-turbo", temperature=1, include_beginning=True, is_list=True)
        pass

        return response_prompt_enhancer

    response_add_edit = get_decision_add_edit(user_input)
    print(response_add_edit + "\n")

    response_prompt_enhancer_main = prompt_enhancer(user_input,mode="")
    print(response_prompt_enhancer_main + "\n")

    if "add" in response_add_edit:
        #### musical
        response_prompt_enhancer_melody = prompt_enhancer(response_prompt_enhancer_main,mode="melody")
        print(response_prompt_enhancer_melody + "\n")
        
        def get_melody(prompt):
            
            message_melody = [                    
                {"role": "user", "content": f"'{user_input}. {response_prompt_enhancer_melody}'. Create a MIDI file that matches the description of the melody. Use the MIDIUtil Python library and only respond with a list of tuples, where each tuple represents a single note in the format (pitch, velocity, duration). The pitch is an integer value between 0 and 127, representing the note's frequency according to the MIDI standard. The velocity is an integer value between 0 and 127, representing the note's intensity or loudness, with higher values indicating a louder note. The duration is a positive integer representing the length of the note in beats. Please provide a full melody using this format: melody = [(PITCH_1, VELOCITY_1, DURATION_1), (PITCH_2, VELOCITY_2, DURATION_2), (PITCH_3, VELOCITY_3, DURATION_3), ...]. Replace the placeholders (PITCH_n, VELOCITY_n, DURATION_n) with appropriate integer values for your melody. "},
                ]
            
            
            response_melody = send_message_to_chatgpt(message_melody, role="user", model="gpt-3.5-turbo", temperature=1.3, include_beginning=True, is_list=True)
            return response_melody
        
        """ def get_melody_with_intermediate_step(prompt):
            
            message_intermediate_step = [                    
                {"role": "user", "content": f"'{response_prompt_enhancer_melody}'. Create MIDI files that match the description of the melody. Use the MIDIUtil Python library and only respond with a list of tuples, where each tuple represents a single note in the format (pitch, velocity, duration). The pitch is an integer value between 0 and 127, representing the note's frequency according to the MIDI standard. The velocity is an integer value between 0 and 127, representing the note's intensity or loudness, with higher values indicating a louder note. The duration is a positive integer representing the length of the note in beats. Please provide a full melody using this format: melody = [(PITCH_1, VELOCITY_1, DURATION_1), (PITCH_2, VELOCITY_2, DURATION_2), (PITCH_3, VELOCITY_3, DURATION_3), ...]. Replace the placeholders (PITCH_n, VELOCITY_n, DURATION_n) with appropriate integer values for your melody."},
                ]
            
            response_melody = send_message_to_chatgpt(message_melody, role="user", model="gpt-4", temperature=0.1, include_beginning=True, is_list=True)
            return response_melody"""

        response_melody = get_melody(response_prompt_enhancer_main)
        #response_melody = get_melody_with_intermediate_step(response_prompt_enhancer_main)

        print(response_melody)

        #### sound design
        response_prompt_enhancer_sounddesign = prompt_enhancer(response_prompt_enhancer_main,mode="sounddesign")
        def get_parameter_adsr(prompt):
            message_parameter_values = [
                {f"Given the following parameter ranges for an ADSR (Attack, Decay, Sustain, Release) envelope in a synthesizer:\n\nAttack (A): 1-1000 ms\nDecay (D): 1-1000 ms\nSustain (S): 0-1 (proportional volume)\nRelease (R): 1-5000 ms\nPlease analyze the following user description and suggest suitable parameter values for the ADSR envelope that best capture the sonic properties described. Carefully consider the user's requirements and try to translate them into the ADSR envelope parameters.\n\nUser description: {prompt}\n\nPlease provide your parameter value suggestions for the Attack (A), Decay (D), Sustain (S), and Release (R) stages, by thinking how they correspond to the sonic properties specified by the user.\n\nYour response should follow this specific output format, suitable for easy extraction with Python:\n\njson\nCopy code\n{\n  \"Attack\": <value_A>,\n  \"Decay\": <value_D>,\n  \"Sustain\": <value_S>,\n  \"Release\": <value_R>\n}\nPlease note that the LLM should strictly adhere to the provided output format, and only include the suggested parameter values in its response, without any additional commentary or explanation."}
            ]
                
            
            response_parameter_values = send_message_to_chatgpt(message_parameter_values, role="user", model="gpt-3.5-turbo", temperature=1, include_beginning=True, is_list=True)
            return response_parameter_values
        
        #def get_parameters(prompt):

        response_parameter_values = get_parameter_adsr(response_prompt_enhancer_sounddesign)
        print("ADSR envelope parameter values: \n")
        print(response_parameter_values + "\n")

        pass
    elif "edit" in response_add_edit:

        pass

main()




