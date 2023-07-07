import streamlit as st
import json
from data import get_summary, region_list, get_champion_pool
import matplotlib.pyplot as plt
import pandas as pd


def display_champion_images(champions, champion_data):
    row = ""
    for i, champion in enumerate(champions):
        image_url = f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/{champion_data[champion]['image']['full']}"
        row += f'<img src="{image_url}" alt="{champion}" width="60" height="60" style="margin: 3px"/>'
    # Display all the images
    if row != "":
        st.markdown(row, unsafe_allow_html=True)

def summoner_info(summoner_name, region):

    stats = get_summary(summoner_name, region)
    if stats:
        # Display summoner info
        name = summoner_name.replace('%20', ' ')
        st.subheader(f"{name}")  
        tier = stats['tier'].lower()
        tier = tier[0].upper() + tier[1:]
        rank = f"{tier} {stats['rank']}"
        lp = stats['leaguePoints']
        st.write(f"__{rank}__ - {lp} LP")

        col1, col2 = st.columns([2,7])
    
        with col1:
            # Calculate win rate percentage
            wins = stats['wins']
            losses = stats['losses']
            total_games = wins + losses
            win_rate = (wins / total_games) * 100

            # Display plot
            # Create a circle at the center of the plot
            my_circle = plt.Circle((0, 0), 0.7, color="#0E1117")
            # Create the pie chart
            fig, ax = plt.subplots(figsize=(6,4),facecolor="#0E1117")
            ax.pie([wins, losses],colors=['skyblue', 'red'])

            # Add the title 
            caption = f"{total_games}G {wins}W {losses}L"
            ax.set_title(caption, loc='center', fontsize=20, color="#FAFAFA")

            # Add the win rate text in the middle of the pie chart
            ax.text(0, 0, f"{int(win_rate)}%", horizontalalignment='center', verticalalignment='center', fontsize=20,
                    color="#FAFAFA")
            
            # Add the circle to the plot
            p = plt.gcf()
            p.gca().add_patch(my_circle)

            # Show the graph in Streamlit
            st.pyplot(fig)

        # Display champion pool
        with col2:
            df = get_champion_pool(summoner_name, region)
            st.dataframe(df)
    
    # No data available
    else: 
        st.subheader('Sorry, no ranked data available')

    
def champion_draft():
    st.subheader("Champion Draft Pick")
    # Fetch champion data
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
    summoner_name = summoner_name.replace(" ", "%20")
    
    # Regions Dropdown
    regions = region_list.keys()  # Add more regions as needed
    selected_region = st.selectbox("Select Region:", regions)
 
    
    if summoner_name:
        tab1, tab2= st.tabs(["Summary", "Champion Draft"])     
        with tab1:
            summoner_info(summoner_name, selected_region)

        with tab2:
            champion_draft()


if __name__ == "__main__":
    main()
    
