/**
* Description:	Implementation of the Memory - Wishbone_CycleCallable
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		memory.cpp
* Date:			20.03.2013
*/

#include "memory.h"
#include <iostream>

// Master Process
void Memory::memoryProcess() {

	static int cycleCnt = 0;
	static int randWaitStates = ((rand() % (cDelayMax-cDelayMin+1)) + cDelayMin);

	tData dataToWrite = "Z";

	oData.write(dataToWrite);
	oAck.write(false);	

	// only when following signals are set
	if ( iStb.read() == true && iCyc.read() == true) {	

		// read from memory
		if (iWe.read() == false) {
			tData dataTemp = mMemory[ iAdr.read().to_uint() ];
			tData maskTemp = createMask( iSel.read() );	

			dataToWrite = dataTemp & maskTemp;			
		}

		// write to memory
		else if (iWe.read() == true) {
			tData dataTemp = mMemory[ iAdr.read().to_uint() ];
			tData maskTemp = createMask( iSel.read() );

			dataTemp &= ~maskTemp;
			dataTemp |= ( iData.read() & maskTemp );					
				
			mMemory[ iAdr.read().to_uint() ] = dataTemp;					 
		}

		assert(randWaitStates > 0);
		if(cycleCnt == randWaitStates){
			// acknowledge line

			oData.write(dataToWrite);

			oAck.write(true);
			cycleCnt = -1;
			randWaitStates = ((rand() % (cDelayMax-cDelayMin+1)) + cDelayMin);
		}

		cycleCnt++;
	}		
}


// Function creates a mask to use only selected bytes 
// in memory and from incoming data
tData Memory::createMask(tSel sel) {
	tData maskTemp = 0x00000000;
	for (int i = 0; i < cSelWidth; i++) {
		
		maskTemp = maskTemp >> 8;		

		if ( sel.get_bit(i) == 1 ) {
			maskTemp = maskTemp | 0xFF000000;
		}		
	}

	return maskTemp;
}