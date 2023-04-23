`default_nettype none
`timescale 10us/10us

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test.py
    input clk,
    input rst,
    input cs_n,
    input sck,
    input mosi,
    input data_in,
    input samples_in,

    output data_out,
    output valid_out,
    output [5:0] samples_out
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("test_fsk_modem_gl.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs = {samples_in, 1'b0, data_in, mosi, sck, cs_n, rst, clk};
    wire [7:0] outputs;
    assign {samples_out, valid_out, data_out} = outputs;

    // instantiate the DUT
    dratini0_fsk_modem_top dratini0_fsk_modem_top(
        `ifdef GL_TEST
            .vccd1( 1'b1),
            .vssd1( 1'b0),
        `endif
        .io_in  (inputs),
        .io_out (outputs)
        );

endmodule
