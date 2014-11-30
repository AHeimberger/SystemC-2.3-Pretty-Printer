/**
* Description:	Memory Header File - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		memory.h
* Date:			20.03.2013
*/

#ifndef MEMORY_H_
#define MEMORY_H_

//#pragma warning (disable : 4996 4267 )

#define SC_INCLUDE_FX
#include <systemc.h>
#include "defines.h"

SC_MODULE(Memory) {
public:
	// Member
	sc_in<bool>			iClk;
	sc_out<bool>		oAck;
	sc_in<tData>		iData;
	sc_out<tData>		oData;
	sc_in<tAdr>			iAdr;
	sc_in<bool>			iWe;
	sc_in<bool>			iCyc;
	sc_in<bool>			iStb;
	sc_in<tSel>			iSel;

	// Memory process
	void memoryProcess();

	// Constructor with sensitivity list
	SC_CTOR(Memory): 
		iClk("clk"),
		oAck("ack"),
		iData("data_from_master"),
		oData("data_to_master"),
		iAdr("adr"),
		iWe("we"),
		iCyc("cyc"),
		iStb("stb"),
		iSel("sel") {

		SC_METHOD(memoryProcess);
		sensitive << iClk.neg();
		dont_initialize();

		// Init. memory
		for (int i = 0; i < cMemSize; i++) {
			mMemory[i] = 0;
		}
	}

private:
	// Memory
	tData mMemory[cMemSize];

	// Function creates a mask to use only selected bytes 
	// in memory and from incoming data
	tData createMask(tSel sel);
 };

#endif
