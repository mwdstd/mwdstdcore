import argparse
import csv
import sys
from numpy import deg2rad, rad2deg, concatenate
from ..datamodel import Run, Survey, Reference
from ..auto.autocor import autocor


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='MSA correction')
    parser.add_argument('FILE', type=argparse.FileType('r'), help='an input .CSV file')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='-', metavar='OUT', help='an output .CSV file')
    parser.add_argument('-ot', '--output-type', action='append', choices=['cs', 'qc', 'srv'], type=str)
    parser.add_argument('-s', '--separator', default='---', type=str)
    parser.add_argument('-nh', '--no-header', action='store_true')
    parser.add_argument('--soft-dni', action='store_true', help='')
    parser.add_argument('-fd', '--field-delimiter', default=',')
    parser.add_argument('-g', '--geomag', choices=['wmm', 'bggm', 'hdgm', 'ifr1'], default='bggm', help='Geomagnetic model')
    parser.add_argument('-v', '--verbose', action='store_true',)
    args = parser.parse_args()
    is_dni_rigid = not args.soft_dni
    if args.output_type is None:
        args.output_type = ['cs']

    if args.verbose:
        eprint(f'D&I rigid: {is_dni_rigid}')
        eprint(f'FILE: {args.FILE}')
        eprint(f'OUT: {args.output}')
        eprint(f'OUT_TYPE: {args.output_type}')

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
    res = autocor(run, args.geomag)

    separator = None
    for t in args.output_type:
        if separator is not None:
            args.output.write(separator)
            args.output.write('\n')
        separator = args.separator
        writer = csv.writer(args.output, delimiter=args.field_delimiter)
        if t == 'cs':
            dni_cs = res.dni_cs.toarray()
            dni_cs[-3:] = rad2deg(dni_cs[-3:])
            ref_cs = res.ref_cs.toarray()
            ref_cs[-1] = rad2deg(ref_cs[-1])
            if not args.no_header:
                writer.writerow(['ABX', 'ABY', 'ABZ', 'ASX', 'ASY', 'ASZ', 'MBX', 'MBY', 'MBZ', 'MSX', 'MSY', 'MSZ', 'MXY', 'MXZ', 'MYZ', 'dG', 'dB', 'dDip'])
            writer.writerow(concatenate([dni_cs, ref_cs]))
        elif t == 'srv':
            if not args.no_header:
                writer.writerow(['MD', 'Gx', 'Gy', 'Gz', 'Bx', 'By', 'Bz', 'Inc', 'Az'])
            for s, st in zip(res.surveys, res.stations):
                writer.writerow([s.md, s.gx, s.gy, s.gz, s.bx, s.by, s.bz, rad2deg(st.inc), rad2deg(st.az)])
            pass
        elif t == 'qc':
            if not args.no_header:
                writer.writerow(['ACC', 'SRV#', 'FSLB', 'EXP', 'REF QC'])
            writer.writerow([
                int(res.qa.accuracy.value), 
                int(res.qa.number_of_surveys.value), 
                int(res.qa.correction_possibility.value), 
                int(res.qa.model_comparison.value),
                int(res.qa.reference.value),
            ])

