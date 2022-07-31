# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/mux.v

TOPLEVEL := mux          # design
MODULE   := test_mux     # test
TESTCASE := test_mux # testcase
TESTCASE := test_mux1 # testcase

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 

