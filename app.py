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
        row += f'<img src="{image_url}" alt="{champion}" width="120" height="120" style="margin: 5px"/>'
        if (i + 1) % 5 == 0:
            st.markdown(row, unsafe_allow_html=True)
            row = ""
    if row != "":
        st.markdown(row, unsafe_allow_html=True)

def main():
    st.title("League of Legends Champion Recommendation")
    
    # Summoner Name
    summoner_name = st.text_input("Enter Summoner Name:")
    
    # Regions Dropdown
    regions = region_list.keys()  # Add more regions as needed
    selected_region = st.selectbox("Select Region:", regions)
    
    # Fetch champion data
    # data = requests.get("http://ddragon.leagueoflegends.com/cdn/13.13.1/data/en_US/champion.json")
    # data = json.loads(data.text)
    # champion_data = data["data"]
    # Opening JSON file
    f = open('champion.json')
    
    # returns JSON object as 
    # a dictionary

    with open('champion.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Access the data from the JSON
    champion_data = data["data"]

    # Retrieve champion name list
    champion_list = list(champion_data.keys())


    # Banned Champions
    banned_champions_team = st.multiselect("Select Banned Champions for Your Team:", champion_list)
    banned_champions_enemy = st.multiselect("Select Banned Champions for Enemy Team:", champion_list)
    
    # Display the banned champion images
    st.subheader("Banned Champions - Your Team")
    display_champion_images(banned_champions_team, champion_data)

    st.subheader("Banned Champions - Enemy Team")
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

 


if __name__ == "__main__":
    main()
    
