import streamlit as st
from streamlit_extras.colored_header import colored_header
import json


# Initialization

def getReferentiel():
    st.session_state.ontology = json.load(open("app/ressources/smart.json"))["SmartOntology"]

def getGaming():
    initialize_session()
    st.session_state["edTechID"] = "gamingTest"
    st.session_state.fieldList = ["Experience Name",  "Date", "Associated Soft Skill Block", "User ID", "Results"]
    return None

def getJobsong():
    initialize_session()
    st.session_state["edTechID"] = "Jobsong"
    st.session_state.fieldList = ["Experience Id","Experience Label","Associated Hard Skills","Suggested Missions","Liked Missons"]
    return None

def getInokufu():
    initialize_session()
    st.session_state["edTechID"] = "Inokufu"
    st.session_state.fieldList = ["Nom","Url","Image","Keywords","Date"]
    return None

def parseFile():
    initialize_session()
    st.session_state['edTechID'] = st.session_state.file.name[:-5]
    data = json.load(st.session_state.file)
    
    first_item = data[0] if isinstance(data, list) else data
    st.session_state.fieldList = [key for key in first_item.keys()]

    st.session_state.download = True


def initialize_session():
    st.cache_data.clear()
    st.cache_resource.clear()
    """Initialise ou réinitialise les variables de session."""
    keys = [ "submitted", "submitted2", "propertyForm", "mappingForm","download",
        "experiences", "competencys", "choices", "skillblocks","profiles","rules","mapped"]
    for key in keys:
        st.session_state[key] = False if key in ["submitted", "download","submitted2", "propertyForm", "mappingForm"] else []
    getReferentiel()
    
# Affichage des infos

def displaySidebar():
    with st.sidebar:
        if st.sidebar.button("Reset", use_container_width=True): 
            initialize_session()
        st.header("Use Cases", divider="red")
        create_sidebar_buttons()

        colored_header("Data Provider", description="", color_name="red-70")
        st.info(st.session_state.edTechID)

        colored_header("EdTech File", description="", color_name="red-70")
        with st.expander(st.session_state.edTechID+".json"):
            for field in st.session_state.fieldList[:-1]:
                st.write(f"   ├─ {field} \n")
            st.write(f"   └─ {st.session_state.fieldList[-1]} \n")
            
        if st.session_state.download:
            st.sidebar.download_button("Download Sample File",data="",use_container_width=True,disabled=True)
        else:
            st.sidebar.download_button("Download Sample File",data=open(f"app/data/jsons/{st.session_state.edTechID.lower()}.json"),file_name=f"{st.session_state.edTechID.lower()}.json",use_container_width=True)


def create_sidebar_buttons():
    """Crée les boutons dans la barre latérale."""
    a, b = st.columns(2)
    st.sidebar.file_uploader("Choose a JSON file", type='json', label_visibility="collapsed", key="file",accept_multiple_files=False,)

    if a.button("Gaming Tests", use_container_width=True):
        getGaming()
    if b.button("Jobsong", use_container_width=True):
        getJobsong()
    if a.button("Inokufu", use_container_width=True):
        getInokufu()
    if b.button("Your Own", use_container_width=True,disabled=not(st.session_state.file)):
        parseFile()


def display_schema():
    """Affiche le schéma de l'ontologie."""
    with st.expander("Schéma", expanded=False):
        colored_header("ARIANE pivot ontology", "", color_name="red-70")
        st.image("app/ressources/ontologyVisualization2.png", use_column_width=True)

# Creation d'objets


def createObjects():
    st.header("Create your objects",divider="red")
    c,h = st.columns([1,2])
    with c:
        create_item_form()
    with h:
        if st.session_state.submitted:
            handle_item_submission()
    display_existing_items()

