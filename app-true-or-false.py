import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(page_title="True or False", page_icon=":robot:")
st.sidebar.header("ChatGPT True or False")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
        message(st.session_state["generated"][i], key=str(i))

def on_message_change():
    input_text = st.session_state.input
    st.session_state.past.append(input_text)
    output = openai.ChatCompletion.create(
	    model='gpt-3.5-turbo',
	    messages=[{
	        'role':'user',
	        'content':input_text
	    }],
	    logit_bias={
	        '2575': 100,
	        '4139': 100
	    },
	    max_tokens=1,
	    temperature=0
    ).choices[0].message.content
    st.session_state.generated.append(output)
    st.session_state.input = ""

input_text = st.text_input("You: ", "", key="input", max_chars=500, on_change=on_message_change)

style_stuff = f"""
<style>
    *, html {{
      scroll-behavior: smooth !important;
    }}
    .stTextInput {{
      position: fixed;
      bottom: 3rem;
    }}
</style>
"""
st.markdown(style_stuff, unsafe_allow_html=True)

js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    scroll({len(st.session_state.generated)})
</script>
"""
st.components.v1.html(js)

