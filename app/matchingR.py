import streamlit as st
from streamlit_extras.colored_header import colored_header
import json
import random
import pandas as pd



def displayGraphG():
    d,m,p = st.columns(3)
    description = st.container()
    indices =list(st.session_state.currentSpot)
    d.selectbox("Domaine",st.session_state.GEN.keys(),index=indices[0],format_func=lambda x : st.session_state.GEN[x]["prefLabel"][0]["@value"],key="domain")
    m.selectbox("Métier",st.session_state.GEN[st.session_state.domain]["children"],index=min(indices[1],len(st.session_state.GEN[st.session_state.domain]["children"])-1),format_func=lambda x : x["prefLabel"][0]["@value"],key="job")
    p.selectbox("Poste",st.session_state.job["children"],index=min(indices[2],len(st.session_state.job["children"])-1),format_func=lambda x : x["prefLabel"][0]["@value"],key="occupation")

    with description:
        occupation = st.session_state.occupation["prefLabel"][0]["@value"]
        colored_header(occupation,"",color_name="blue-30")
        st.info(f'The "{occupation}" is a- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam molestie gravida turpis sit amet pellentesque. Aliquam suscipit posuere egestas. Quisque ac sapien eros. Sed gravida dictum dui ut condimentum. Integer accumsan turpis ut nulla iaculis pulvinar. Donec efficitur, odio quis dignissim consequat, urna magna mattis tellus, vel rutrum ipsum sem ac odio. Donec diam nibh, placerat ut risus a, lobortis blandit risus. Vestibulum ac mattis enim, sed sollicitudin justo. Duis eget pretium libero. Phasellus facilisis velit vel odio molestie, ut interdum nisi facilisis.')

def displayName(x):
    if x != "No filter":
        return x + " - " + st.session_state.ROMEnames[x]
    return x

