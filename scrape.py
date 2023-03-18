import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import re
import pandas as pd


def extract_data(paragraph):

    # Extract the desired information using regular expressions
    aa_count = int(re.search(r"Number of amino acids: (\d+)", paragraph).group(1))
    mw = float(re.search(r"Molecular weight: ([\d.]+)", paragraph).group(1))
    pi = float(re.search(r"Theoretical pI: ([\d.]+)", paragraph).group(1))

    # Print the extracted information
    print(f"Number of amino acids: {aa_count}")
    print(f"Molecular weight: {mw}")
    print(f"Theoretical pI: {pi}")

    # Extract the amino acid composition using regular expressions
    aa_composition = {}
    aa_pattern = r"([A-Z][a-z]{2}) \(([A-Z])\) +(\d+) +([\d.]+)%"
    aa_matches = re.findall(aa_pattern, paragraph)
    for aa in aa_matches:
        aa_code = aa[1]
        aa_count = int(aa[2])
        aa_percentage = float(aa[3])
        aa_composition[aa_code] = {"percentage": aa_percentage}

    # Print the amino acid composition
    print("Amino acid composition:")
    for aa in aa_composition:
        print(f"{aa}: percentage = {aa_composition[aa]['percentage']}%")

    # Extract the important data using regular expressions
    total_neg_charged_res = 0
    total_pos_charged_res = 0
    charge_pattern = r"Total number of (negatively|positively) charged residues \((Asp|Glu|\+|Arg|Lys)\): (\d+)"
    charge_matches = re.findall(charge_pattern, paragraph)
    for charge in charge_matches:
        if charge[0] == "negatively":
            total_neg_charged_res += int(charge[2])
        elif charge[0] == "positively":
            total_pos_charged_res += int(charge[2])

    # Print the total number of negatively charged and positively charged residues
    print(f"Total number of negatively charged residues (Asp + Glu): {total_neg_charged_res}")
    print(f"Total number of positively charged residues (Arg + Lys): {total_pos_charged_res}")

    # Extract the important data using regular expressions
    atom_composition = {}
    atom_pattern = r"([A-Z][a-z]*) +([A-Z]+) +(\d+)"
    atom_matches = re.findall(atom_pattern, paragraph)
    for atom in atom_matches:
        atom_name = atom[0]
        atom_symbol = atom[1]
        atom_count = int(atom[2])
        atom_composition[atom_name] = {"symbol": atom_symbol, "count": atom_count}

    # Print the atomic composition
    print(f"Atomic composition:")
    for atom in atom_composition:
        print(f"{atom_composition[atom]['symbol']} {atom_composition[atom]['count']}")

    # Extract the important data using regular expressions
    total_atoms_pattern = r"Total number of atoms: (\d+)"
    total_atoms_matches = re.findall(total_atoms_pattern, paragraph)
    total_atoms = int(total_atoms_matches[0])

    # Print the total number of atoms
    print(f"Total number of atoms: {total_atoms}")

    pattern = r"Ext\.? coeff(?:icient)?\s+(\d+\.\d+)\s+"

    # Search for matches in the text
    ext_coeff_matches = re.findall(pattern, paragraph)

    if ext_coeff_matches:
        print("Extinction coefficients found:")
        for match in ext_coeff_matches:
            print(match)
    else:
        print("No extinction coefficients found.")

    mammalian_reticulocytes_pattern = r"(\d+(?:\.\d+)?) hours \(mammalian reticulocytes, in vitro\)"
    mammalian_reticulocytes_match = re.search(mammalian_reticulocytes_pattern, paragraph)

    if mammalian_reticulocytes_match:
        mammalian_reticulocytes_half_life = float(mammalian_reticulocytes_match.group(1))
        print("The half-life in mammalian reticulocytes is:", mammalian_reticulocytes_half_life, "hours.")
    else:
        print("No half-life information found for mammalian reticulocytes.")

    instability_regex = r"instability index \(II\) is computed to be ([\d\.]+)"
    aliphatic_regex = r"Aliphatic index: ([\d\.]+)"
    gravy_regex = r"Grand average of hydropathicity \(GRAVY\): ([\d\.-]+)"

    # Extract values using regular expressions
    instability_match = re.search(instability_regex, paragraph)
    aliphatic_match = re.search(aliphatic_regex, paragraph)
    gravy_match = re.search(gravy_regex, paragraph)

    # Print results
    if instability_match:
        instability_index = float(instability_match.group(1))
        print(f"Instability index: {instability_index}")
    else:
        print("No instability index found.")

    if aliphatic_match:
        aliphatic_index = float(aliphatic_match.group(1))
        print(f"Aliphatic index: {aliphatic_index}")
    else:
        print("No Aliphatic index found.")
    
    if gravy_match:
        gravy_match = float(gravy_match.group(1))
        print(f"Gravy Match: {gravy_match}")
    else:
        print("No Gravy Match found.")
    
df = pd.read_csv('./Data.csv')

df.columns[0]


url = "https://web.expasy.org/protparam/"
sequence = "FLPFQQFGRDIA"

driver = webdriver.Chrome(ChromeDriverManager().install())

wait = WebDriverWait(driver, 10)

driver.get('https://web.expasy.org/protparam/')

seq_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/form/textarea')))

seq_field.send_keys(sequence)


submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/form/p[1]/input[2]')))
submit_btn.click()

data_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sib_body"]/pre[2]')))

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

# print(soup)
#print(data_div.text)

extract_data(data_div.text)



