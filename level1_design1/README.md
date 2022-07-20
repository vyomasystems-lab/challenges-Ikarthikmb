# Mux Desing Verification
The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![Setup](img/setup.png)

## Verification environment

The CoCoTb based Python test is developed as explained. The test drives inputs to the Design Under Test (Mux module here) which takes in 31 input ports (inp#) with each 2-bits, 4-bit select (sel) ports and results in 2-bit output port (out).

(Note: here inp# refers to the range from inp0,inp1 to inp30)

A random 2-bit value is assigned to each input port (inp#) and is tested for output based on sequential select (sel) cases. 

The assert statement is used for comparing the Mux output to the expected value.

The following error is seen:

```
assert dut.out.value ==  mux_inr[s_val],f"Mux result is incorrect; inp{s_val}: dut.out.value = {dut.out.value} != {mux_inr[s_val]}"
```

## Test Scenario #1

Test Inputs:

Inputs are all same either 00's or 01's or 10's or 11's 

Result: No change in the output and no bugs detected.


## Test Scenario #2

Random inputs

### Design Bug

The input output from the selection 12 should be inp12 instead inp13's output is observed due to error in bits selection.

```
// Design 
      5'b01101: out = inp12;
```

### Design Fix

Rectifying the error bits to 5'01100 which is case-12 shall resolve this issue.

```
// Correct assignment
      5'b01100: out = inp12;
```

## Test Scenario #3

Random inputs 

### Design Bug

The mux design consists of 5-bit selection pins which means 2^5(=32) actual selection pins are necessary instead 31 are available in the design.

### Design Fix

32 pin (i.e inp31) should be defined in the design

```
input [1:0] inp31;
```

> The updated design is checked in as mux_fix.v

## Verification Strategy

The goal of the verification is to test all the necessary inputs. While testing I noticed the inp12 was erraneous, whereas when the input signal are similar (either 0's or 1's or 01's or 10's) this bug could not be identified. Thus it is important to verify every test scenario.