def create_item_form():
    with st.form("Item type"):
        colored_header("Add a new item:", description="", color_name="red-50")
        l,r = st.columns([3,1])
        l.selectbox("Select your Object type and language", ["Experience", "Competency", "Choice","Profile","Skill Block"], key="selectedType")
        r.selectbox("Select",["EN","DE","FR","ES","IT","RU","TR","UK","PL","RO"],key="language",label_visibility="hidden")
        object_count = len(st.session_state.competencys) + len(st.session_state.experiences) + len(st.session_state.choices) + len(st.session_state.skillblocks) + len(st.session_state.profiles)
        st.text_input("Name your Object", f"{st.session_state.edTechID} - Object {object_count}", help="Name your Object", key="objectName")
        if st.form_submit_button("Confirm", use_container_width=True) : st.session_state.submitted = True

def handle_item_submission():
    with st.form("property match"):
        colored_header("Define mandatory properties", description="Add each field which is an experience, a competency or an individual choice", color_name="red-50")
        item_type_handlers = {
            "Experience": handle_experience_submission,
            "Competency": handle_competency_submission,
            "Choice": handle_choice_submission,
            "Profile": handle_profile_submission,
            "Skill Block": handle_skillBlock_submission
        }
        selected_type_handler = item_type_handlers.get(st.session_state.selectedType, lambda: None)
        selected_type_handler()

def handle_experience_submission():
    l,r = st.columns(2)
    l.info("Experience Type")
    r.selectbox("objectFields",["Professional","Vocationnal","Educational","Test","Custom"],label_visibility="collapsed",key="selected")
    l,r = st.columns(2)
    l.info("Experience Status")
    r.selectbox("objectFields",["Past","Ongoing","Suggested"],label_visibility="collapsed",key="selected2")
    if st.form_submit_button("Confirm",use_container_width=True) : 
        st.session_state.experiences.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.language,st.session_state.selected,st.session_state.selected2))
        st.session_state.submitted = False
        st.rerun()

def handle_competency_submission():
    l,r = st.columns(2)
    l.info("Skill Type")
    r.selectbox("objectFields",["Hard Skill","Soft Skill","Personality Trait","Mixed"],label_visibility="collapsed",key="selected")
    l,r = st.columns(2)
    l.info("Experience")
    if len(st.session_state.experiences)>0:
        r.selectbox("objectFields",st.session_state.experiences,format_func=lambda x : x[1],label_visibility="collapsed",key="selected2")
        if st.form_submit_button("Confirm",use_container_width=True) : 
            st.session_state.competencys.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.language,st.session_state.selected,st.session_state.selected2[1]))
            st.session_state.submitted = False
            st.rerun()
    else:
        r.error("First create an experience")
        st.form_submit_button("Confirm",disabled=True)

def handle_skillBlock_submission():
    l,r = st.columns(2)
    l.info("Skill Type")
    r.selectbox("objectFields",["Hard Skill","Soft Skill","Personality Trait","Mixed"],label_visibility="collapsed",key="selected")
    l,r = st.columns(2)
    l.info("Experience")
    if len(st.session_state.experiences)>0:
        r.selectbox("objectFields",st.session_state.experiences,format_func=lambda x : x[1],label_visibility="collapsed",key="selected2")
        if st.form_submit_button("Confirm",use_container_width=True) : 
            st.session_state.skillblocks.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.language,st.session_state.selected,st.session_state.selected2[1]))
            st.session_state.submitted = False
            st.rerun()
    else:
        r.error("First create an experience")
        st.form_submit_button("Confirm",disabled=True)

def handle_choice_submission():
    l,r = st.columns(2)
    l.info("Polarity")
    r.selectbox("objectFields",["Like","Level"],label_visibility="collapsed",key="selected")
    l,r = st.columns(2)
    l.info("Experience")
    if len(st.session_state.experiences)>0:
        r.selectbox("objectFields",st.session_state.experiences,format_func=lambda x : x[1],label_visibility="collapsed",key="selected2")
        if st.form_submit_button("Confirm",use_container_width=True) : 
            st.session_state.choices.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.language,st.session_state.selected,st.session_state.selected2[1]))
            st.session_state.submitted = False
            st.rerun()
    else:
        r.error("First create an experience")
        st.form_submit_button("Confirm",disabled=True)

