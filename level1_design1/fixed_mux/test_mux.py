# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random
import time


@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    cocotb.log.info('##########################################')
    cocotb.log.info('##### Mux Test [0]: Random Inputs ########')
    cocotb.log.info('##########################################')

    mux_inp_all = []
    mux_inr = []
    for n in range(32):
        num = f"mux_inp{n}"
        ran_val = random.randrange(0, 4)
        num = ran_val
        mux_inr.append(ran_val)
        mux_inp_all.append(num)

    # mux_inp_all = mux_inr

    dut.inp0.value = mux_inp_all[0]
    dut.inp1.value = mux_inp_all[1]
    dut.inp2.value = mux_inp_all[2]
    dut.inp3.value = mux_inp_all[3]
    dut.inp4.value = mux_inp_all[4]
    dut.inp5.value = mux_inp_all[5]
    dut.inp6.value = mux_inp_all[6]
    dut.inp7.value = mux_inp_all[7]
    dut.inp8.value = mux_inp_all[8]
    dut.inp9.value = mux_inp_all[9]
    dut.inp10.value = mux_inp_all[10]
    dut.inp11.value = mux_inp_all[11]
    dut.inp12.value = mux_inp_all[12]
    dut.inp13.value = mux_inp_all[13]
    dut.inp14.value = mux_inp_all[14]
    dut.inp15.value = mux_inp_all[15]
    dut.inp16.value = mux_inp_all[16]
    dut.inp17.value = mux_inp_all[17]
    dut.inp18.value = mux_inp_all[18]
    dut.inp19.value = mux_inp_all[19]
    dut.inp20.value = mux_inp_all[20]
    dut.inp21.value = mux_inp_all[21]
    dut.inp22.value = mux_inp_all[22]
    dut.inp23.value = mux_inp_all[23]
    dut.inp24.value = mux_inp_all[24]
    dut.inp25.value = mux_inp_all[25]
    dut.inp26.value = mux_inp_all[26]
    dut.inp27.value = mux_inp_all[27]
    dut.inp28.value = mux_inp_all[28]
    dut.inp29.value = mux_inp_all[29]
    dut.inp30.value = mux_inp_all[30]
    # dut.inp31.value = mux_inp_all[31]

    for s_val in range(31):
        cocotb.log.info(f"Test Case #{s_val}")
        dut.sel.value = s_val
        await Timer(2, units="ns")
        cocotb.log.info(f"inp{s_val}={bin(mux_inp_all[s_val])}\tsel={s_val}\tout={dut.out.value}")
        assert dut.out.value == mux_inr[
            s_val], f"Mux result is incorrect; inp{s_val}: dut.out.value = {dut.out.value} != {mux_inr[s_val]}"

    cocotb.log.info('##### Mux Test [0]: END ########')

@cocotb.test()
async def test_mux1(dut):
    """Test for mux"""

    cocotb.log.info('###############################################')
    cocotb.log.info('##### Mux Test [1]: Incremental Inputs ########')
    cocotb.log.info('###############################################')

    mux_inp_all = []
    mux_inr = []
    for n in range(32):
        for v in range(1,3):
            num = f"mux_inp{n}"
            mux_inr.append(v)
            mux_inp_all.append(v)

    # mux_inp_all = mux_inr

    dut.inp0.value = mux_inp_all[0]
    dut.inp1.value = mux_inp_all[1]
    dut.inp2.value = mux_inp_all[2]
    dut.inp3.value = mux_inp_all[3]
    dut.inp4.value = mux_inp_all[4]
    dut.inp5.value = mux_inp_all[5]
    dut.inp6.value = mux_inp_all[6]
    dut.inp7.value = mux_inp_all[7]
    dut.inp8.value = mux_inp_all[8]
    dut.inp9.value = mux_inp_all[9]
    dut.inp10.value = mux_inp_all[10]
    dut.inp11.value = mux_inp_all[11]
    dut.inp12.value = mux_inp_all[12]
    dut.inp13.value = mux_inp_all[13]
    dut.inp14.value = mux_inp_all[14]
    dut.inp15.value = mux_inp_all[15]
    dut.inp16.value = mux_inp_all[16]
    dut.inp17.value = mux_inp_all[17]
    dut.inp18.value = mux_inp_all[18]
    dut.inp19.value = mux_inp_all[19]
    dut.inp20.value = mux_inp_all[20]
    dut.inp21.value = mux_inp_all[21]
    dut.inp22.value = mux_inp_all[22]
    dut.inp23.value = mux_inp_all[23]
    dut.inp24.value = mux_inp_all[24]
    dut.inp25.value = mux_inp_all[25]
    dut.inp26.value = mux_inp_all[26]
    dut.inp27.value = mux_inp_all[27]
    dut.inp28.value = mux_inp_all[28]
    dut.inp29.value = mux_inp_all[29]
    dut.inp30.value = mux_inp_all[30]
    # dut.inp31.value = mux_inp_all[31]

    for s_val in range(31):
        cocotb.log.info(f"Test Case #{s_val}")
        dut.sel.value = s_val
        await Timer(2, units="ns")
        cocotb.log.info(f"inp{s_val}={bin(mux_inp_all[s_val])}\tsel={s_val}\tout={dut.out.value}\texp={bin(mux_inr[s_val])}")
        assert dut.out.value == mux_inr[
            s_val], f"Mux result is incorrect; inp{s_val}: dut.out.value = {dut.out.value} != {mux_inr[s_val]}"

    cocotb.log.info('##### Mux Test [0]: END ########')
