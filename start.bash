#!/bin/bash
touch useds.json
node index.js
python3 generateMergedTexts.py
python3 ./Normalization/occArray.py
python3 ./Normalization/calcEmbeddings.py
python3 ./Normalization/calcDistance.py