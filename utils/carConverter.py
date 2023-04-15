# use 
# convert file to car file and record json info

import os
import json
import subprocess
import argparse

DEAL_CLIENT = '0x99ec576ce2930BbE74b84739c27DCf28c2A370CC'

cwd = os.getcwd()

# go to GENERATE_CAR_PATH
GENERATE_CAR_PATH='/Users/admin/Projects/generate-car'

# input file path
FILE_PATH='/Users/admin/Downloads/personal/pfps/milady1119.png'

# output file path
OUTPUT_FILE_PATH='/Users/admin/Projects/langchain/utils/output.json'

# filecoin path
FILECOIN_PATH='/Users/admin/Projects/fevm-hardhat-kit'

command_text = '%s/generate-car --single -i %s -o %s/out -p %s' %(GENERATE_CAR_PATH, FILE_PATH, GENERATE_CAR_PATH, FILE_PATH)
print(command_text)

output = json.loads(os.popen(command_text).read())
print()
# print(output)

# 
text = \
'yarn hardhat make-deal-proposal --contract %s' %(DEAL_CLIENT) +\
' --piece-cid ' + output["PieceCid"]+\
' --piece-size %s' %(output["PieceSize"])+ \
' --verified-deal false' + \
' --label "' + output["PieceCid"] + '"' +\
' --start-epoch 520000' +\
' --end-epoch 1555200' +\
' --storage-price-per-epoch 0' +\
' --provider-collateral 0' + \
' --client-collateral 0 ' + \
' --extra-params-version 1' +\
' --location-ref "https://data-depot.lighthouse.storage/api/download/download_car?fileId=005b377e-89a6-44c6-aa04-871509019bec.car"' +\
' --car-size 194875' + \
' --skip-ipni-announce false' + \
' --remove-unsealed-copy false'

print()
print(text)

os.chdir(FILECOIN_PATH)
#print(os.getcwd())

#push_output = os.popen(text)
push_output = subprocess.Popen(text, shell=True)


parser = argparse.ArgumentParser(description="Filecoin car converter and uploader",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-gc", "--generate_car_path", default=GENERATE_CAR_PATH)
parser.add_argument("-f", "--file_path", default=FILE_PATH, help="file path for raw file to convert")
parser.add_argument("-o", "--output_file_path", default=OUTPUT_FILE_PATH,help="output file path")
parser.add_argument("-fevm", "--filecoin_evm_path", default=FILECOIN_PATH,help="path for the fevm-hardhat-kit")

args = parser.parse_args()
config = vars(args)
print(config)

"""
if os.path.isfile(OUTPUT_FILE_PATH):
    with open(OUTPUT_FILE_PATH, 'r') as file:
        exisiting_data = json.load(file)

    # append new data
    exisiting_data.append(output)

    # write to file
    with open(OUTPUT_FILE_PATH, 'w') as file:
        json.dump(exisiting_data, file)
        print(OUTPUT_FILE_PATH, " updated")

else:
    with open(OUTPUT_FILE_PATH, 'w') as file:
        json.dump(output, file)
        print("new output file written")
"""