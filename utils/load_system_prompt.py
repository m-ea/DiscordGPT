def load_system_prompt():
    with open("system_prompt.txt", encoding='utf-8') as file:
        system_prompt = []
        for line in file:
            word = line.strip()
            system_prompt.append(word)
        system_prompt = " ".join(system_prompt)
    return str(system_prompt)