import streamlit as st

st.set_page_config(page_title="Meet The Team", layout="wide", page_icon="🤖")

st.markdown('<h1 style="text-align: center; color: #0066cc; font-weight: bold; margin-bottom: 10px;">Meet Our Amazing Team</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #666; margin-bottom: 30px;">The talented minds behind ExamEye</h3>', unsafe_allow_html=True)


# Custom CSS for styling 
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* Profile card styling */
        .profile-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            height: 100%;
        }
        
        /* Circular profile image */
        .profile-image {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #0066cc;
            margin: 0 auto 15px auto;
            display: block;
        }
        
        /* Team member name */
        .member-name {
            color: #333;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        /* Role title */
        .member-role {
            color: #0066cc;
            font-size: 16px;
            margin-bottom: 15px;
        }
        
        /* LinkedIn button */
        .linkedin-button {
            background-color: #0066cc;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 14px;
            display: inline-block;
            margin-top: 10px;
            transition: background-color 0.3s;
        }
        
        .linkedin-button:hover {
            background-color: #004d99;
        }
    </style>
""", unsafe_allow_html=True)

team_members = [
    {
        "name": "Alhanouf Alswayed",
        "role": "Back-End Developer",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
    },
    {
        "name": "Ezdhar Altamimi",
        "role": "Back-End Developer",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
    },
    {
        "name": "Mohanad Abouassonon ",
        "role": "Back-End Developer",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
    },
    {
        "name": "Faisal Almufarrih",
        "role": "Back-End Developer",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
    },
    {
        "name": "Mrawan Alhinidi",
        "role": "Back-End Developer",
        "image": "https://static.vecteezy.com/system/resources/previews/020/911/731/original/profile-icon-avatar-icon-user-icon-person-icon-free-png.png",
    }
]

cols = st.columns(5)
for i, member in enumerate(team_members):
    with cols[i]:
        st.markdown(f"""
            <div class="profile-card">
                <img src="{member['image']}" class="profile-image" alt="{member['name']}">
                <div class="member-name">{member['name']}</div>
                <div class="member-role">{member['role']}</div>
            </div>
        """, unsafe_allow_html=True)

# footer
st.markdown('<div style="text-align: center; margin-top: 50px; color: #666;">© 2025 ExamEye. All rights reserved.</div>', unsafe_allow_html=True)