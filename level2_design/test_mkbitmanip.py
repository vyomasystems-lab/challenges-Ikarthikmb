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
# Sample Test - 1 : Constant input, Random instructions
#################################################################################
@cocotb.test()
def run_test1(dut):
    # clock
    cocotb.fork(clock_gen(dut.CLK))
    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
    cocotb.log.info('##################################################')
    cocotb.log.info("#### Sample Test - 1 ####")
    cocotb.log.info('##################################################')

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x0
    mav_putvalue_src3 = 0x0
    for r in range(5): 
	    # mpi6_0    =  random.choice(['0010011','0110011'])  #  T7 
	    mpi6_0    =  random.choice(['13','33'])  #  T7 
	    # mpi7_19   =  '0'.zfill(13)                         #  T13
	    mpi7_19   =  '0'.zfill(4)                         #  T13
	    # mpi21_24  =  '0'.zfill(4)                          #  T4 
	    mpi21_24  =  '0'.zfill(1)                          #  T4 
	    # mpi25_26 = '0'.zfill(4)       # T4 
	    # mpi25_31 = random.choice(['0000100', '0000101', '0010000', '0010100', '0100000', '0100100', '0110000', '0110100'])      # T7 
	    mpi25_31 = random.choice(['4', '5', '10', '14', '20', '24', '30', '34'])	# T7 
	    mav_putvalue_instr = int(mpi6_0 + mpi7_19 + mpi21_24 + mpi25_31)
	    cocotb.log.info(type(mav_putvalue_instr))
	    cocotb.log.info(hex(mav_putvalue_instr))

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
		    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} | {hex(expected_mav_putvalue)} | MATCHED ')
	    else:
		    cocotb.log.info(f'--------------------------------------------------------------------------')
		    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} | {hex(expected_mav_putvalue)} | NOT MATCHED ')
		    cocotb.log.info(f'--------------------------------------------------------------------------')

	    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
	    assert dut_output == expected_mav_putvalue, error_message
	

#################################################################################
# Sample Test - 2 : Constant input, Every Instructions
#################################################################################
@cocotb.test()
def run_test2(dut):
    # clock
    cocotb.fork(clock_gen(dut.CLK))
    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
    cocotb.log.info(f'                                                  ')
    cocotb.log.info('##################################################')
    cocotb.log.info("#### Sample Test - 2 ####")
    cocotb.log.info('##################################################')

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x0
    mav_putvalue_src3 = 0x0
    for r in range(5): 
	    # mpi6_0    =  random.choice(['0010011','0110011'])  #  T7 
	    mpi6_0    =  ['13','33']  #  T7 
	    # mpi7_19   =  '0'.zfill(13)                         #  T13
	    mpi7_19   =  '0'.zfill(4)                         #  T13
	    # mpi21_24  =  '0'.zfill(4)                          #  T4 
	    mpi21_24  =  '0'.zfill(1)                          #  T4 
	    # mpi25_26 = '0'.zfill(4)       # T4 
	    # mpi25_31 = random.choice(['0000100', '0000101', '0010000', '0010100', '0100000', '0100100', '0110000', '0110100'])      # T7 
	    mpi25_31 = ['4', '5', '10', '14', '20', '24', '30', '34']	# T7 
	    for items in mpi6_0:
		    for elements in mpi25_31:
			    mav_putvalue_instr = int(items + mpi7_19 + mpi21_24 + elements)
				
			    # cocotb.log.info(type(mav_putvalue_instr))
			    cocotb.log.info(f"Instruction: {hex(mav_putvalue_instr)}")

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
				    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} | {hex(expected_mav_putvalue)} | MATCHED ')
			    else:
				    cocotb.log.info('--------------------------------------------------')
				    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} | {hex(expected_mav_putvalue)} | NOT MATCHED ')
				    cocotb.log.info('--------------------------------------------------')
			    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
			    assert dut_output == expected_mav_putvalue, error_message


