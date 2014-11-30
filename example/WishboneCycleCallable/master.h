/**
* Description:	Wishbone Master Header File - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		master.h
* Date:			20.03.2013
*/

#ifndef MASTER_H_
#define MASTER_H_

// #pragma warning (disable : 4996 4267 )

#define SC_INCLUDE_FX
#include <systemc.h>
#include "defines.h"

SC_MODULE(Master) {
public:
	// Member
	sc_in<bool>			iClk;
	sc_in<bool>			iAck;	
	sc_in<tData>		iData;
	sc_out<tData>		oData;
	sc_out<tAdr>		oAdr;
	sc_out<bool>		oWe;
	sc_out<bool>		oCyc;
	sc_out<bool>		oStb;
	sc_out<tSel>		oSel;

	// Master Process
	void masterProcess();

	// Constructor with sensitivity list
	SC_CTOR(Master): 
		iClk("clk"),
		iAck("ack"),
		iData("data_from_mem"),
		oData("data_to_mem"),
		oAdr("adr"),
		oWe("we"),
		oCyc("cyc"),
		oStb("stb"),
		oSel("sel") {

		SC_THREAD(masterProcess);
		sensitive << iClk.pos();
		dont_initialize();
    }

private:
	// Implementation
	tData singleRead(tSel sel, tAdr adr);
	bool singleWrite(tData data, tSel sel, tAdr adr);

	// Testcases
	void TestCase1_Write(unsigned int testData);
	void TestCase2_Read(unsigned int expectedData);
	void TestCase3_Random();
 };

#endif
