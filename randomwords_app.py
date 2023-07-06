import streamlit as st
import anthropic
from elevenlabs import generate, set_api_key

def generate_word():
    prompt = (f"{anthropic.HUMAN_PROMPT} Give me one non-English word that's commonly misspelled and the meaning. Please strictly follow the format! example: Word: Schadenfreude; Meaning: joy at other's expenses."
              f"{anthropic.AI_PROMPT} Word: Karaoke; Meaning: a form of entertainment where people sing popular songs over pre-recorded backing tracks."
              f"{anthropic.HUMAN_PROMPT} Great! just like that. Remember, only respond following the pattern.")

    c = anthropic.Anthropic(api_key=st.secrets["claude_key"])
    resp = c.completions.create(
        prompt=f"{prompt} {anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1.3-100k",
        max_tokens_to_sample=900,
    )

    print(resp.completion)
    return resp.completion

def generate_speech(word):
    set_api_key(st.secrets['xi_api_key'])
    audio = generate(
        text=word,
        voice="Bella",
        model='eleven_multilingual_v1'
    )

    return audio

st.title("Random Words Generator")

with st.container():
    st.header("Random Word")
    random_word = st.subheader("-")
    word_meaning = st.text("Meaning: -")

    st.write("Click the `Generate` button to generate new word")
    if st.button("Generate"):
        result = generate_word()
        # Split the string on the semicolon
        split_string = result.split(";")

        # Split the first part on ": " to get the word
        word = split_string[0].split(": ")[1]

        # Split the second part on ": " to get the meaning
        meaning = split_string[1].split(": ")[1]

        print(f"word result: {word}")
        random_word.subheader(word)
        word_meaning.text(f"Meaning: {meaning}")
        speech = generate_speech(word)
        st.audio(speech, format='audio/mpeg')
