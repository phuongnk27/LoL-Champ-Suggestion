import streamlit as st
import json
import requests



region_list = {
    "NA": "North America", "EUW": "Europe West",
    "EUN": "Europe Nordic & East", "KR": "Korea",
    "BR": "Brazil", "JP": "Japan",
    "RU": "Russia", "OCE": "Oceania",
    "TR": "Turkey", "LAN": "Latin America North",
    "LAS": "Latin America South", "PH": "Philippines",
    "SG": "Singapore", "TH":"Thailand",
    "TW": "Taiwan", "VN": "Vietnam"
}

def display_champion_images(champions, champion_data):
    row = ""
    for i, champion in enumerate(champions):
        image_url = f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/{champion_data[champion]['image']['full']}"
        row += f'<img src="{image_url}" alt="{champion}" width="60" height="60" style="margin: 3px"/>'
    # Display all the images
    if row != "":
        st.markdown(row, unsafe_allow_html=True)

def summoner_info():
    st.subheader("Summary")

def champion_draft():
    st.subheader("Champion Draft Pick")
    # Fetch champion data
    # Opening JSON file
    with open('champion.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Access the data from the JSON file
    champion_data = data["data"]

    # Retrieve champion name list
    champion_list = list(champion_data.keys())

    # Banned Champions
    banned_champions_team = st.multiselect("Select Banned Champions for Your Team:", champion_list, max_selections=5)
    banned_champions_enemy = st.multiselect("Select Banned Champions for Enemy Team:", champion_list, max_selections=5)

    # Display the banned champions
    st.subheader("Banned Champions")
    col1, col2 = st.columns([3, 3])
    with col1:
        st.caption("Your Team")
        display_champion_images(banned_champions_team, champion_data)
    with col2:
        st.caption("Enemy Team")
        display_champion_images(banned_champions_enemy, champion_data)
    

    # Perform Analysis and Display Recommendations
    if st.button("Get Champion Picked Recommendation"):
        # Perform your analysis based on the user inputs (summoner_name, selected_region, banned_champions)
        # Generate and display the counter champion recommendations
        
        # Example Output
        st.subheader("Champion Recommendations")
        st.write("These are the recommended champions:")
        st.write("- Champion 1")
        st.write("- Champion 2")
        st.write("- Champion 3")
        # Add more recommendations as needed


def main():
    st.title("League of Legends Champion Recommendation")
    
    # Summoner Name
    summoner_name = st.text_input("Enter Summoner Name:")
    
    # Regions Dropdown
    regions = region_list.keys()  # Add more regions as needed
    selected_region = st.selectbox("Select Region:", regions)
    
    if summoner_name:
        tab1, tab2= st.tabs(["Summary", "Champion Draft"])     
        with tab1:
            summoner_info()

        with tab2:
            champion_draft()


if __name__ == "__main__":
    main()
    
