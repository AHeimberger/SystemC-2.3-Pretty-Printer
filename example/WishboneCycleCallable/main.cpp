/**
* Description:	Main Implementation - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		main.cpp
* Date:			20.03.2013
*/

#define SC_INCLUDE_FX
#include <systemc.h>
#include <ctime>
#include "top.h"

int sc_main( int, char*[]){

    Top top("top");    
	
#ifdef TRACE
    //Generate a VCD-Tracefile
    sc_trace_file *my_trace_file;
    my_trace_file = sc_create_vcd_trace_file("cycle_callable_trace");
	//my_trace_file->set_time_unit(1.0, SC_NS);

    //signals which should be traced
	sc_trace(my_trace_file, top.clk, "clk");
	sc_trace(my_trace_file, top.ack, "ack");
	sc_trace(my_trace_file, top.data_master_to_mem, "data_master_to_mem");
	sc_trace(my_trace_file, top.data_mem_to_master, "data_mem_to_master");
	sc_trace(my_trace_file, top.adr, "adr");
	sc_trace(my_trace_file, top.we, "we");
	sc_trace(my_trace_file, top.cyc, "cyc");
	sc_trace(my_trace_file, top.stb, "stb");
	sc_trace(my_trace_file, top.sel, "sel");
#endif

	// run stimuli 
    sc_start(200, SC_MS);	

#ifdef TRACE
	// close trace file
    sc_close_vcd_trace_file(my_trace_file);
#endif

	return 0;
}