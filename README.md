# Table of Contents
1. [Challenge Description](README.md#challenge-description)
2. [Solution Approach](README.md#solution-approach)
3. [Tests](README.md#tests)
4. [Repo directory structure](README.md#repo-directory-structure)

# Challenge Description
https://github.com/InsightDataScience/donation-analytics

# Solution Approach
Python3 solution to the Insight Data Engineering Coding Challenge described above.

The entire solution is contained in `./src/campaign_loyalty_trends.py`. 5 python packages used `csv` `sys` `collections` `decimal` and `operator`.

Function descriptions are provided at the top of each function. This solution iterates the input line by line. Each qualifying line appends the output with one emit. Thus making this code streamable and able to feed into a running front-end interface.

All fields that are not considered from the input are removed at the start regardless of what they contain. Then each line goes through a series of qualifiers, computations are done on every qualifying line. 

It is recommended to keep ouput directory empty for any tests run through insight_testsuite. 

`/run.sh` wraps `./src/campaign_loyalty_trends.py`

# Tests

    all_invalid                  : Tests all disqualifiers. Produces no output
    diff_zip_cmte_id             : Tests different ZIP_CODE with everything same and CMTE_ID with everything same
    float_amounts                : Checks float TRANSACTION_AMT, to test summing, rounding, and percentile behavior 
    multiple_donation_diff_years : Multiple donations from different years, seeing how emitions add up
    one_repeat_one_emit          : One qualified, One emit.
    percentile_test              : Multiple 5 dollar donations to see if percentile behaves as expected as it moves through rank order.
    prior_calendar_year          : Checking if no prior calendar year qualifier.
    test_1                       : Default Test provided by Insight.

Excluded large test, due to large size. Specs:
* File Size: 358 MB
* 1,984,084 donation records processed
* Producing 125 Qualifying lines/emitions in 53.78 seconds with negligible memory use

## Repo directory structure

    .
    ├── README.md 
    ├── run.sh
    ├── src
    │   └── campaign_loyalty_trends.py
    ├── input
    │   └── README.md
    ├── output
    |   └── README.md
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            ├── test_1
            |   └── ... 
            ├── all_invalid
            |   └── ...
            ├── diff_zip_cmte_id
            |   └── ...
            ├── float_amounts
            |   └── ...
            ├── multiple_donation_diff_years
            |   └── ...
            ├── one_repeat_one_emit
            |   └── ...
            ├── percentile_test
            |   └── ...
            ├── prior_calendar_year
            |   └── ...
