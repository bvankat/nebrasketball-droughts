import json


###############################

# define the years you want to work on
years = ["2019"]

# to get another team, change lines 10, 47, 61, 92, 112
team = "Ohio+St."


#loop through each year in the list above
for year in years:
    
    #filenames
    clean_file_name = 'game_data_' + year + '_' + team.lower() + '.json'
    save_file = 'game_data_with_droughts_' + year + '_' + team.lower() + '.json'
    drought_file = 'game_droughts_' + year + '_' + team.lower() + '.json'  
    
    print("File: " + clean_file_name)
    print("File: " + save_file)
    print("File: " + drought_file)
    
    # open the game data file for the current season
    with open(clean_file_name) as f:
        games = json.load(f)
        
    print(str(year) + " game count: " + str(len(games)))
   
    all_droughts = [] 
    
    # initialize count for seasonlong drought counts
    season_three_plus = 0
    season_four_plus = 0
    season_five_plus = 0
    season_six_plus = 0
    season_seven_plus = 0
    season_eight_plus = 0
    
    game_count = len(games)
       
    for game in games:
    
        game_date = game["ymd"]
        
        if game["team1"] == "Ohio St.": # in game["input"] team names aren't slugified (e.g. "Ohio State")
            site = "Road"
            game_opponent = game["team2"]
        else: 
            site = "Home"
            game_opponent = game["team1"]
            
        print
        print(game_date, site, game_opponent)
        
        #sort the possessions from 40 to 0
        game["input"] = sorted(game["input"], key=lambda k: k["TL"], reverse=True)
        
        #find all the scoring possessions
        if game["team1"] == "Ohio St.":
            nebraska = [p for p in game["input"] if p["VSc"] == 1] #Nebraska is away team
            opponent = [p for p in game["input"] if p["HSc"] == 1]
    
        else:
            opponent = [p for p in game["input"] if p["VSc"] == 1]
            nebraska = [p for p in game["input"] if p["HSc"] == 1] #Nebraska is home team
            
    
        
        # calculate droughts on opponent scores
        for x,y in zip(opponent[::], opponent[1::]):
            y["Dr"] = (x["TL"] - y["TL"])
            
        # calculate droughts on nebraska scores
        for x,y in zip(nebraska[::], nebraska[1::]):
            y["Dr"] = (x["TL"] - y["TL"])
            
        # calculate drought for first home score
        opponent[0]["Dr"] = (40 - opponent[0]["TL"])
        
        # calculate drought for first away score
        nebraska[0]["Dr"] = (40 - nebraska[0]["TL"])
    
        # create and save list of home and away droughts
        
        game_droughts = {}
        
        # sort possessions by drought length
        nebraska_sorted = sorted(nebraska, key=lambda k: k["Dr"], reverse=True)
        opponent_sorted = sorted(opponent, key=lambda k: k["Dr"], reverse=True)
        print("Longest Ohio State drought: %.2f" % nebraska_sorted[0]["Dr"])
        print("Longest " + game_opponent + " drought: %.2f" % opponent_sorted[0]["Dr"])
        
        nebraska_droughts = [ p["Dr"] for p in nebraska_sorted ]
        opponent_droughts = [ p["Dr"] for p in opponent_sorted ]
        
        # tallying nebraska droughts by length
        droughts_by_length = []
        
        three_plus = len([p for p in nebraska_droughts if p >= 3])
        four_plus = len([p for p in nebraska_droughts if p >= 4])
        five_plus = len([p for p in nebraska_droughts if p >= 5])
        six_plus = len([p for p in nebraska_droughts if p >= 6])
        seven_plus = len([p for p in nebraska_droughts if p >= 7])
        eight_plus = len([p for p in nebraska_droughts if p >= 8])
        
        droughts_by_length.append({ "three_plus": three_plus, "four_plus": four_plus, "five_plus": five_plus, "six_plus": six_plus, "seven_plus": seven_plus, "eight_plus": eight_plus })
        
        print("3+ minute droughts for ", team, ": ", three_plus)
        
        game_droughts["ohio-state"] = nebraska_droughts
        game_droughts["opponent"] = opponent_droughts
        game_droughts["droughts-by-length"] = droughts_by_length
                
        all_droughts.append({ "date": game_date, "site": site, "opponent": game_opponent, "droughts": game_droughts })
        
        season_three_plus = season_three_plus + three_plus
        season_four_plus = season_four_plus + four_plus
        season_five_plus = season_five_plus + five_plus
        season_six_plus = season_six_plus + six_plus
        season_seven_plus = season_seven_plus + seven_plus
        season_eight_plus = season_eight_plus + eight_plus
        
        
    season_totals = { "season_three_plus": season_three_plus, "season_four_plus": season_four_plus, "season_five_plus": season_five_plus, "season_six_plus": season_six_plus, "season_seven_plus": season_seven_plus, "season_eight_plus": season_eight_plus, "games": game_count }
    
    all_droughts.append({"season-totals": season_totals})
    
        
        
    # save the new game data and drought_list to a file
        
        
    with open(save_file, 'w') as outfile:
        json.dump(games, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        
    with open(drought_file, 'w') as outfile:
        json.dump(all_droughts, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        