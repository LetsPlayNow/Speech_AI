import re

phrase = "– ([А-Я][А-Яа-я ]*)"
phrase_regex = re.compile(phrase)

dialogues = []
with open('war_and_peace.txt', encoding='windows-1251', mode='r') as f:
    i = 0
    dialogue = []
    last_match = 0
    for line in f:
        match = phrase_regex.match(line)
        if match:
            if abs(last_match - i) <= 10:
                dialogue.append(match[1])
            else:
                if dialogue:
                    dialogues.append(dialogue.copy())
                dialogue = []

            last_match = i
        i+=1


import json
with open('war_and_peace.corpus.json', 'w') as out_file:
    json.dump({'dialogues' : dialogues}, out_file, ensure_ascii=False)
