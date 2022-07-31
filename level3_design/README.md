# README-L3

# Asynchrnous FIFO Verification

The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![gitpod-l3-design.png](README-L3%2089eeddb12e40428ab4eb12759a597d09/gitpod-l3-design.png)

## **Verification environment**

The CoCoTb based Python test is developed as explained. The Design Under Test (here, the async fifo module) has 7 input ports, and the test monitors the 3 output ports.

The assert statement is used for comparing the output that is stored in `dout` list to the expected value which is stored in `val` list.

The following error is seen:

```verilog
assert dout[rc] == val[rc], f"##########\n Data Mis-match\n##########"
```

## Test Scenario #1

Goal: Functioning of the design by sending and receiving data packets

Testcase: run_test

Test Inputs:

| Input | Value |
| --- | --- |
| ffi_rdy | 1 |
| ffi_bus | [4,1,7] |
| ffi_vld | 1 |

| Output | Observed | Expected |
| --- | --- | --- |
| ffo_bus | [4,1,7] | [4,1,7] |

Test inputs may vary for every run since random is used to generate input values. 

Result: Received outputs with no bugs

## Test Scenario #2

Goal: Data loss check of the async fifo design

Testcase: run_test1

Test Inputs:

| Input | Value |
| --- | --- |
| ffi_rdy | 1 |
| ffi_bus | [4,3,3] |
| ffi_vld | 1 |

| Output | Observed | Expected |
| --- | --- | --- |
| ffo_bus | [4,3,3] | [4,3,3] |

Test inputs may vary for every run since random is used to generate input values. 

Result: Observed data once sent can not be modified unless the stored data in the FIFO reaches respective fanouts hence not allowing the reception of any new data. This checks the data integrity of the design.