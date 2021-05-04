import numpy as np
def generate_RR(n):
    '''
    Generate round robin line-up for n teams in a round robin event
    Using algorithm from https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
    Parameters:
    -----------
    n: int
        number of teams

    Returns:
    --------
    mat: n * n matrix
        ith row jth column represent the opponent for team i on round j

    Notes:
    n must be even integer
    '''
    if n % 2 != 0:
        raise ValueError("Not even number of teams")
    
    # init
    team1 = 1
    teams = np.array(range(2, n+1))
    matches = np.empty((0,n), int)

    def flatten_teams(arr, anchor_team = 1):
        '''
        Take in the current circle of teams with length n-1 and return the line up for n teams
        Assuming 1 is the anchor team.
        '''
        arr = np.insert(arr, 0, anchor_team, axis=0)

        line_up = np.zeros(n)

        for i,v in enumerate(arr):
            # take the opposite end of the array
            line_up[v-1] = arr[n-i-1]
        return line_up

    for i in range(n-1):
        matches = np.append(matches, [flatten_teams(teams)], axis=0)
        # put last team to first place
        teams = np.concatenate([[teams[-1]], teams[:-1]])
        print(matches, teams)
        # print(flatten_teams(teams))
    return matches

if __name__ == '__main__':
    print(generate_RR(14))
