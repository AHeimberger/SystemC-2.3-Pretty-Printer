/**
* Description:	Connect Master and Memory - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		top.h
* Date:			20.03.2013
*/

#ifndef TOP_H_
#define TOP_H_

#include <systemc.h>
#include "master.h"
#include "memory.h"
#include "defines.h"

SC_MODULE(Top){
	// logic
    Master * master;
    Memory * memory;

	// signals
	sc_signal<bool>		ack;
	sc_signal<tData> 	data_master_to_mem;
	sc_signal<tData> 	data_mem_to_master;
	sc_signal<tAdr>		adr;
	sc_signal<bool>		we;
	sc_signal<bool>		cyc;
	sc_signal<bool>		stb;
	sc_signal<tSel>		sel;

	// clk
	sc_clock			clk;

	// Constructor with clk
    SC_CTOR(Top) : clk("clk", 10, SC_NS) {
		
		master = new Master("master");
		master->iClk(clk);
		master->iAck(ack);
		master->iData(data_mem_to_master);
		master->oData(data_master_to_mem);
		master->oAdr(adr);
		master->oWe(we);
		master->oCyc(cyc);
		master->oStb(stb);
		master->oSel(sel);

        memory = new Memory("memory");
		memory->iClk(clk);
		memory->oAck(ack);
		memory->iData(data_master_to_mem);
		memory->oData(data_mem_to_master);
		memory->iAdr(adr);
		memory->iWe(we);
		memory->iCyc(cyc);
		memory->iStb(stb);
		memory->iSel(sel);
    }

	~Top() {
		delete master;	master = 0;
		delete memory;	memory = 0;
	}

};

#endif