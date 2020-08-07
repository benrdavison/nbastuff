import pandas as pd
import io
import random
import math
import scipy.stats
data= pd.read_csv("/Users/user/Library/Mobile Documents/com~apple~CloudDocs/ws/Projects/Statsketball/18_19tourneycs.csv")

num_of_sims= 1000
teams= data.to_numpy().tolist()
team_dict= {}
for i in range(0, len(teams)):
    team_dict[teams[i][2]]= [0, 0, 0, 0, 0, 0, 0]

def find_winners(input_list, round):
    winners= []
    for i in range(0, len(input_list)):
        if i % 2 != 0:
            pass
        else:
            team1= input_list[i]
            team2= input_list[i+1]
            #SRS Difference, Calculate Team 1 Win Probability from Odds Ratio (between 0 and 1)
            srs_diff= team1[3]-team2[3]
            team1_prob= scipy.stats.norm(0,10.36).cdf(srs_diff)
            #Random draw from (0, 1)
            draw= random.random()
            #If draw falls under Team 1 Win Prob, Team 1 Wins
            if draw <= team1_prob:
                winners.append(team1)
                team_dict[team1[2]][round] +=1
            else:
                winners.append(team2)
                team_dict[team2[2]][round] +=1

    return winners

def bracket_printout(round_list):
    for i in range(0, len(round_list)):
        temp_list= round_list[i]
        for j in range(0, len(temp_list)):
            print(str(temp_list[j][1])+ " " + temp_list[j][2]+ " " + str(temp_list[j][3]))
            if j % 2 != 0:
                print("")

        print("")
        print("")
        print("")

def tourney_sim(teams):
    for x in team_dict:
        team_dict[x][0] += 1

    round_32= find_winners(teams, 1)
    sweet_16= find_winners(round_32, 2)
    elite_8= find_winners(sweet_16, 3)
    final_4= find_winners(elite_8, 4)
    championship= find_winners(final_4, 5)
    winner= find_winners(championship, 6)
    #bracket_printout([teams, round_32, sweet_16, elite_8, final_4, championship, winner])

if __name__ == "__main__":
    for i in range(1, num_of_sims+1):
        tourney_sim(teams)

    for x in team_dict:
        for i in range(0, len(team_dict[x])):
            team_dict[x][i]= team_dict[x][i]/num_of_sims
        print(x+ " " + str(team_dict[x]))
