# README-L1D2

# Sequence Detection Verification

The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![gitpod_setup_l1d2.jpeg](gitpod_setup_l1d2.jpeg)

## **Verification environment**

The CoCoTb based Python test is developed as explained. The test drives input to the Design Under Test (seqeunce detector here) which takes 1-bit inp_bit, 1-bit clk (clock), and 1-bit reset to detect the sequence 1011 which changes the seq_seen bit to 0b1.

The “if” condition is used for comparing the design output to the expected value.

The following message is seen:

```verilog
if ((int(b_val) == 1011) and dut.seq_seen.value):
  cocotb.log.info("## Match Found")
  cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
elif (((int(b_val) == 1011) and ~dut.seq_seen.value) or ((int(b_val) != 1011) and dut.seq_seen.value)):
  cocotb.log.info("## Bug Detected")
  cocotb.log.info(f'{b_val} | seq_seen={dut.seq_seen.value}')
```

## **Test Scenario #1**

**Description**

4-bit incremental input is applied with each clock cycle sending 1-bit to the DUT and the output is observed after 2-clock cycles.

**Test Inputs:** 0, 1, 2, 3, … 15

**Result:** The design is valid and no bugs were detected

## **Test Scenario #2**

**Description**

4-bit randomized input is applied with each clock cycle sending 1-bit to the DUT and the output is observed after 2-clock cycles.

**Test Inputs:** Random 4-bit values

**Result:** The design is valid and no bugs were detected