def handle_profile_submission():
    st.info("There are no mandatory properties for a profile, just press 'Confirm'")
    if st.form_submit_button("Confirm",use_container_width=True) : 
        st.session_state.profiles.append((st.session_state.selectedType,st.session_state.objectName,st.session_state.language,"No property","No property"))
        st.session_state.submitted = False
        st.rerun()


           
def display_existing_items():
    item_types = {
        "Experience": st.session_state.experiences,
        "Competency": st.session_state.competencys,
        "Choice": st.session_state.choices,
        "Skill Block": st.session_state.skillblocks,
        "Profile": st.session_state.profiles
    }
    if len(item_types["Experience"])>0:
        cols = st.columns([1.5,2,4.5,1])
        names = ["Type","Name","Properties","X"]
        for i in range(4):
            cols[i].subheader(names[i],divider="red")
    for item_type, items in item_types.items():
        for i, item in enumerate(items):
            display_item(item_type, item, i)

def display_item(item_type, item, index):
    cols = st.columns([1.5, 2,0.5,2,2, 1])
    cols[0].success(f"{item_type} n°{index}")
    for i,property in enumerate(item[1:]):
        cols[i+1].info(property)
    if cols[-1].button("🗑️", use_container_width=True, key=f"{item_type.lower()}{index}"):
        items = getattr(st.session_state, f"{item_type.lower()}s")
        items.pop(index)
        st.rerun()

# Matching

def matchingTool():
    colored_header("Mapping",description="Map all your fields to their relevant object and property",color_name="red-70")
    if len(st.session_state.experiences)+len(st.session_state.profiles)>0:
        createPropertyForm()           
        if st.button("Confirm mappings",use_container_width=True):
            createRules()
        if len(st.session_state.rules)>0:
            displayRules()
    else:
        st.warning("First create an object in the 'Object Creation' tab")                         

def createPropertyForm():
    cols = st.columns(3)
    names = ["Field","Object","Property"]
    for i in range(3):
        cols[i].subheader(names[i],divider="red")
        
    for field in st.session_state.fieldList:
        if field not in st.session_state.mapped:
            createMatchingForm(field)

def createMatchingForm(field):
    f,o,p = st.columns(3)
    f.info(field)
    o.selectbox("object",[[0,"No Mapping"]] + st.session_state.experiences + st.session_state.competencys + st.session_state.choices + st.session_state.skillblocks + st.session_state.profiles,label_visibility='collapsed', format_func=lambda x:x[1],key=f"object{field}")
    if st.session_state[f"object{field}"][1] != "No Mapping":
        properties = st.session_state.ontology[st.session_state[f"object{field}"][0]]["Properties"]
        p.selectbox("Propriété",properties,key=f"property4{field}",label_visibility="collapsed")
    else:
        p.selectbox("Propriété",[],key=f"property4{field}",label_visibility="collapsed")

def createRules():
    for field in st.session_state.fieldList:
        if field not in st.session_state.mapped:
            if st.session_state[f"object{field}"][1] != "No Mapping":
                rule = f"'{field}' is associated with the property '{st.session_state[f'property4{field}']}' of the object '{st.session_state[f'object{field}'][1]}'"
                st.session_state.rules.append(rule)
                st.session_state.mapped.append(field)
    st.rerun()


def displayRules():
    for i,rule in enumerate(st.session_state.rules):
        l,m,r = st.columns([1,10,1])
        l.success(f"Rule {i}")
        m.success(rule)
        if r.button("🗑️",use_container_width=True,key = f"Rule{i}"): 
            del st.session_state.rules[i]
            del st.session_state.mapped[i]
            st.rerun()


def ontologyMatching2():
    """Logique principale de l'outil de matching d'ontologie."""
    st.title("Outil de Mapping d'Ontologie")
    if "submitted" not in st.session_state:
        getGaming()
    getReferentiel()
    displaySidebar()
    display_schema()
    tabs = st.tabs(["Object Creation","Field Mapping"])
    with tabs[0]:
        createObjects()
    with tabs[1]:
        matchingTool()



# Définissez ici les autres fonctions nécessaires pour réduire la duplication de code.

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    st.title("Outil de Matching d'Ontologie")
    ontologyMatching2()