def displayGraphD():
    css='''
    <style>
        [class="st-emotion-cache-keje6w e1f1d6gn2"] {
            overflow-y: scroll;
            overflow-x: hidden;
            max-height: 50rem;
        }
    </style>
    '''

    st.markdown(css,unsafe_allow_html=True)
    df = st.session_state.matching.loc[st.session_state.matching["Libelle GEN"] == st.session_state.occupation["prefLabel"][0]["@value"],["V","Code ROME","Libelle ROME","score"]].sort_values(by='score', ascending=False)
    df['column_name'] = pd.Categorical(df['V'], categories=['Oui', 'Na', 'Non'], ordered=True)
    df= df.sort_values('column_name')

    if len(df) == 0:
        st.warning("No proposed match for this particular occupation")
    else:
        filter = st.selectbox("Domain Filter",["No filter"] + list("ABCDEFGHIJKLMN"),format_func=lambda x :displayName(x),key= "filter 1")

        if filter != "No filter":
            names = [name for name in st.session_state.ROMEnames.keys() if (name.startswith(filter) and len(name)==3)]
            filter2 = st.selectbox("Job Card Filter",["No filter"]+ names,format_func=lambda x :displayName(x),key= "filter 2")

            if len(filter2)==3:
                names2 = [name for name in st.session_state.ROMEnames.keys() if (name.startswith(filter2) and len(name)==5)]
                filter3 = st.selectbox("Job Filter",["No filter"]+ names2,format_func=lambda x :displayName(x),key= "filter 3")
                filter = filter2
                
                if len(filter3) == 5:
                    filter = filter3
        

        if filter != "No filter":
            df = df[df["Code ROME"].str.startswith(filter)]
        if len(df) == 0:
            st.warning("No matches for selected filters")
        with st.container():
            for rank,row in df.iterrows():
                try:
                    description = st.session_state.defs[row["Libelle ROME"]]
                except:
                    description = "No description available"
                
                if row["V"] == "Oui": 
                    st.subheader(f'{row["score"]} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="green")
                    with st.expander("Description"):
                        st.info(description)

                    if st.button("Unmatch",use_container_width=True,key=f"{rank}submit"): 
                        st.session_state.matching.loc[rank,"V"] = "Non"
                        st.rerun()
                    
                elif row["V"] == "Non" :  
                    st.subheader(f'{row["score"]} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="red")
                    with st.expander("Description"):
                        st.info(description)

                    if st.button("Match",use_container_width=True,key=f"{rank}submit"): 
                        st.session_state.matching.loc[rank,"V"] = "Oui"
                        st.rerun()
                
                else:
                    st.subheader(f'{row["score"]} % | {row["Code ROME"]} - {row["Libelle ROME"]}',divider="orange")
                    with st.expander("Description"):
                        st.info(description)
                    l,r = st.columns(2)
                    
                    if l.button("Match",use_container_width=True,key=f"{rank}lsubmit"): 
                        st.session_state.matching.loc[rank,"V"] = "Oui"
                        st.rerun()
                    if r.button("Unmatch",use_container_width=True,key=f"{rank}rsubmit"): 
                        st.session_state.matching.loc[rank,"V"] = "Non"
                        st.rerun()

            



def displaySidebar():
    with st.sidebar:
        st.header("Use Cases",divider="red")
        st.button("GEN Framework",use_container_width=True)
        st.header("Data Provider",divider="red")
        st.info("GEN")
        st.header("Targeted Framework",divider="red")
        l,r = st.columns(2)
        l.button("ROME Framework",use_container_width=True)
        r.button("ESCO Framework",use_container_width=True)
        st.header("Automatic Validation",divider="red")
        st.slider("Automatic Validation Treshold",0,99,90,1,key="seuil")
        


def displayMatching():
    st.header("Progression",divider="red")
    st.session_state.bools = [ (st.session_state.matching["V"] == "Oui") | (st.session_state.matching["score"] > st.session_state.seuil),
                                (st.session_state.matching["score"] > 2*st.session_state.seuil/3),
                                (st.session_state.matching["score"] > st.session_state.seuil/3),
                                (st.session_state.matching["score"] >= 0)]
    st.session_state.groups = [set(st.session_state.matching.loc[st.session_state.bools[i],"Libelle GEN"].unique()) for i in range(4)]

    for i in range(1, len( st.session_state.groups)):
            st.session_state.groups[i] -= set.union(* st.session_state.groups[:i])
    values = [len(group) for group in  st.session_state.groups]
    st.sidebar.progress((111-values[0])/111,f"Left to be validated : {111-values[0]}/111")
    colors = ["green","yellow","orange","red"]
    names = ["Validated"]+[f"Confidence Threshold {i+1}" for i in range(3)]
    desc = [ f"Items that have been mapped, either manually or automatically",
            f"Items with a suggested mapping above {2*st.session_state.seuil//0.3/10}%",
            f"Items with a suggested mapping above {st.session_state.seuil//0.3/10}%",
                f"Items with a suggested mapping above {0}%"]
    for i in range(4):
        colored_header(names[i],description=desc[i],color_name=f"{colors[i]}-70")
        if st.button(f"Access ({values[i]})",use_container_width=True,key=f'button{i}'): st.session_state["confiance"] = i 


def displayMatches():
    with st.expander("Occupations",expanded=True):
        colors = ["green","yellow","orange","red"]
        names = ["Validated",
                 "Automatic Validation",
                 "Manual Evaluation",
                 "Rejected"]
        colored_header(names[st.session_state.confiance],"",color_name=f"{colors[st.session_state.confiance]}-70")
        df = st.session_state.matching[st.session_state.matching["Libelle GEN"].isin( st.session_state.groups[st.session_state.confiance]) ].sort_values(by='Libelle GEN', ascending=True).sort_values(by="score",ascending=False).drop_duplicates(subset="Libelle GEN")
        for rank,row in df.iterrows():
            b,g,s = st.columns([1,3,1])
            if b.button("Go To",key=f'goto{rank}',use_container_width=True) : 
                st.session_state.currentSpot = [int(i) for i in st.session_state.selectSpot[row["Libelle GEN"]]]
                js = '''
                        <script>
                            var body = window.parent.document.querySelector(".main");
                            console.log(body);
                            body.scrollTop = 0;
                        </script>
                        '''
                st.components.v1.html(js)
            g.info(row["Libelle GEN"])
            with s:
                if st.session_state.confiance == 0:
                    if row["V"] == "Oui":
                        st.success("VM")
                    else:
                        st.warning("VA")
                else:
                    st.metric("Best Mapping",row["score"])




def initialization():
    st.session_state.GEN = json.load(open("app/data/GEN/transformed_referentielGEN.json","rb"))
    st.session_state.matching = pd.read_csv("app/data/GEN/GEN_ROME.csv")
    st.session_state.defs = json.load(open("app/data/ROME/descriptionsROME.json","r"))
    st.session_state.selectSpot = json.load(open("app/data/GEN/selectSpot.json"))
    st.session_state.ROMEnames = json.load(open("app/data/ROME/ROME_names.json")) 
    st.session_state["confiance"] = 0
    st.session_state.currentSpot = [1,1,1]
    st.session_state.rules = []

def referentialMatching():


    if st.sidebar.button("Reset",use_container_width=True) or "GEN" not in st.session_state:
        with st.spinner("Loading Frameworks"):
            initialization()
    displaySidebar()
    col1, col2 = st.columns(2)
    st.divider()
    l,r = st.columns(2)
    with l:
        displayMatching()
    with r:
        displayMatches()
    with col1:
        st.header("GEN Framework",divider="red")
        displayGraphG()
    with col2:
        st.header("ROME Framework",divider="red")
        displayGraphD()

if __name__ == "__main__":
    st.set_page_config(page_title="matching tool",layout="wide")
    st.title("Outil de Matching de Référentiel")
    referentialMatching()