def pretty_card(list):
    card = [
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
        ["0", "0", "X", "0", "0"],
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    
    for col in range(5):
        aux = list[col*5:col*5+5]
        if col == 2:
            aux[2] = -1
            aux = sorted(aux)
            aux[0] = aux[1]
            aux[1] = aux[2]
            aux[2] = 'X'
        else:
            aux = sorted(aux)

        for row in range(5):
            card[row][col] = str(aux[row])

    s = ""
    for i in range (len(card)):
        s += '|{:^3s} {:^3s} {:^3s} {:^3s} {:^3s}|\n'.format(card[i][0], card[i][1], card[i][2], card[i][3], card[i][4])
    return s