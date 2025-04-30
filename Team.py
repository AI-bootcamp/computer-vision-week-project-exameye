# Team.py

import streamlit as st

st.set_page_config(page_title="Our Team", page_icon="👨‍💻")

def main():
    st.markdown("""
        <style>
            h1 {
                color: black;
                text-align: center;
            }
            .team-header {
                color: #1E90FF;
                font-size: 22px;
                font-weight: bold;
            }
            .team-subtext {
                color: white;
                margin-bottom: 20px;
            }
            .member-block {
                color:black;
                background-color: #F0F8FF;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1> ExamEye Development Team</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="team-subtext">
        We are a team of skilled.behind ExamEye — focused on building scalable and intelligent grading systems using Computer Vision and OCR.
    </div>
    """, unsafe_allow_html=True)

    # Team members
    members = [
        ("Alhanouf", "Back-End Developer"),
        ("Ezdhar", "Back-End Developer"),
        ("Mohanad", "Back-End Developer"),
        ("faisal", "Back-End Developer"),
        ("Marwan", "Back-End Developer"),

    ]

    for name, role in members:
        st.markdown(f"""
        <div class="member-block">
            <div class="team-header">👤 {name}</div>
            <div>{role}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#1E90FF;'>Together, we built ExamEye to make grading fast, accurate, and hassle-free.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
