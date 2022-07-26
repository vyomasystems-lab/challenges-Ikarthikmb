# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

#################################################################################
# Sample Default Test 
#################################################################################
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    ### Test values
    func3 = ["001" ,"010" ,"011" ,"100" ,"101" ,"110" ,"111"]
    # func3 = [hex(int("0b"+c,2))[2:] for c in func3]
    func7 = ["0000100" ,"0000101" ,"0010000" ,"0010100" ,"0100000" ,"0100100" ,"0110000" ,"0110100"]
    # func7 = [hex(int("0b"+c,2))[2:] for c in func7]
    func7_2bit = ["10" ,"11"]
    # func7_2bit = [hex(int("0b"+c,2))[2:] for c in func7_2bit]
    func7_fsri_1bit = 0
    func7_imm = ["00100" ,"00101" ,"01001" ,"01100" ,"01101"]
    # func7_imm = [hex(int("0b"+c,2))[2:] for c in func7_imm]
    func7_imm_SHFL = "000010"
    imm_value_1 = ["00000" ,"00001" ,"00010" ,"00100" ,"00101" ,"10000" ,"10001" ,"10010" ,"11000" ,"11001" ,"11010"]
    # imm_value_1 = [hex(int("0b"+c,2))[2:] for c in imm_value_1]
    opcode = ["0010011" ,"0110011"]
    # opcode = [hex(int("0b"+c,2))[2:] for c in opcode]

    # input transaction
    mav_putvalue_src1 = 0x2
    mav_putvalue_src2 = 0b11111111111111111111111111111111
    mav_putvalue_src3 = 0b00000000000000000000000000000011
    # mav_putvalue_instr = 0x101010B3
    #mav_putvalue_instr = random.choice(func7) + random.choice(imm_value_1) + "0".zfill(5) + random.choice(func3) + "0".zfill(5) + random.choice(opcode)
    #mav_putvalue_instr = int(hex(int("0b"+mav_putvalue_instr,2))[2:])
    # mav_putvalue_instr = int(random.choice(func7) + random.choice(imm_value_1) + "0".zfill(2) + random.choice(func3) + "0".zfill(2) + random.choice(opcode))
    mav_putvalue_instr = 0x40007033
    cocotb.log.info(type(mav_putvalue_instr))
    cocotb.log.info(f'mav_putvalue_instr={hex(int(mav_putvalue_instr))}')

    # expected output from the model
    expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

    # driving the input transaction
    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    dut.mav_putvalue_instr.value = mav_putvalue_instr

    yield Timer(1) 

    # obtaining the output
    dut_output = dut.mav_putvalue.value

    # cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')

    # comparison
    if (dut_output == expected_mav_putvalue):
	    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} == EXPECTED{hex(expected_mav_putvalue)} | MATCHED ')
    else:
	    cocotb.log.info('--------------------------------------------------')
	    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} != EXPECTED={hex(expected_mav_putvalue)} | NOT MATCHED ')
	    cocotb.log.info('--------------------------------------------------')
    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    # assert dut_output == expected_mav_putvalue, error_message

#################################################################################
# Sample Test1
#################################################################################
@cocotb.test()
def run_test2(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0b11111111111111111111111111111111
    mav_putvalue_src3 = 0b00000000000000000000000000000011
    # mav_putvalue_instr = 0x101010B3
    # mav_putvalue_instr = 0x40007033
    fp = open("inst_hex.txt", "r")
    for line in fp:
	    mav_putvalue_instr = int(line,16)
	    # cocotb.log.info(type(mav_putvalue_instr))
	    cocotb.log.info('--------------------------------------------------')
	    cocotb.log.info(f'mav_putvalue_instr={hex(int(mav_putvalue_instr))}')
	    cocotb.log.info(f'mav_putvalue_instr={bin(int(mav_putvalue_instr))}')
	    mpiv = bin(int(mav_putvalue_instr))
	    cocotb.log.info(f'{mpiv[2:6]} {mpiv[6:10]} {mpiv[10:14]} {mpiv[14:18]} {mpiv[18:22]} {mpiv[22:26]} {mpiv[26:30]} {mpiv[30:]}')

	    instr=hex(mav_putvalue_instr)[2:]
	    le=int(instr,16) #convert Hex  to int
	    le=bin(le)[2:] #convert int to binary
	    le=le.zfill(32)
	    length=len(le)
	    opcode = le[-7::]
	    func3 = le[length-15:length-12]
	    func7 = le[length-32:length-25]
	    func7_imm = le[length-32:length-27]
	    func7_2bit = le[length-27:length-25]
	    func7_1bit = le[length-28:length-27]
	    func7_fsri_1bit = le[length-27:length-26]
	    func7_imm_SHFL = le[length-32:length-26]
	    imm_value = le[length-25:length-20]
	    imm_value_1 = le[length-25:length-20]
	    fsr_imm_value = le[length-26:length-20]
	    fsr_imm_value=(int(str(fsr_imm_value),2))
	    imm_value=(int(str(imm_value),2))
	    shamt_imm= imm_value & (31)
	    shamt1= mav_putvalue_src2 & (31)

	    # expected output from the model
	    expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

	    # driving the input transaction
	    dut.mav_putvalue_src1.value = mav_putvalue_src1
	    dut.mav_putvalue_src2.value = mav_putvalue_src2
	    dut.mav_putvalue_src3.value = mav_putvalue_src3
	    dut.EN_mav_putvalue.value = 1
	    dut.mav_putvalue_instr.value = mav_putvalue_instr

	    yield Timer(1) 

	    # obtaining the output
	    dut_output = dut.mav_putvalue.value

	    # cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
	    # cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')

	    # comparison
	    if (dut_output == expected_mav_putvalue):
		    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} == EXPECTED={hex(expected_mav_putvalue)} | MATCHED ')
	    else:
		    cocotb.log.info(f'opcode={opcode}; func3={func3}; func7={func7}; func7_imm={func7_imm}; func7_2bit={func7_2bit}; func7_1bit={func7_1bit}; func7_fsri_1bit={func7_fsri_1bit}; func7_imm_SHFL={func7_imm_SHFL}; imm_value={imm_value}; imm_value_1={imm_value_1}; fsr_imm_value={fsr_imm_value}; fsr_imm_value={fsr_imm_value}; imm_value={imm_value}; shamt_imm={shamt_imm}; shamt1={shamt1}')
		    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} != EXPECTED={hex(expected_mav_putvalue)} | NOT_MATCHED ')
		    cocotb.log.info('**************************************************')
	    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
	    assert dut_output == expected_mav_putvalue, error_message
	    cocotb.log.info('--------------------------------------------------')
