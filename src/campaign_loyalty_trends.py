#!/usr/bin/env python3

import csv
import sys

from collections import namedtuple
from decimal import Decimal, ROUND_HALF_UP
from operator import itemgetter


def bad_data(line):
    """
    Takes a line
    Checks id data is valid
    If valid it Removes all fields that are not being considered in this program
    refer: https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
    """
    if len(line) != 21:
        print(line, "invalid line. Not conforming to Data Dictionary. skipping...", file=sys.stderr)
        return True
    else:
        remove_ix = list(range(1, 7)) + [8, 9, 11, 12] + list(range(16, 21))
        for rm_ix in sorted(remove_ix, reverse=True):
            del line[rm_ix]  # removing all fields that are not being used
        return False


def emit(out_file, cmte_id, zip_code, year, perc_value, total, count):
    """
    Takes an output file and 6 values to emit
    emits all values in output '|' delimited
    """
    emit = [cmte_id, zip_code, year, perc_value, total, count]
    print(emit)
    with open(out_file, 'a', newline='') as f_out:
        out_writer = csv.writer(f_out, delimiter='|')
        out_writer.writerow(emit)


def finalize(donor_dict, donor_values, zip_five, percentile, out_file):
    """
    Takes a dictionary of qualifying repeated donors contributions, contribution values, 5 digit zip code,
    the percentile value and the output file.
    Qualifies repeated donors;
    For a qualifying donor it uses zip code to make a key. feeds dictionary, key, and qualifying donation into
    get_values() function.

    Feeds percentile into get_calcs() function.
    Feeds output file and emit values into emit() function.
    breaks loop for every qualifying contribution. 1 qualifying contribution -> 1 emit.
    """
    for donation in range(0, len(donor_values) - 1):
        ongoing = Donor(donor_values[-1][0], donor_values[-1][1], donor_values[-1][2])
        if len(donor_values) > 1 and ongoing.year > donor_values[donation][1]:  # Has donation in a prior year?
            donation_key = ongoing.cmte_id + '_' + zip_five + '_' + ongoing.year
            amount_list = get_values(donor_dict, donation_key, ongoing.transaction_amt)
            calc_out = get_calcs(amount_list, percentile)
            calc = Calc_names(calc_out[0], calc_out[1], calc_out[2])
            emit(out_file, ongoing.cmte_id, zip_five, ongoing.year, calc.perc_value, calc.total, calc.count)
            break


def get_calcs(list_of_amounts, percentile):
    """
    takes a list of transaction amounts and the percentile value
    returns the value at that percentile rank, total and count
    """
    float_amounts = [float(amount) for amount in list_of_amounts]
    float_amounts.sort()
    total = sum_floats_list(float_amounts, .01)
    rank_idx = round_up((percentile / 100) * len(float_amounts)) - 1  # -1 to get python index of rank
    perc_value = round_up(float_amounts[rank_idx])
    count = len(float_amounts)
    return perc_value, total, count


def get_values(dix, key, value):
    """
    takes a dictionary, key and value
    appends value to key
    returns all values of that key
    """
    if key not in dix:
        dix[key] = []
    dix[key].append(value)
    return dix[key]



def invalid_line(current):
    """
    Checks for malformed, invalid, or disqualifying data
    if valid, returns false
    """
    if not current.cmte_id:
        print(current, "invalid No CMTE_ID. skipping...", file=sys.stderr)
        return True
    elif not current.name or len(current.name) > 200:  # notice the change from if to elif
        print(current, "invalid NAME. skipping...", file=sys.stderr)
        return True
    elif len(current.zip_code) < 5 or len(current.zip_code) > 9:
        print(current, "invalid ZIP_CODE. skipping...", file=sys.stderr)
        return True
    elif len(current.transaction_dt) != 8:  # TODO: Is this sufficient for date check MMDDYYYY?
        print(current, "invalid TRANSACTION_DT. skipping...", file=sys.stderr)
        return True
    elif not current.transaction_amt or float(current.transaction_amt) <= 0:
        print(current, "invalid TRANSACTION_AMT. skipping...", file=sys.stderr)
        return True
    elif current.other_id:  # Contribution is from a candidate or another committee. skipping...
        return True

    return False


def round_up(num):
    """
    takes a float
    returns an integer that is rounded up if .50
    Rounding .5's up as per https://en.wikipedia.org/wiki/Percentile and challenge instructions
    regular python function round. rounds down from .5
    """
    return int(Decimal(num).quantize(0, ROUND_HALF_UP))


def sum_floats_list(f_list, place_form):
    """
    takes a list of floats, and place (i.e 1, .01 etc.)
    returns a float that is the sum limited to a decimal place
    Ensures output will not have trailing decimal numbers
    """
    place = str(place_form)
    return float(str(Decimal(sum(f_list)).quantize(Decimal(place))))


Donation = namedtuple('Donation', ['cmte_id', 'name', 'zip_code', 'transaction_dt', 'transaction_amt', 'other_id'])
Donor = namedtuple('Donor', ['cmte_id', 'year', 'transaction_amt'])
Calc_names = namedtuple('Calc', ['perc_value', 'total', 'count'])


def interface(in_file, percentile_file, out_file):
    open(out_file, 'w').close()  # Ensuring output file is clear at the start of the interface
    with open(percentile_file, 'r') as perc_file:
        percentile = int(perc_file.read())
    with open(in_file, 'r') as f:
        full_dict = {}
        repeat_donors = {}
        reader = csv.reader(f, delimiter='|')
        for i, line in enumerate(reader):
            if bad_data(line):
                continue
            current = Donation(line[0], line[1], line[2], line[3], line[4], line[5])
            if invalid_line(current):
                continue
            line[3] = current.transaction_dt[4:]  # Just the year
            zip_five = current.zip_code[:5]  # 5 digit zip
            full_key = current.name + '_' + zip_five
            trimd_line = list(itemgetter(0, 3, 4)(line))  # Only cmte_id, year, and transaction_amt
            donor_values = get_values(full_dict, full_key, trimd_line)
            finalize(repeat_donors, donor_values, zip_five, percentile, out_file)


def cli_interface():
    """
    cli wrapper to go from commandline to function
    """
    try:
        in_file, percentile_file, out_file = sys.argv[1:]
    except:
        print("usage: {}  <in_file> <percentile_file> <out_file>".format(sys.argv[0]))
        sys.exit(1)
    interface(in_file, percentile_file, out_file)


if __name__ == '__main__':
    cli_interface()
# TODO: Test different zip codes same name, same year
# TODO: test a 200+ character name
# TODO: See if you can implement month check day check , year check. maybe there is a date checking function
# TODO: Test a non 21 field line
# TODO: Check only one repeat, one output
# TODO: Test negative ammount
