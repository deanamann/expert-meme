import streamlit as st
import os
import base64

def _set_bg_from_local(image_path: str):
    if not os.path.exists(image_path):
        return
    with open(image_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
      background-image: url("data:image/jpg;base64,{b64}");
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
    }}
    .stApp section, .css-1lcbmhc {{
      background: rgba(255,255,255,0.92);
      color: #000;
    }}
    .stApp h1, .stApp h2, .stApp p, .stApp .stText, .stApp .stMarkdown {{
      color: #000;
    }}
    .stApp h1, .stApp p {{
      text-align: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

_set_bg_from_local("background.jpg")

# Initialize session state
if 'accepted' not in st.session_state:
    st.session_state['accepted'] = False
if 'rejectcount' not in st.session_state:
    st.session_state['rejectcount'] = 0


if st.session_state['accepted']:
    # Load valentine.png as base64
    valentine_b64 = ""
    if os.path.exists("valentine.png"):
        with open("valentine.png", "rb") as f:
            valentine_b64 = base64.b64encode(f.read()).decode()

    # Load hearts.png as base64
    hearts_b64 = ""
    if os.path.exists("hearts.png"):
        with open("hearts.png", "rb") as f:
            hearts_b64 = base64.b64encode(f.read()).decode()

    # Heart rain animation + message using st.components.v1.html so JS runs
    import streamlit.components.v1 as components

    components.html(f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: rgba(255, 255, 255, 0.95);
            font-family: 'Source Sans Pro', sans-serif;
            overflow-x: hidden;
        }}
        @keyframes fall {{
            0% {{ transform: translateY(-10vh) rotate(0deg); opacity: 1; }}
            70% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
        }}
        .heart-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            overflow: hidden;
            z-index: 9998;
        }}
        .heart {{
            position: absolute;
            top: -10vh;
            animation: fall linear forwards;
            user-select: none;
        }}
        .heart img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .accepted-message {{
            position: relative;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.8); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        .accepted-message h1 {{
            color: #FF1493 !important;
            font-size: 4rem;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .accepted-message h2 {{
            color: #FF69B4 !important;
            font-size: 1.8rem;
            font-weight: 400;
            margin-top: 0;
            padding-top: 0;
        }}
        .valentine-img {{
            max-width: 300px;
            width: 60%;
            margin: 0.2rem 0;
            padding: 0;
            animation: fadeIn 2s ease-in-out;
        }}
    </style>
    </head>
    <body>
        <div class="heart-container" id="hearts"></div>
        <div class="accepted-message">
            <h1>Yayyy! 🥰</h1>
            <img class="valentine-img" src="data:image/png;base64,{valentine_b64}" alt="Valentine" />
            <h2>I cant wait to see you next week xx</h2>
        </div>

        <script>
            const container = document.getElementById('hearts');
            const heartSrc = "data:image/png;base64,{hearts_b64}";
            for (let i = 0; i < 50; i++) {{
                const heart = document.createElement('div');
                heart.classList.add('heart');
                const img = document.createElement('img');
                img.src = heartSrc;
                const size = 30 + Math.random() * 60;
                heart.style.width = size + 'px';
                heart.style.height = size + 'px';
                heart.appendChild(img);
                heart.style.left = Math.random() * 100 + 'vw';
                heart.style.animationDuration = (2 + Math.random() * 3) + 's';
                heart.style.animationDelay = (Math.random() * 2.5) + 's';
                container.appendChild(heart);
            }}
        </script>
    </body>
    </html>
    """, height=700, scrolling=False)


else:
    heart_path = "heart.gif"
    if heart_path:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(heart_path, width=50, use_container_width=True)

    st.title("Will you be my valentine?")
    st.write("I know this doesnt really work as im not here, but still will you be my valentine?")

    base_no_width = 200
    base_yes_width = 200
    no_scale = max(0.0, 1.0 - 0.2 * st.session_state['rejectcount'])
    yes_scale = 1.0 + 0.3 * st.session_state['rejectcount']

    no_width = int(base_no_width * no_scale)
    yes_width = int(base_yes_width * yes_scale)

    st.markdown(f"""
    <style>
        div[data-testid="column"] {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        div[data-testid="column"]:nth-of-type(1) {{
            min-width: {yes_width}px !important;
            flex: 0 0 {yes_width}px !important;
        }}
        div[data-testid="column"]:nth-of-type(3) {{
            min-width: {no_width}px !important;
            flex: 0 0 {no_width}px !important;
            opacity: {no_scale};
        }}
        div.stButton > button {{
            width: 100%;
            height: {int(48 * yes_scale)}px;
            font-weight: 700;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
            font-size: {int(16 * yes_scale)}px;
        }}
        div[data-testid="column"]:nth-of-type(3) div.stButton > button {{
            height: {int(48 * no_scale)}px;
            font-size: {int(16 * no_scale)}px;
        }}
        div.stButton > button[kind="primary"] {{
            background-color: #FF1493;
            color: white;
        }}
        div.stButton > button[kind="secondary"] {{
            background-color: #808080;
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

    messages = [
        "Think again!",
        "Really??",
        "Why nottt :(",
        "Awwww Mann",
        "You have to say yes now :)"
    ]

    col1, col2, col3 = st.columns([yes_scale, 0.1, max(no_scale, 0.1)])

    with col1:
        if st.button("Yes", key="yes_btn", type="primary", use_container_width=True):
            st.session_state['accepted'] = True
            st.rerun()

    with col3:
        if no_width > 0:
            if st.button("No", key="no_btn", type="secondary", use_container_width=True):
                st.session_state['rejectcount'] += 1
                st.rerun()

    if st.session_state['rejectcount'] > 0:
        idx = min(st.session_state['rejectcount'] - 1, len(messages) - 1)
        st.info(messages[idx])