#!/usr/bin/env python2.7

#    topas_tools - set of scripts to help using Topas
#    Copyright (C) 2015 Stef Smeets
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import re
import sys

__author__ = "Stef Smeets"
__email__ = "stef.smeets@mmk.su.se"


def pbpaste():
    """Mac only: paste text from clipboard"""
    outf = os.popen('pbpaste', 'r')
    content = outf.read()
    outf.close()
    return content


def equals_about(val, compare_to):
    return compare_to * 0.9 <= val <= compare_to*1.1


def main():
    if sys.argv > 0:
        text = open(sys.argv[1], "r").read()
    else:
        if sys.platform == "darwin":
            text = pbpaste()

    oto = 109.5
    tot = 145.0
    to = 1.61

    oto_vals = []
    tot_vals = []
    to_vals = []

    n_lines = 0
    n_oto = 0
    n_tot = 0
    n_to = 0

    for line in re.split('\r|\n', text):
        n_lines += 1

        line = line.strip()

        if line.startswith("'"):
            continue
        if "Restrain" not in line:
            continue
        if "Si" not in line:
            continue

        stuff, restraint, measured, box, weight = line.split(',')

        restraint = float(restraint)
        measured = float(measured.replace('`', '').split("_")[0])

        if equals_about(restraint, oto):
            oto_vals.append(measured)
            n_oto += 1
        elif equals_about(restraint, tot):
            tot_vals.append(measured)
            n_tot += 1
        elif equals_about(restraint, to):
            to_vals.append(measured)
            n_to += 1
        else:
            print line + ' -- FAIL'

    if not tot_vals:
        tot_vals = [0]
    if not to_vals:
        to_vals = [0]
    if not oto_vals:
        oto_vals = [0]

    print "Parsed {} lines".format(n_lines)
    print "{} restraints - tot: {}, oto: {}, to: {}".format(n_tot+n_oto+n_to, n_tot, n_oto, n_to)
    print ""
    print '        {:>10s} {:>10s} {:>10s} {:>10s} '.format('restraint', 'min', 'max', 'avg')
    print ' T-O-T  {:10.1f} {:10.3f} {:10.3f} {:10.3f} '.format(tot, min(tot_vals), max(tot_vals), sum(tot_vals)/len(tot_vals))
    print ' O-T-O  {:10.1f} {:10.3f} {:10.3f} {:10.3f} '.format(oto, min(oto_vals), max(oto_vals), sum(oto_vals)/len(oto_vals))
    print '   T-O  {:10.2f} {:10.3f} {:10.3f} {:10.3f} '.format(to, min(to_vals), max(to_vals), sum(to_vals)/len(to_vals))

if __name__ == '__main__':
    main()
