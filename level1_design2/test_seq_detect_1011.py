# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
	"""Test for seq detection """
	clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
	cocotb.start_soon(clock.start())        # Start the clock
	# reset
	dut.reset.value = 1
	cocotb.log.info('### RESET ON SEQUENCE DETECTOR ### ')
	await FallingEdge(dut.clk)  
	dut.reset.value = 0
	cocotb.log.info('### RESET OFF SEQUENCE DETECTOR ###')
	await FallingEdge(dut.clk)
	cocotb.log.info('#### CTB: Develop your test here! ######')
	dut.inp_bit.value = 0

	cocotb.log.info(f'----------------------------')
	cocotb.log.info('#### Test Scenario 1 ######')
	cocotb.log.info(f'----------------------------')
	for i in range (16):
		b_val = format(i,'04b')
		for s in range (0,4):
			await RisingEdge(dut.clk)
			dut.inp_bit.value = int(b_val[s])
		await RisingEdge(dut.clk)
		await RisingEdge(dut.clk)
		cocotb.log.info(f'{b_val} | seq_seen: {dut.seq_seen.value}')
		if ((int(b_val) == 1011) and dut.seq_seen.value):
			cocotb.log.info(f'----------------------------')
			cocotb.log.info("## Match Found")
			cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
			cocotb.log.info(f'----------------------------')
		elif ((int(b_val) == 1011) and ~dut.seq_seen.value):
			cocotb.log.info(f'----------------------------')
			cocotb.log.info("## Bug Detected")
			cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
			cocotb.log.info(f'----------------------------')
		await RisingEdge(dut.clk)

@cocotb.test()
async def test_seq_bug2(dut):
	"""Test for seq detection """
	clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
	cocotb.start_soon(clock.start())        # Start the clock
	# reset
	dut.reset.value = 1
	cocotb.log.info('### RESET ON SEQUENCE DETECTOR ### ')
	await FallingEdge(dut.clk)  
	dut.reset.value = 0
	cocotb.log.info('### RESET OFF SEQUENCE DETECTOR ###')
	await FallingEdge(dut.clk)
	cocotb.log.info('#### CTB: Develop your test here! ######')
	dut.inp_bit.value = 0

	cocotb.log.info(f'----------------------------')
	await FallingEdge(dut.clk)
	cocotb.log.info('#### Test Scenario 2 ######')
	dut.inp_bit.value = 0
	for i in range (16):
		rv = random.randrange(0,16)
		b_val = format(rv,'04b')
		for s in range (0,4):
			await RisingEdge(dut.clk)
			dut.inp_bit.value = int(b_val[s])
		await RisingEdge(dut.clk)
		# await RisingEdge(dut.clk)
		cocotb.log.info(f'{"".join(str(i) for i in b_val).zfill(4)} | seq_seen: {dut.seq_seen.value}')
		if ((s==3) and (int(b_val) == 1011) and dut.seq_seen.value):
			cocotb.log.info(f'----------------------------')
			cocotb.log.info("## Match Found")
			cocotb.log.info(f'{b_val[s-3]}{b_val[s-2]}{b_val[s-1]}{b_val[s]} | seq_seen={dut.seq_seen.value}')
			cocotb.log.info(f'----------------------------')
		elif ((s==3) and (int(b_val) == 1011) and ~dut.seq_seen.value):
			cocotb.log.info(f'----------------------------')
			cocotb.log.info("## Bug Detected")
			cocotb.log.info(f'{b_val[s-3]}{b_val[s-2]}{b_val[s-1]}{b_val[s]} | seq_seen={dut.seq_seen.value}')
			cocotb.log.info(f'----------------------------')
		await RisingEdge(dut.clk)

	
@cocotb.test()
async def test_seq_bug3(dut):
	"""Test for seq detection """
	clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
	cocotb.start_soon(clock.start())        # Start the clock
	# reset
	dut.reset.value = 1
	cocotb.log.info('### RESET ON SEQUENCE DETECTOR ### ')
	await FallingEdge(dut.clk)  
	dut.reset.value = 0
	cocotb.log.info('### RESET OFF SEQUENCE DETECTOR ###')
	await FallingEdge(dut.clk)
	cocotb.log.info('#### CTB: Develop your test here! ######')
	dut.inp_bit.value = 0

	cocotb.log.info(f'----------------------------')
	cocotb.log.info('#### Test Scenario 3 ######')
	dut.inp_bit.value = 0
	d_seq = []
	for i in range (10):
		cv = 0
		while (cv < 4):
			b_val = random.randrange(0,2)
			await RisingEdge(dut.clk)
			d_seq.append(b_val)
			dut.inp_bit.value = d_seq[i]
			cv += 1
		cocotb.log.info(f'{"".join(str(i) for i in d_seq).zfill(31)} | seq_seen: {dut.seq_seen.value}')
		await RisingEdge(dut.clk)
		await RisingEdge(dut.clk)
		if (i >= 3):
			ovl = [d_seq[i-3],d_seq[i-2],d_seq[i-1],d_seq[i]]
			ovj = [str(i) for i in ovl]
			out_val = ("".join(ovj).zfill(4))
			if ((int(out_val) == 1011) and ~dut.seq_seen.value):
				cocotb.log.info(f'----------------------------')
				cocotb.log.info("## Bug Detected")
				cocotb.log.info(f'current sequence: {out_val} | seq_seen: {dut.seq_seen.value}')
				cocotb.log.info(f'----------------------------')
			elif ((int(out_val) == 1011) and dut.seq_seen.value):
				cocotb.log.info(f'----------------------------')
				cocotb.log.info("## Match Found")
				cocotb.log.info(f'current sequence: {out_val} | seq_seen: {dut.seq_seen.value}')
				cocotb.log.info(f'----------------------------')
		await RisingEdge(dut.clk)
