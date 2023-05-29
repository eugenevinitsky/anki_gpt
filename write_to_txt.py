
def write_to_txt(card_list):
    file = open('anki_cards.txt', 'w')

    print(card_list)

    for card in card_list:
        file.write('Q: ' + card[0] + "\n")
        file.write('A: ' + card[1] + "\n")
        file.write('\n')

    file.close()




