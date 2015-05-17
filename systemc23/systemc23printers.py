#!/usr/bin/python3
# Pretty-printers for SystemC23
#
# This file was created to Pretty-Print Datatypes from SystemC.
# For more informations about Pretty-Printers see https://sourceware.org/gdb/wiki/STLSupport
#
# Copyright (C) 2014 Andreas Heimberger
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------------

import gdb
import numpy
import math
from decimal import *

class ScBit:
    """Print a sc_bit object."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "1" if str(self.val["m_val"]) == "true" else "0"


class ScBvBase:
    """Print a sc_bit object."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        outBin = "";
        length = int(self.val["m_len"])
        size = int(self.val["m_size"])
        mod = length % 32
        if (mod == 0):
            mod = 32

        for  i in range(size, 0, -1):
            data = numpy.uint32((self.val["m_data"] + (i-1) ).dereference())
            if i == size:
                outBin += str(bin(data)[2:(mod+2)].zfill(mod))
            else:
                outBin += str(bin(data)[2:(32+2)].zfill(32))

        return outBin


class ScLogic:
    """Print a sc_logic object."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        logic = int(self.val['m_val'])
        if logic is 0:
            out = "0"
        elif logic is 1:
            out = "1"
        elif logic is 2:
            out = "Z"
        elif logic is 3:
            out = "X"
        else:
            out ="UNEXPECTED VALUE OF TYPE SC_LOGIC"

        return out


class ScLV:
    """Print a sc_lv object."""
    def __init__(self, val):
        self.val = val

    def to_string(self):
        outLogic = "";
        length = int(self.val["m_len"])
        size = int(self.val["m_size"])
        mod = length % 32
        if (mod == 0):
            mod = 32

        for  i in range(size, 0, -1):
            data = numpy.uint32((self.val["m_data"] + (i-1) ).dereference())
            ctrl = numpy.uint32((self.val["m_ctrl"] + (i-1) ).dereference())

            constraint = 32
            if i == size:
                constraint = mod

            constant = 0
            for j in range(constraint, 0, -1):
                logic = 0
                constant = 1 << (j - 1)
                if (constant & data) == constant:
                    logic |= 1
                if (constant & ctrl) == constant:
                    logic |= 2

                if logic is 0:
                    outLogic += "0"
                elif logic is 1:
                    outLogic += "1"
                elif logic is 2:
                    outLogic += "Z"
                elif logic is 3:
                    outLogic += "X"
                else:
                    outLogic +="(UNEXPECTED VALUE OF TYPE SC_LOGIC)"

        return outLogic


class ScIntBase:
    """Print a sc_int object."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        length = self.val["m_len"]
        int64 = numpy.int64(self.val["m_val"]);
        return str(int64)


class ScUIntBase:
    """Print a sc_uint object."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        length = self.val["m_len"]
        uint64 = numpy.uint64(self.val["m_val"])
        return str(uint64)


class ScBigUInt_ScBigInt:
    """Print a sc_bigint object."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        output = ""
        sgn = int(self.val["sgn"])
        ndigits = int(self.val["ndigits"]);
        digit = self.val["digit"].dereference();
        for i in range(ndigits, 0, -1):
            data = numpy.uint32((self.val["digit"] + (i-1) ).dereference())
            output += str(bin(data)[2:].zfill(30))

        return str(sgn * int(output,2))


