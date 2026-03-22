import streamlit as st
import os

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Data Radar | Research Assistant",
    page_icon="📡",
    layout="wide",

)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Fixed header and footer
st.markdown("""
<div class="fixed-header">
    <h1>(((DATA <span style="color: red;">RADAR📡</span> )))</h1>
    <h2><span style="color: red;">R</span>esearch <span style="color: red;">A</span>nd <span style="color: red;">D</span>ata <span style="color: red;">A</span>nalysis <span style="color: red;">R</span>esource</h2>
</div>
<div class="fixed-footer">
    Scholarly Academic Resource by 
    <a href="https://wawerujm.github.io" target="_blank" style="color:white;text-decoration:underline;">
    James Waweru
    </a>
</div>
""", unsafe_allow_html=True)

# Content wrapper
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 1
if "df" not in st.session_state:
    st.session_state.df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "filename" not in st.session_state:
    st.session_state.filename = None
if "column_categories" not in st.session_state:
    st.session_state.column_categories = {}
if "cleaning_log" not in st.session_state:
    st.session_state.cleaning_log = []
if "test_results" not in st.session_state:
    st.session_state.test_results = []

# Routing based on page number
if st.session_state.page == 1:
    import pages.page1_upload as page1
    page1.show()
elif st.session_state.page == 2:
    import pages.page2_confirm as page2
    page2.show()
elif st.session_state.page == 3:
    import pages.page3_cleaning as page3
    page3.show()
elif st.session_state.page == 4:
    import pages.page4a_graphical as page4a
    page4a.show()
elif st.session_state.page == 5:
    import pages.page4b_numerical as page4b
    page4b.show()
elif st.session_state.page == 6:
    import pages.page5_tests as page5
    page5.show()
elif st.session_state.page == 7:
    import pages.page6_documentation as page6
    page6.show()
else:
    st.error("Invalid page. Redirecting to start.")
    st.session_state.page = 1
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)