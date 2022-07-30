# See LICENSE.vyoma for details

import cocotb
import asyncio
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
import random
import time

# Round 0
@cocotb.test()
async def run_test(dut):
    """Round 1 Data Loss Check for cdc_fifo"""
    cocotb.log.info("####################################")
    cocotb.log.info("Round 1 Data Loss Check for cdc_fifo")
    cocotb.log.info("####################################")
    clock1 = Clock(dut.ffi_clk, 10, units="ns")
    clock2 = Clock(dut.ffo_clk, 14, units="ns")
    cocotb.start_soon(clock1.start())  # Start the clock1
    cocotb.start_soon(clock2.start())  # Start the clock2
    # Resetting the design
    cocotb.log.info("[INFO] Resetting the design ...")
    dut.ffi_rst.value = 1
    dut.ffo_rst.value = 1

    await FallingEdge(dut.ffi_clk)  # Synchronize with the clock
    await FallingEdge(dut.ffi_clk)  # Synchronize with the clock
    await FallingEdge(dut.ffo_clk)  # Synchronize with the clock
    await FallingEdge(dut.ffo_clk)  # Synchronize with the clock

    dut.ffi_rst.value = 0
    dut.ffo_rst.value = 0
    cocotb.log.info("[DONE] Reset design")

    FW = 3
    await RisingEdge(dut.ffi_clk)
    dut.ffi_vld.value = 1
    cocotb.log.info(f'ffi_rdy={dut.ffi_rdy.value}')
    val = []
    SC = 3
    RC = 1
    # Sending Packet first time
    for r in range (SC):
        cocotb.log.info(f"Sending packet {r} time")
        for i in range (5):
            await RisingEdge(dut.ffi_clk)
            if (dut.ffi_rdy.value & dut.ffi_vld.value):
                cocotb.log.info(f"======> Sending data")
                for wc in range (FW):
                    await RisingEdge(dut.ffi_clk)
                    cocotb.log.info(f'ffi_clk={dut.ffi_clk.value}; ffo_clk={dut.ffo_clk.value}')
                    val.append(random.randint(1, 8))
                    dut.ffi_bus.value = int(val[wc])  # Assign the random value val to the input port bus
                    cocotb.log.info(f"Data Packet={val[wc]}")
                    # cocotb.log.info(f"i_vld={dut.ffi_vld.value}; i_rdy={dut.ffi_rdy.value}; o_vld={dut.ffo_vld.value}; o_rdy={dut.ffo_rdy.value}; Received={dut.ffo_bus.value}")
                cocotb.log.info(f"======> Data Sent to FIFO")
                break
            else:
                cocotb.log.info(f'waiting for ffi_rdy...')
                cocotb.log.info(f"ffi_rdy is {dut.ffi_rdy.value}")

    """
    # Sending Packet second time
    cocotb.log.info(f"Sending packet second time")
    for i in range (5):
        await RisingEdge(dut.ffi_clk)
        if (dut.ffi_rdy.value & dut.ffi_vld.value):
            cocotb.log.info(f"======> Sending data")
            for wc in range (FW):
                await RisingEdge(dut.ffi_clk)
                cocotb.log.info(f'ffi_clk={dut.ffi_clk.value}; ffo_clk={dut.ffo_clk.value}')
                val.append(random.randint(1, 8))
                dut.ffi_bus.value = int(val[wc])  # Assign the random value val to the input port bus
                cocotb.log.info(f"Data Packet={val[wc]}")
                # cocotb.log.info(f"i_vld={dut.ffi_vld.value}; i_rdy={dut.ffi_rdy.value}; o_vld={dut.ffo_vld.value}; o_rdy={dut.ffo_rdy.value}; Received={dut.ffo_bus.value}")
            cocotb.log.info(f"======> Data Sent to FIFO")
            break
        else:
            cocotb.log.info(f'waiting for ffi_rdy...')
            cocotb.log.info(f"ffi_rdy is {dut.ffi_rdy.value}")
    """

    # Reading from Async FIFO
    for r in range (RC):
        cocotb.log.info(f"Receiving packet {r} time")
        cocotb.log.info(f'ffo_vld={dut.ffo_rdy.value}')
        dut.ffo_rdy.value = 1
        await RisingEdge(dut.ffo_clk)
        cocotb.log.info(f'ffo_vld={dut.ffo_vld.value}')
        dout = []
        for i in range (4):
            cocotb.log.info(f'ffo_rdy={dut.ffo_rdy.value}')
            await RisingEdge(dut.ffo_clk)
            dut.ffo_rdy.value = 1
            if (dut.ffo_vld.value & dut.ffo_rdy.value):
                cocotb.log.info(f"<====== Receiving data")
                for rc in range(FW):
                    await RisingEdge(dut.ffo_clk)
                    cocotb.log.info(f'ffi_clk={dut.ffi_clk.value}; ffo_clk={dut.ffo_clk.value}')
                    dout.append(dut.ffo_bus.value)
                    assert dout[rc] == val[rc], f"##########\n Data Mis-match\n##########"
                    cocotb.log.info(f"ffo_bus={int(dout[rc])}")
                cocotb.log.info(f"<====== Data Received from FIFO")
                break
            else:
                cocotb.log.info(f'waiting for ffo_vld...')
                cocotb.log.info(f'ffo_rdy={dut.ffo_rdy.value}')
            
    # print(type(int(dout)))
    for i in range(FW):
        if (int(dout[i])) != val[i]:
            # raise TestFailure("Received incorrectg data")
            cocotb.log.info("************************")
            cocotb.log.info("Received incorrect data")
            cocotb.log.info(f"ffi_vld={dut.ffi_vld.value}; ffi_rdy={dut.ffi_rdy.value}; ffo_vld={dut.ffo_vld.value}; ffo_rdy={dut.ffo_rdy.value}; Received={int(dout[i])}; Expected={val[i]}")
            cocotb.log.info("************************")
        else:
            dut._log.info("Received correctly")
            cocotb.log.info(f"ffi_vld={dut.ffi_vld.value}; ffi_rdy={dut.ffi_rdy.value}; ffo_vld={dut.ffo_vld.value}; ffo_rdy={dut.ffo_rdy.value}; Received={int(dout[i])}; Expected={val[i]}")