class ScUFixed_ScFixed_ScUFix_ScFix:
    """Print a sc_bigint object."""

    def __init__(self, val):
        self.val = val

    def to_string(self):
        wl = self.val["m_params"]["m_type_params"]["m_wl"]
        iwl = self.val["m_params"]["m_type_params"]["m_iwl"]
        q_mode = self.val["m_params"]["m_type_params"]["m_q_mode"]
        o_mode = self.val["m_params"]["m_type_params"]["m_o_mode"]
        n_bits = self.val["m_params"]["m_type_params"]["m_n_bits"]

        data = (self.val["m_rep"]).dereference()
        size = int((data["m_mant"]["m_size"]))
        sgn = int(data["m_sign"])
        state = int(data["m_state"])
        wp = int(data["m_wp"])
        msw = int(data["m_msw"])
        lsw = int(data["m_lsw"])
        r_flag = int(data["m_r_flag"])

        int_part = []
        frac_part = []
        for i in range(0, size):
            int_part.append( numpy.uint32((data["m_mant"]["m_array"] + i ).dereference()) )
            frac_part.append( numpy.uint32((data["m_mant"]["m_array"] + i ).dereference()) )

        for i in range(lsw, wp):
            if (i <= msw) and (i < wp):
                int_part[i] = 0

        int_is_zero = True
        if (state != 0):
            int_is_zero = False
        for i in range(0, size):
            if (int_part[i] != 0):
                int_is_zero = False

        if int_is_zero == False:
            for i in range(0, size):
                if (int_part[i] != 0):
                    frac_part[i] = 0;

        frac_is_zero = True
        if (state != 0):
            frac_is_zero = False
        for i in range(0, size):
            if (frac_part[i] != 0):
                frac_is_zero = False

        out_int = "0"
        if int_is_zero is False:
            for i in range(msw, (wp-1), -1):
                tmp = numpy.uint32(int_part[i])
                out_int += str(bin(tmp)[2:].zfill(32))

        bits_frac = int(wl - iwl)
        bits_mod = bits_frac % 32;
        bits_used = 0;

        out_frac = "0"
        if frac_is_zero is False:
            bytes_for_bits = math.ceil(bits_frac / 32)
            for i in range( (wp-1), (wp-1-bytes_for_bits), -1):
                tmp = numpy.uint32(frac_part[i])
                if i >= 0 and i != (wp-1-bytes_for_bits):
                    bits_used += 32;
                    out_frac += str(bin(tmp)[2:].zfill(32))
                if i == (wp-1-bytes_for_bits):
                    bits_used += bits_mod;
                    out_frac += str(bin(tmp)[2:].zfill(bits_mod))

        precision = 0
        if (bits_frac != 0):
            precision = Decimal(1.0) / Decimal(2) ** Decimal(bits_used)

        getcontext().prec = 100 ### hmmm whats the real length????
        frac = (Decimal(int(out_frac,2)) * Decimal(precision)).normalize()

        ret = ""
        if frac_is_zero is False:
            ret = "." + str(frac)[2:]

        if out_int is not "0":
            ret = str(Decimal(sgn) * Decimal(int(out_int, 2))) + ret

        if ret == "":
            return "0"

        return ret


def build_pretty_printer():
    systemc23 = gdb.printing.RegexpCollectionPrettyPrinter("SystemC23")
    systemc23.add_printer('sc_bit', 'sc_dt::sc_bit', ScBit)
    systemc23.add_printer('sc_bv_base', 'sc_dt::sc_bv<(.*)>', ScBvBase)
    systemc23.add_printer('sc_logic', 'sc_dt::sc_logic', ScLogic)
    systemc23.add_printer('sc_lv', 'sc_dt::sc_lv<(.*)>', ScLV)
    systemc23.add_printer('sc_int', 'sc_dt::sc_int<(.*)>', ScIntBase)
    systemc23.add_printer('sc_uint', 'sc_dt::sc_uint<(.*)>', ScUIntBase)
    systemc23.add_printer('sc_bigint', 'sc_bigint<(.*)>', ScBigUInt_ScBigInt)
    systemc23.add_printer('sc_biguint', 'sc_biguint<(.*)>', ScBigUInt_ScBigInt)
    systemc23.add_printer('sc_fixed', 'sc_fixed<(.*)>', ScUFixed_ScFixed_ScUFix_ScFix)
    systemc23.add_printer('sc_ufixed', 'sc_ufixed<(.*)>', ScUFixed_ScFixed_ScUFix_ScFix)
    systemc23.add_printer('sc_fix', 'sc_fix', ScUFixed_ScFixed_ScUFix_ScFix)
    systemc23.add_printer('sc_ufix', 'sc_ufix', ScUFixed_ScFixed_ScUFix_ScFix)
    return systemc23


def register_systemc23_printers(val):
    gdb.printing.register_pretty_printer(
        gdb.current_objfile(),
        build_pretty_printer())
