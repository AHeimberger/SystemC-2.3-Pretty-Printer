/**
* Description:	Implementation of the Wishbone Master - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		master.cpp
* Date:			20.03.2013
*/

#include "master.h"
#include <iostream>
#include <iomanip>

// retrieving time stamp counter of CPU
uint64_t ReadTSC(){
/*
	int dummy[4];				// for unused returns
	volatile int DontSkip;		// volatile to prevent optimizing
	sc_biguint<64> clock = 0;	// cycles 
	__cpuid(dummy, 0);			// serialize to prevent out-of-order-execution	
	DontSkip = dummy[0];		// prevent optimizing away cpuid

	clock = __rdtsc();			// read time stamp counter
	__cpuid(dummy, 0);			// serialize to prevent out-of-order-execution	
	DontSkip = dummy[0];		// prevent optimizing away cpuid
		
	return clock;				// cycles since cpu start
*/
	uint64_t a, d;
	__asm__ volatile ("rdtsc" : "=a" (a), "=d" (d));
	return (d<<32) | a;
}

// Master Process
void Master::masterProcess() {
	std::cout << "master process" << std::endl;

	// time measurement
	sc_biguint<64>  start = 0;
	sc_biguint<64>  diff = 0;
	sc_biguint<64>  startClk = 0;
	sc_biguint<64>  diffClk = 0;  
	int randNr = rand();

	// start measurement
	start = ReadTSC();
	startClk = clock();

	TestCase1_Write(randNr);
	TestCase2_Read(randNr);
	TestCase3_Random();

	// end measurement
	diffClk = clock() - startClk;
	diff = ReadTSC() - start;

	std::cout << "end of master process" << std::endl;

	std::cout << "At " << sc_time_stamp();
	std::cout << ", in delta cyles " << sc_delta_count() << std::endl;
	std::cout << "Duration: " << diffClk << " ms, in clock cycles: " << std::dec << diff << std::endl;
}


// Testcase 1: Write 'testData' into the whole memory
void Master::TestCase1_Write(unsigned int testData) {
	std::cout << "TestCase1 Write" << std::endl;

#ifdef DEBUG
	for(int i = 0; i < cNumberOfDebugTestCases; i++){
#else
	for(int i = 0; i < cMemSize; i++){
#endif
		singleWrite(testData, "1111", i);
	}

	std::cout << std::endl;
}


// Testcase 2: Read the whole memory and compair it with 'expectedData'
void Master::TestCase2_Read(unsigned int expectedData) {
	std::cout << "TestCase2 Read" << std::endl;

	tData dat = 0;

#ifdef DEBUG
	for(int i = 0; i < cNumberOfDebugTestCases; i++){
#else
	for(int i = 0; i < cMemSize; i++){
#endif
		dat = singleRead("1111", i);
		assert(dat == expectedData);
	}

	std::cout << std::endl;
}


// Testcase 3: Write and Read random Data to/from random address
void Master::TestCase3_Random() {
	std::cout << "TestCase3 Random" << std::endl;

	unsigned int randAddress = 0;
	unsigned int randData = 0;
	tData dat = 0;

#ifdef DEBUG
	for(int i = 0; i < cNumberOfDebugTestCases; i++){
#else
	for(int i = 0; i < cNumberOfRandomTestCases; i++){
#endif
		// random values for testcase
		randAddress = rand() % cMemSize;
		randData = rand();

		singleWrite(randData, 0xffffffff, randAddress);
		dat = singleRead("1111", randAddress);
		assert(dat == randData);
	}

	std::cout << std::endl;
}


// Implementation
tData Master::singleRead(tSel sel, tAdr adr) {

	wait(iClk.posedge_event());

	oAdr.write(adr);
	oWe.write(false);
	oSel.write(sel);
	oStb.write(true);
	oCyc.write(true);
	
	do{
		wait(iClk.posedge_event());
	}while(iAck.read() == false);

	oAdr.write("Z");
	oSel.write("Z");
	oWe.write(false);		
	oStb.write(false);
	oCyc.write(false);

#ifdef DEBUG
	std::cout << "Time: " << sc_time_stamp() << "\t ReadData:\t" << iData.read() << std::endl; 
#endif

	return iData.read();
}


bool Master::singleWrite(tData data, tSel sel, tAdr adr) {
	
	wait(iClk.posedge_event());
	
	oAdr.write(adr);
	oData.write(data);
	oWe.write(true);
	oSel.write(sel);
	oStb.write(true);
	oCyc.write(true);

	do{
		wait(iClk.posedge_event());
	}while(iAck.read() == false);

	oAdr.write("Z");
	oData.write("Z");
	oWe.write(false);
	oSel.write("Z");
	oStb.write(false);
	oCyc.write(false);

#ifdef DEBUG
	std::cout << "Time: " << sc_time_stamp() << "\t WriteData successfully @ " << adr.to_uint() << std::endl;
#endif

	return true;
}


