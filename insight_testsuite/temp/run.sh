#!/bin/bash
#

#for file in "/drives/c/Users/moosa/PycharmProjects/insight_data/campaign_loyalty_trends/loyalty_trends/insight_testsuite/tests"/*;do

#cd ${file}/../../..

python3 ./src/campaign_loyalty_trends.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt 2> /dev/null