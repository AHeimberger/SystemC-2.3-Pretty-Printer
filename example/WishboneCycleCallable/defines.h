/**
* Description:	Definition File for Wires
* Author:		Markus Nabecker, Andreas Heimberger
* FileName:		defines.h
* Date:			20.03.2013
*/

#ifndef DEFINES_H_
#define DEFINES_H_

// Configuration of cycle callable timed simulation
//#define DEBUG
#define TRACE

// Constants for Bit Width
const int cAdrWidth		= 12;
const int cDataWidth	= 32;
const int cSelWidth		= 4;  // indicates valid data bytes
const int cMemSize		= 4096;

// Typedefs
typedef sc_lv<cDataWidth>	tData;
typedef sc_lv<cAdrWidth>	tAdr;
typedef sc_lv<cSelWidth>	tSel;

// Constants for Delays
const int cDelayMin		= 1;
const int cDelayMax		= 10;

// Size for Random TestCases
const int cNumberOfRandomTestCases = 1000000; 
const int cNumberOfDebugTestCases = 10;

#endif