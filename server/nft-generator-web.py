import streamlit as st
import os
from generator import NFTGenerator
from pathlib import Path
import zipfile
import secrets
import base64


def zipdir(path):
    ziph = zipfile.ZipFile(f'{path}.zip', 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
    ziph.close()


st.title("NFT generator")
st.subheader("talk to me at https://twitter.com/Stick_BUIDLer")
if 'gogo' not in st.session_state:
    print('init gogo')
    st.session_state.gogo = False

file = st.file_uploader('upload parts zip file', type=['zip'])
if file is not None and ('token' not in st.session_state):
    token = secrets.token_hex(nbytes=16)
    st.session_state.token = token
    st.write('session token - ' + token)
    file_name = token + '_' + file.name
    with open(file_name, 'wb') as fp:
        fp.write(file.read())
    active_path = token + '_parts'
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(active_path)

with st.sidebar:
    if 'token' in st.session_state:
        session_token = st.text_input('session token', st.session_state.token)
    else:
        session_token = st.text_input('session token')

    is_animate = st.checkbox('animate?')
    if is_animate:
        fps = st.number_input('fps', 1)
        n_frame = st.number_input('no. of frame', 1)

    test = st.button('test')
    st.session_state['test'] = True
    with st.form(key="generate?"):
        amount = st.number_input('amount', 1)
        unique = st.checkbox("unique mode")
        st.write('*unique mode will generate in order (not random)')
        submit_button = st.form_submit_button(label='go go')

if submit_button:
    print('GOGO')
    output_dir = session_token + '_output'
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)
    the_bar = st.progress(0)
    if is_animate:
        nft_generator = NFTGenerator(input_dir=session_token + '_parts', animate=is_animate, fps=fps, n_frame=n_frame,
                                     unique=unique)
        for i in range(amount):
            the_bar.progress((i + 1) / amount)
            nft_generator.generate(save_path=output_dir, file_name=i)
    else:
        nft_generator = NFTGenerator(input_dir=session_token + '_parts', unique=unique)
        for i in range(amount):
            the_bar.progress((i + 1) / amount)
            nft_generator.generate(save_path=output_dir, file_name=i)
    st.header("DONE!")
    zipdir(output_dir)
    data = open(output_dir + ".zip", "rb")
    b64 = base64.b64encode(data.read())
    st.markdown(
        f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="output.zip">output.zip</a>',
        unsafe_allow_html=True)

if test:
    if is_animate:
        nft_generator = NFTGenerator(input_dir=session_token + '_parts', animate=is_animate, fps=fps, n_frame=n_frame,
                                     unique=unique)
        sample = nft_generator.generate()
        st.image(sample, caption=[f'frame {i + 1}' for i in range(len(sample))])
    else:
        nft_generator = NFTGenerator(input_dir=session_token + '_parts', unique=unique)
        sample = nft_generator.generate()
        st.image(sample, caption="sample")
