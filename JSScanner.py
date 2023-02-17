import os
import requests
import re
import urllib3
import concurrent.futures
import colored
from colored import stylize
urllib3.disable_warnings()

print(stylize(
     " ╔════════════════════════════════════════════════════════════════╗\n"
      "║                    Devlope By 0x240x23elu                      ║\n"
      "║                    Mod By jjardel                              ║\n"
      "║                                                                ║\n"
      "╚════════════════════════════════════════════════════════════════╝",
    colored.fg("red")
))

print(stylize(
    "╔════════════════════════════════════════════════════════════════╗\n"
    "║                                                                ║\n"
    "║                           WARNING                              ║\n"
    "║                                                                ║\n"
    "║      I highly recommend using this tool by using Kali Linux OS ║\n"
    "║                                                                ║\n"
    "║      By using this tool it means you agree with terms,         ║\n"
    "║      conditions, and risks                                     ║\n"
    "║                                                                ║\n"
    "║      By using this tool you agree that                         ║\n"
    "║      1. use for legitimate security testing                    ║\n"
    "║      2. not for crime                                          ║\n"
    "║      3. the use of this tool solely for                        ║\n"
    "║         educational reasons only                               ║\n"
    "║                                                                ║\n"
    "║      By using this tool you agree that                         ║\n"
    "║      1. You are willing to be charged with criminal or state   ║\n"
    "║         law applicable by law enforcement officers             ║\n"
    "║         and government when abused                             ║\n"
    "║      2. the risk is borne by yourself                          ║\n"
    "║                                                                ║\n"
    "║         Thank you and happy pentest                            ║\n"
    "║                                                                ║\n"
    "╚════════════════════════════════════════════════════════════════╝",
    colored.fg("white")
))

path = "/home/kali/00-BUGBOUNTY/JSScanner"
reg = "/home/kali/00-BUGBOUNTY/JSScanner/regex.txt"
text_files = [f for f in os.listdir(path) if f.endswith('.txt')]
text_files.sort()

# mostrar opções do menu
print("Selecione um arquivo de texto: ")
for i, f in enumerate(text_files):
    print(f"{i+1} - {f}")

# pedir entrada do usuário e validar
selection = None
while not selection:
    try:
        selection = int(input("Opção: "))
        if selection < 1 or selection > len(text_files):
            raise ValueError
    except ValueError:
        print("Opção inválida. Tente novamente.")
        selection = None

# selecionar arquivo escolhido e usar na aplicação
chosen_file = os.path.join(path, text_files[selection-1])
print(f"Arquivo selecionado: {chosen_file}")

with open(chosen_file, 'r') as file1:
    lines = file1.readlines()

    for line in lines:
        ip = line.strip()
        print(colored.fg("white"), ip)

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(requests.get, ip) for _ in range(1)]

            results = [f.result().text for f in futures]

            with open(reg, 'r') as file2:
                lines2 = file2.readlines()

                for line2 in lines2:
                    regex = line2.strip()

                    matches = re.finditer(regex, str(results), re.MULTILINE)

                    for matchNum, match in enumerate(matches, start=1):
                        print(colored.fg("green"), "Regex: ", regex)
                        print(colored.fg("red"), "Match {matchNum} was found at: {match}".format(
                            matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()), '\n')

                        #with open('zzzzzzzzzzzzzzzout.txt', 'a') as file3:
                        with open(f'zResultado-{text_files[selection-1]}', 'a') as file3:
                            L = [ip, '\n', "Regex: ", regex, '\n', "Match {matchNum} was found at: {match}".format(
                                matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()), '\n']
                            file3.writelines(L)

        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            print("Error: {}".format(e))



