import streamlit as st
st.set_page_config(layout="wide")
from app.skillExtraction import skillExtraction
from app.matchingO2 import ontologyMatching2
from app.matchingR import referentialMatching

def main():
    st.sidebar.title("ARIANE Interoperability")
    st.sidebar.image("app/ressources/logoMM.png")
    st.sidebar.divider()
    if "selector" not in st.session_state:
        st.session_state.selector = ""
    if st.sidebar.button("Ontology Mapping",use_container_width=True) : st.session_state.selector = "Interface Ontologie" 
    if st.sidebar.button("Framework Mapping",use_container_width=True): st.session_state.selector = "Interface Référentiel"
    if st.sidebar.button("Training Enhancement",use_container_width=True): st.session_state.selector= "Skill Mapping"

    # Direct to the appropriate page
    if st.session_state.selector == "Interface Ontologie":
        ontologyMatching2()
    if st.session_state.selector == "Skill Mapping":
        skillExtraction()
    if st.session_state.selector== "Interface Référentiel":
        referentialMatching()


    
       
if __name__ == "__main__":
    main()
