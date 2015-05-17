/*
// build via:
g++ -I. -I$SYSTEMC_HOME/include -L. -L$SYSTEMC_HOME/lib-linux64 -Wl,-rpath=$SYSTEMC_HOME/lib-linux64 -o main main.cpp -g -O0 -lsystemc -lm
*/

#define SC_INCLUDE_FX
#include <systemc.h>
#include <iostream>

int sc_main( int, char*[]){

    // this method is used to turn off warnings for sc_bit which is deprecated
    sc_report_handler::set_actions("/IEEE_Std_1666/deprecated", SC_DO_NOTHING);

    // systemc datatypes
    sc_bit test1;
    test1 = '1';
    std::cout  << "sc_bit: " << test1 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_bv<40> test2 = "1100110011001100110011001100110011001100";
    std::cout  << "test2 sc_bv: " << test2 << std::endl << std::endl;

    sc_bv<40> test2_1 = "1000000000000000000000000000000000000000";
    std::cout  << "test2_1 sc_bv: " << test2_1 << std::endl << std::endl;

    sc_bv<32> test2_2 = "11001100110011001100110011001100";
    std::cout  << "test2_2 sc_bv: " << test2_2 << std::endl << std::endl;

    sc_bv<1> test2_3 = "1";
    std::cout  << "test2_3 sc_bv: " << test2_3 << std::endl << std::endl;


// -----------------------------------------------------------------------

    sc_logic test3;
    test3 = 'z';
    std::cout  << "sc_logic: " << test3 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_lv<4> test4 = "XZ01";
    std::cout  << "sc_lv: " << test4 << std::endl << std::endl;

    sc_lv<32> test4_1 = "XZXZ";
    std::cout  << "sc_lv: " << test4_1 << std::endl << std::endl;

    sc_lv<1> test4_2 = "X";
    std::cout  << "sc_lv: " << test4_2 << std::endl << std::endl;

    sc_lv<40> test4_3 = "X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0ZZZZ";
    std::cout  << "sc_lv: " << test4_3 << std::endl << std::endl;


// -----------------------------------------------------------------------

/*
    sc_signal_resolved test5;
    std::cout  << "sc_signal_resolved: " << test6 << std::endl;
    test6 = (sc_logic )'0';
    std::cout  << "sc_signal_resolved: " << test6 << std::endl;
    test6 = (sc_logic )'1';
    std::cout  << "sc_signal_resolved: " << test6 << std::endl  << std::endl;

    sc_signal_rv<4> test6;
    std::cout  << "sc_signal_rv: " << test6 << std::endl;
    test7 = "01XZ";
    std::cout  << "sc_signal_rv: " << test6 << std::endl  << std::endl;
*/

// -----------------------------------------------------------------------

    bool test7 = true;
    std::cout  << "bool: " << test7 << std::endl  << std::endl;

// -----------------------------------------------------------------------

    int test8 = 10;
    std::cout  << "int: " << test8 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_int<10> test9 = -100;
    std::cout  << "sc_int: " << test9 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_uint<64> test10 = -100;
    std::cout  << "sc_uint: " << test10 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_bigint<20> test11 = -1000;
    std::cout  << "sc_bigint: " << test11 << std::endl << std::endl;
    test11 += 1000;
    std::cout  << "sc_bigint: " << test11 << std::endl << std::endl;
    test11 += 1000;
    std::cout  << "sc_bigint: " << test11 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_biguint<64> test12 = 9223372036854775807;
    std::cout  << "sc_biguint: " << test12 << std::endl << std::endl;
    test12 += 9223372036854775807;
    std::cout  << "sc_biguint: " << test12 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_fixed<16, 5, SC_RND, SC_SAT> test13 = 10;
    std::cout << "test13 sc_fixed: " << test13 << std::endl << std::endl;

    sc_fixed<16, 5> test13_1 = 10.5;
    std::cout << "test13_1 sc_fixed: " << test13_1 << std::endl << std::endl;

    sc_fixed<16, 5> test13_2 = 15.25;
    std::cout << "test13_2 sc_fixed: " << test13_2 << std::endl << std::endl;

    sc_fixed<100, 50> test13_3 = 15121212.2512121212;
    std::cout << "test13_3 sc_fixed: " << test13_3 << std::endl << std::endl;

    sc_fixed<100, 0> test13_4 = 15121212.00002512121212;
    std::cout << "test13_4 sc_fixed: " << test13_4 << std::endl << std::endl;

    sc_fixed<100, 80> test13_5 = 15121212.2512121212;
    std::cout << "test13_5 sc_fixed: " << test13_5 << std::endl << std::endl;

    sc_fixed<100, 100> test13_6 = 15121212.2512121212;
    std::cout << "test13_6 sc_fixed: " << test13_6 << std::endl << std::endl;

    sc_fixed<100, 100> test13_7 = 1111111115121212.2512121212;
    std::cout << "test13_7 sc_fixed: " << test13_7 << std::endl << std::endl;

    sc_fixed<16, 5, SC_RND, SC_SAT> test13_8 = 0.5;
    std::cout << "test13_8 sc_fixed: " << test13_8 << std::endl << std::endl;

    sc_fixed<16, 5, SC_RND, SC_SAT> test13_9 = -0.5;
    std::cout << "test13_9 sc_fixed: " << test13_9 << std::endl << std::endl;

    sc_fixed<16, 5> test13_10 = -10.5;
    std::cout << "test13_10 sc_fixed: " << test13_10 << std::endl << std::endl;

    sc_fixed<16, 5> test13_11 = -15.25;
    std::cout << "test13_11 sc_fixed: " << test13_11 << std::endl << std::endl;


// -----------------------------------------------------------------------

    sc_ufixed<16, 4, SC_RND, SC_SAT> test14 = 10;
    std::cout << "test14 sc_ufixed: " << test14 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_fix test15 (16, 5, SC_RND, SC_SAT);
    test15 = 10;
    std::cout << "test15 sc_fix: " << test15 << std::endl << std::endl;

// -----------------------------------------------------------------------

    sc_ufix test16 (16, 4, SC_RND, SC_SAT);
    test16= 10;
    std::cout << "test16 sc_ufix: " << test16 << std::endl << std::endl;

// -----------------------------------------------------------------------

    float test17 = 14.4;
    std::cout << "test17 float: " << test17 << std::endl << std::endl;


    std::cout << "-----------------------------------------------" << std::endl;
    return 0;
}
