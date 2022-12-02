import argparse
import csv
import sys
from numpy import deg2rad, rad2deg
from ..datamodel import Run, Survey, Reference
from ..auto.autocor import autocor


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='MSA correction')
    parser.add_argument('FILE', type=argparse.FileType('r'), help='an input .CSV file')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='-', metavar='OUT', help='an output .CSV file')
    parser.add_argument('--soft-dni', action='store_true', help='')
    parser.add_argument('-fd', '--field-delimiter', default=',')
    args = parser.parse_args()
    is_dni_rigid = not args.soft_dni

    eprint(f'D&I rigid: {is_dni_rigid}')
    eprint(f'FILE: {args.FILE}')
    eprint(f'OUT: {args.output}')

    try:
        reader = csv.reader(args.FILE, delimiter=args.field_delimiter, quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in reader]
    except ValueError as e:
        eprint(f"mwdmsa: error: can't parse CSV file: {e}")
        exit(2)

    try:
        surveys = [Survey(md=row[0], gx=row[1], gy=row[2], gz=row[3], bx=row[4], by=row[5], bz=row[6]) for row in rows]
        reference = [Reference(row[7], row[8], deg2rad(row[9]), deg2rad(row[10]), deg2rad(row[11])) for row in rows]
    except IndexError:
        eprint(f"mwdmsa: error: invalid number of columns in CSV file")
        exit(2)

    run = Run(surveys, 0., is_dni_rigid, reference=reference)
    res = autocor(run)

    writer = csv.writer(args.output, delimiter=args.field_delimiter)
    dni_cs = res.dni_cs.toarray()
    dni_cs[-3:] = rad2deg(dni_cs[-3:])
    writer.writerow(dni_cs)

