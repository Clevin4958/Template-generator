import numpy as np
import csv
from math import ceil
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
        # print(flatten_teams(teams))
    return matches

def gen_csv(matches, highest_set=2):
    '''
    generate array in the form ready for csv. It will include header and table number.

    Parameter:
    ----------
    n: int
        number of tables
    matches: m * n array
        m rows (matches) of n tables
    highest_set: int
        number of sets of boards used, unlimited if set to -1.
    '''
    m, n = matches.shape

    # set up header
    header = ['Round'] + ['NS', 'EW', 'Boards'] * n
    table_row = ['Table->'] + [None] * (n * 3)
    for i in range(n):
        table_row[3 * i + 1] = i + 1

    # transpose matches
    matches = np.transpose(matches)

    # prepare set number columns
    bd_sets = []
    highest_set = 2
    if highest_set == -1:
        bd_sets = np.array(range(1, m+1))
    else:
        unit = range(1, highest_set + 1)
        # repeat the unit set and take first m elem
        bd_sets = np.array(list(unit) * ceil(m / highest_set))[:m]

    # get center section of the output (product is 1d array)
    result = np.array(range(1, m+1))
    for i in range(n):
        # concat result, NS, ES, boards
        NS = np.empty(m)
        NS.fill(i + 1)
        result = np.concatenate((result, NS, matches[i], bd_sets))

    # transpose back
    result = result.astype('int32')
    result = result.reshape((3*n+1, m))
    result = np.transpose(result)

    print([header, table_row], result)
    # concat headers
    result = np.concatenate([[header, table_row], result], axis=0)
    return result.tolist()

def export(content, file_name):
    with open(file_name, 'w', newline='') as f:
        write = csv.writer(f, lineterminator=',\r\n')
        write.writerows(content)

if __name__ == '__main__':
    data = gen_csv(generate_RR(12))
    export(data, '12 team RR.csv')
