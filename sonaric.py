import requests
import pandas as pd
from rich import print
from rich.table import Table

title = """
 $$$$$$\                                          $$\           
$$  __$$\                                         \__|          
$$ /  \__| $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  $$\  $$$$$$$\ 
\$$$$$$\  $$  __$$\ $$  __$$\  \____$$\ $$  __$$\ $$ |$$  _____|
 \____$$\ $$ /  $$ |$$ |  $$ | $$$$$$$ |$$ |  \__|$$ |$$ /      
$$\   $$ |$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |      $$ |$$ |      
\$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$ |$$ |      $$ |\$$$$$$$\ 
 \______/  \______/ \__|  \__| \_______|\__|      \__| \_______|\n"""

def get_points(host):
  api = f"https://api.sonaric.xyz/telemetry/v1/clusters?query={host}"
  response = requests.get(api)
  if response.status_code == 200:
    data = response.json()
    try:
      return data['items'][0]['points']
    except (KeyError, IndexError):
      print(f"Error retrieving data for {host} : {response.status_code}")
      return None
      
def color_points(val):
    if val < 1000:
        color = "#889D9D"
    elif 1000 <= val < 3000:
        color = "#FFFFFF"
    elif 3000 <= val < 5000:
        color = "#1EFF0C"
    elif 5000 <= val < 7000:
        color = "#0070FF"
    elif 7000 <= val < 10000:
        color = "#A335EE"
    else:
        color = "#FF8000"
    return f"[{color} bold]{val}[/{color} bold]"

def create_legend(color_mapping):
    print(title)
    legend = "Légende des couleurs : \n----------------------\n"
    for color, range_str in color_mapping.items():
        legend += f"* [{color} bold]{range_str}[/{color} bold]\n"
    return legend

color_mapping = {
    "#889D9D": "Points inférieur à 1000",
    "#FFFFFF": "Points entre 1000 et 3000",
    "#1EFF0C": "Points entre 3000 et 5000",
    "#0070FF": "Points entre 5000 et 7000",
    "#A335EE": "Points entre 7000 et 10000",
    "#FF8000": "Points supérieur à 10000"
}

if __name__ == "__main__":
  hosts = ["Your_Nodes_Names"]
  results = {}
  total_points = 0
  for host in hosts:
    points = get_points(host)
    if points is not None:
      results[host] = points
      total_points += points

  if results:
    df = pd.DataFrame.from_dict(results, orient='index', columns=['Points'])
    df.index.name = 'Hosts'
    df = df.reset_index()
    df = df.sort_values('Points', ascending=False)  
    df['Points'] = df['Points'].apply(color_points)

    table = Table(show_header=True, header_style="bold #00ADEF")
    table.add_column("Hosts", style="dim")
    table.add_column("Points")

    for index, row in df.iterrows():
        table.add_row(row['Hosts'], str(row['Points']))

    colored_legend = create_legend(color_mapping)
    print("----------------------")
    print(colored_legend)
    table.add_row()
    table.add_row("Total", str(total_points), style="bold #00ADEF")

    print(table)
  else:
    print("No data retrieved from the API for any host.")
