import pandas as pd

if __name__ == "__main__":
    #reads data
    df = pd.DataFrame(pd.read_csv("gen1_pokemon_full.csv", sep=",")) #ngl I thought it was gonna be ";"" not "," caught me off guard for a min

    high_speed = df.sort_values(by="speed", ascending=False).iloc[:5, [1, 8]] #limits the list down to the top 5 pokemon with highest speed
    high_speed.to_json("top_5_speed.csv") #produces the csv
    
    
    
