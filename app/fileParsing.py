import streamlit as st
import time 

def fileAnalysis(file):
    time.sleep(2)
    questions =  '''1. Voulez vous vous intéresser à certaines clés dans ce référeniel ? Par exemple voulez vous seulement les objets "Job" ou "Sector" ?\n2. Quel niveau de détail voulez vous inclure dans votre référentiel ? Y a t il une profondeur limite ou voulez vous inclure tous les niveaux ??\n3. Comment voulez vous afficher votre référentiel ? sous la forme d'un graphe, ou du texte suffira ?'''
    return questions

def parsing(file, answer):
    time.sleep(2)
    referential = """- Gestion / Pilotage
  - Entrepreneuriat
    - Créateur d'entreprise
    - Entrepreneur digital
    - Startupper
  - Gestion de projet digital
    - Chef de projet agile
    - Chef de projet digital
    - Chef de projet technique
    - Coordinateur de projet
    - Directeur de projet
    - Scrum master
  - Gestion de site web
    - Chef de projet web
    - Webmaster
  - Management Produit
    - Product Manager
    - Product Owner
"""
    return referential

def fileParsing():
    st.sidebar.image("referentialMatching/ressources/logoMM.png")
    uploaded_file = st.sidebar.file_uploader("Choose a file",key="ufile")
    

    if uploaded_file is not None:

        if "parse" not in st.session_state:
            st.session_state.parse = False
        if "question" not in st.session_state:
            with st.spinner("Analyzing the file..."):
                st.session_state.question = fileAnalysis(uploaded_file)

        st.header("Notre IA a analysé le fichier, pour mieux l'aider à comprendre, veuillez répondre à ces questions :",divider="red")
        with st.expander("Assistant",expanded=True),st.chat_message("Assistant",avatar="🤖"):
            st.write(st.session_state.question)
        
        with st.form("ALTOR",clear_on_submit=True):
            st.text_area(label="Répondez comme si vous parliez à un humain",placeholder="1.\n2.\n3.",key="user_answer")
            if st.form_submit_button("Répondre"): st.session_state.parse = True
        
        
        if st.session_state.parse == True:
            if "info" not in st.session_state:
                with st.spinner("Parsing the file..."):
                    st.session_state.info = parsing(uploaded_file, st.session_state.user_answer)
            with st.expander("Assistant",expanded=True),st.chat_message("Assistant",avatar="🤖"):
                st.write("Voici un aperçu du référentiel que j'ai récupéré :")
                st.write(st.session_state.info[:200] + "\n...")
            with st.form("answer",clear_on_submit=True):
                l,m,r = st.columns(3)
                if l.form_submit_button("Ce référentiel me semble correct"):
                    st.success("Information saved successfully!")
                if m.form_submit_button("J'aimerai vérifier un peu plus"):
                    with st.chat_message("Assistant",avatar="🤖"):
                        st.write("Voici le référentiel complet")
                        st.write(st.session_state.info)
                if r.form_submit_button("Il y a un problème"):
                    st.session_state.parse = False
    else:
        st.image("referentialMatching/ressources/robot.jpeg")
        st.info("Uploadez votre fichier dans l'encadré à gauche de votre écran")
      
      

if __name__ == "__main__":
    st.title("Outil de Lecture de Référentiel")
    fileParsing()