#################################################################################
# Sample Test - 3 : Variable input, all instructions
#################################################################################
@cocotb.test()
def run_test3(dut):
    # clock
    cocotb.fork(clock_gen(dut.CLK))
    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
    cocotb.log.info(f'                                                  ')
    cocotb.log.info('##################################################')
    cocotb.log.info("#### Sample Test - 3 ####")
    cocotb.log.info('##################################################')

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_src1 = 0x1
    mav_putvalue_src2 = 0x2
    mav_putvalue_src3 = 0x2
    for r in range(1): 
	    mpi2_0    =  '3'  #  T1 
	    mpi3_19   =  '0'.zfill(5)                         #  T13
	    mpi21_24  =  '0'.zfill(1)                          #  T4 
	    mpi25     = '0'
	    mpi26_31 = ['2', '10', '26']	# T6 
	    for elements in mpi26_31:
		    mav_putvalue_instr = int(mpi2_0 + mpi3_19 + mpi21_24 + mpi25 + elements)
		    # mav_putvalue_instr = int(items + mpi7_19 + mpi21_24 + elements)
			
		    # cocotb.log.info(type(mav_putvalue_instr))
		    cocotb.log.info(f"Instruction: {hex(mav_putvalue_instr)}")

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
			    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} == {hex(expected_mav_putvalue)} | MATCHED ')
		    else:
			    cocotb.log.info('--------------------------------------------------')
			    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} != {hex(expected_mav_putvalue)} | NOT MATCHED ')
			    cocotb.log.info('--------------------------------------------------')
		    error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
		    # assert dut_output == expected_mav_putvalue, error_message

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
    # input transaction
    mav_putvalue_src1 = 0x5
    mav_putvalue_src2 = 0x2
    mav_putvalue_src3 = 0x2
    mav_putvalue_instr = 0x101010B3

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

    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
    cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')

    # comparison
    if (dut_output == expected_mav_putvalue):
	    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} == {hex(expected_mav_putvalue)} | MATCHED ')
    else:
	    cocotb.log.info('--------------------------------------------------')
	    cocotb.log.info(f'DUT OUTPUT={hex(dut_output)} == {hex(expected_mav_putvalue)} | NOT MATCHED ')
	    cocotb.log.info('--------------------------------------------------')
    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    # assert dut_output == expected_mav_putvalue, error_message

#################################################################################
# Sample Test - 4 : Variable Input, Variable Instructions
#################################################################################
@cocotb.test()
def run_test4(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    for i in range (2**32):
	    mav_putvalue_src1 = i
	    mav_putvalue_src2 = i
	    mav_putvalue_src3 = i
	    mav_putvalue_instr = 0x101010B3

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
		    cocotb.log.info(f'DUT OUT:{hex(dut_output)} == EXPECTED: {hex(expected_mav_putvalue)} | MATCHED ')
	    else:
		    cocotb.log.info('--------------------------------------------------')
		    cocotb.log.info(f'DUT OUT:{hex(dut_output)} == EXPECTED: {hex(expected_mav_putvalue)} | NOT MATCHED ')
		    cocotb.log.info('--------------------------------------------------')
	    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
	    # assert dut_output == expected_mav_putvalue, error_message

#################################################################################
# Sample Test - 5 : Variable Input, Variable Instructions
#################################################################################
@cocotb.test()
def run_test5(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    for i in range (2**32):
	    mav_putvalue_src1 = i
	    mav_putvalue_src2 = i
	    mav_putvalue_src3 = i
	    mav_putvalue_instr = 0x101010B3

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
		    cocotb.log.info(f'DUT OUT:{hex(dut_output)} == EXPECTED: {hex(expected_mav_putvalue)} | MATCHED ')
	    else:
		    cocotb.log.info('--------------------------------------------------')
		    cocotb.log.info(f'DUT OUT:{hex(dut_output)} == EXPECTED: {hex(expected_mav_putvalue)} | NOT MATCHED ')
		    cocotb.log.info('--------------------------------------------------')
	    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
	    # assert dut_output == expected_mav_putvalue, error_message
