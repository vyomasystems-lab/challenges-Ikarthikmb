# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge, FallingEdge


# Test cases are tuned to identify 1011 out of 16 combinations
@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """
    clock = Clock(
        dut.clk, 10, units="us")  # Create a 10us period clock on port clk
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

    for i in range(16):
        b_val = format(i, '04b')
        for s in range(0, 4):
            await RisingEdge(dut.clk)
            dut.inp_bit.value = int(b_val[s])
        # await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        cocotb.log.info(f'{b_val} | seq_seen: {dut.seq_seen.value}')
        if ((int(b_val) == 1011) and dut.seq_seen.value):
            cocotb.log.info(f'----------------------------')
            cocotb.log.info("## Match Found")
            cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
            cocotb.log.info(f'----------------------------')
        elif (((int(b_val) == 1011) and ~dut.seq_seen.value) or ((int(b_val) != 1011) and dut.seq_seen.value)):
            cocotb.log.info(f'----------------------------')
            cocotb.log.info("## Bug Detected")
            cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
            cocotb.log.info(f'----------------------------')
        await RisingEdge(dut.clk)


@cocotb.test()
async def test_seq_bug2(dut):
    """Test for seq detection """
    clock = Clock(
        dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    # reset
    dut.reset.value = 1
    cocotb.log.info('[INFO] RESET ON SEQUENCE DETECTOR')
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    cocotb.log.info('[INFO] RESET OFF SEQUENCE DETECTOR')
    await FallingEdge(dut.clk)
    cocotb.log.info('#### CTB: Develop your test here! ######')
    dut.inp_bit.value = 0

    cocotb.log.info(f'----------------------------')
    cocotb.log.info('#### Test Scenario 2 ######')
    cocotb.log.info(f'----------------------------')

    for i in range(16):
        b_val = format(random.randrange(16), '04b')
        for s in range(0, 4):
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
        elif (((int(b_val) == 1011) and ~dut.seq_seen.value) or ((int(b_val) != 1011) and dut.seq_seen.value)):
            cocotb.log.info(f'----------------------------')
            cocotb.log.info("## Bug Detected")
            cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
            cocotb.log.info(f'----------------------------')
        await RisingEdge(dut.clk)
