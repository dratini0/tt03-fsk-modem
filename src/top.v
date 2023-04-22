/* Generated by Yosys 0.23 (git sha1 7ce5011c24b) */

module dratini0_fsk_modem_top(io_out, io_in);
  wire [5:0] \$1 ;
  wire [5:0] \$2 ;
  input [7:0] io_in;
  wire [7:0] io_in;
  output [7:0] io_out;
  wire [7:0] io_out;
  wire rx_clk;
  wire [9:0] rx_frequency;
  wire rx_frequency_invert;
  wire rx_in_;
  wire rx_out;
  wire rx_rst;
  wire rx_valid;
  wire [9:0] wg1_frequency;
  wire [9:0] wg1_out;
  wire [9:0] wg2_frequency;
  wire [9:0] wg2_out;
  assign \$2  = wg1_out[9:5] + wg2_out[9:5];
  rx rx (
    .clk(rx_clk),
    .frequency(10'h08f),
    .frequency_invert(1'h0),
    .in_(rx_in_),
    .out(rx_out),
    .rst(rx_rst),
    .valid(rx_valid)
  );
  wg1 wg1 (
    .clk(rx_clk),
    .frequency(10'h03f),
    .out(wg1_out),
    .rst(rx_rst)
  );
  wg2 wg2 (
    .clk(rx_clk),
    .frequency(10'h06d),
    .out(wg2_out),
    .rst(rx_rst)
  );
  assign \$1  = \$2 ;
  assign io_out[7:3] = \$2 [5:1];
  assign io_out[1] = rx_valid;
  assign io_out[0] = rx_out;
  assign io_out[2] = 1'h0;
  assign rx_in_ = io_in[3];
  assign rx_frequency_invert = 1'h0;
  assign wg2_frequency = 10'h06d;
  assign wg1_frequency = 10'h03f;
  assign rx_frequency = 10'h08f;
  assign rx_rst = io_in[1];
  assign rx_clk = io_in[0];
endmodule

module i_filter(rst, in_, out, clk);
  wire [31:0] \$1 ;
  wire [3:0] \$10 ;
  wire [26:0] \$100 ;
  wire [3:0] \$102 ;
  wire [27:0] \$104 ;
  wire [3:0] \$106 ;
  wire [28:0] \$108 ;
  wire [1:0] \$110 ;
  wire [29:0] \$112 ;
  wire [1:0] \$114 ;
  wire [30:0] \$116 ;
  wire [1:0] \$118 ;
  wire [4:0] \$12 ;
  wire [31:0] \$120 ;
  wire [3:0] \$14 ;
  wire [5:0] \$16 ;
  wire [3:0] \$18 ;
  wire [1:0] \$2 ;
  wire [6:0] \$20 ;
  wire [3:0] \$22 ;
  wire [7:0] \$24 ;
  wire [7:0] \$26 ;
  wire [8:0] \$28 ;
  wire [7:0] \$30 ;
  wire [9:0] \$32 ;
  wire [7:0] \$34 ;
  wire [10:0] \$36 ;
  wire [7:0] \$38 ;
  wire [2:0] \$4 ;
  wire [11:0] \$40 ;
  wire [7:0] \$42 ;
  wire [12:0] \$44 ;
  wire [7:0] \$46 ;
  wire [13:0] \$48 ;
  wire [7:0] \$50 ;
  wire [14:0] \$52 ;
  wire [7:0] \$54 ;
  wire [15:0] \$56 ;
  wire [7:0] \$58 ;
  wire [1:0] \$6 ;
  wire [16:0] \$60 ;
  wire [7:0] \$62 ;
  wire [17:0] \$64 ;
  wire [7:0] \$66 ;
  wire [18:0] \$68 ;
  wire [7:0] \$70 ;
  wire [19:0] \$72 ;
  wire [7:0] \$74 ;
  wire [20:0] \$76 ;
  wire [7:0] \$78 ;
  wire [3:0] \$8 ;
  wire [21:0] \$80 ;
  wire [7:0] \$82 ;
  wire [22:0] \$84 ;
  wire [7:0] \$86 ;
  wire [23:0] \$88 ;
  wire [7:0] \$90 ;
  wire [24:0] \$92 ;
  wire [3:0] \$94 ;
  wire [25:0] \$96 ;
  wire [3:0] \$98 ;
  reg [29:0] _x = 30'h00000000;
  wire [29:0] \_x$next ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  output [8:0] out;
  wire [8:0] out;
  input rst;
  wire rst;
  assign \$100  = \$96  + \$98 ;
  assign \$104  = \$100  + \$102 ;
  assign \$108  = \$104  + \$106 ;
  assign \$112  = \$108  + \$110 ;
  assign \$116  = \$112  + \$114 ;
  assign \$120  = \$116  + \$118 ;
  always @(posedge clk)
    _x <= \_x$next ;
  assign \$12  = \$8  + \$10 ;
  assign \$16  = \$12  + \$14 ;
  assign \$20  = \$16  + \$18 ;
  assign \$24  = \$20  + \$22 ;
  assign \$28  = \$24  + \$26 ;
  assign \$32  = \$28  + \$30 ;
  assign \$36  = \$32  + \$34 ;
  assign \$40  = \$36  + \$38 ;
  assign \$44  = \$40  + \$42 ;
  assign \$48  = \$44  + \$46 ;
  assign \$4  = in_ + \$2 ;
  assign \$52  = \$48  + \$50 ;
  assign \$56  = \$52  + \$54 ;
  assign \$60  = \$56  + \$58 ;
  assign \$64  = \$60  + \$62 ;
  assign \$68  = \$64  + \$66 ;
  assign \$72  = \$68  + \$70 ;
  assign \$76  = \$72  + \$74 ;
  assign \$80  = \$76  + \$78 ;
  assign \$84  = \$80  + \$82 ;
  assign \$88  = \$84  + \$86 ;
  assign \$8  = \$4  + \$6 ;
  assign \$92  = \$88  + \$90 ;
  assign \$96  = \$92  + \$94 ;
  assign \$1  = \$120 ;
  assign out = \$120 [8:0];
  assign \_x$next [29:1] = _x[28:0];
  assign \_x$next [0] = in_;
  assign \$2  = { 1'h0, _x[0] };
  assign \$6  = { _x[1], 1'h0 };
  assign \$10  = { 1'h0, _x[2], 2'h0 };
  assign \$14  = { 1'h0, _x[3], 2'h0 };
  assign \$18  = { _x[4], 3'h0 };
  assign \$22  = { _x[5], 3'h0 };
  assign \$26  = { 3'h0, _x[6], 4'h0 };
  assign \$30  = { 3'h0, _x[7], 4'h0 };
  assign \$34  = { 3'h0, _x[8], 4'h0 };
  assign \$38  = { 2'h0, _x[9], 5'h00 };
  assign \$42  = { 2'h0, _x[10], 5'h00 };
  assign \$46  = { 2'h0, _x[11], 5'h00 };
  assign \$50  = { 2'h0, _x[12], 5'h00 };
  assign \$54  = { 2'h0, _x[13], 5'h00 };
  assign \$58  = { 2'h0, _x[14], 5'h00 };
  assign \$62  = { 2'h0, _x[15], 5'h00 };
  assign \$66  = { 2'h0, _x[16], 5'h00 };
  assign \$70  = { 2'h0, _x[17], 5'h00 };
  assign \$74  = { 2'h0, _x[18], 5'h00 };
  assign \$78  = { 2'h0, _x[19], 5'h00 };
  assign \$82  = { 3'h0, _x[20], 4'h0 };
  assign \$86  = { 3'h0, _x[21], 4'h0 };
  assign \$90  = { 3'h0, _x[22], 4'h0 };
  assign \$94  = { _x[23], 3'h0 };
  assign \$98  = { _x[24], 3'h0 };
  assign \$102  = { 1'h0, _x[25], 2'h0 };
  assign \$106  = { 1'h0, _x[26], 2'h0 };
  assign \$110  = { _x[27], 1'h0 };
  assign \$114  = { 1'h0, _x[28] };
  assign \$118  = { 1'h0, _x[29] };
endmodule

module lut(out, in_);
  reg \$auto$verilog_backend.cc:2083:dump_module$1  = 0;
  wire \$1 ;
  wire [9:0] \$3 ;
  wire [9:0] \$5 ;
  wire [9:0] \$6 ;
  input [9:0] in_;
  wire [9:0] in_;
  output [9:0] out;
  reg [9:0] out;
  assign \$1  = ~ in_[9];
  assign \$5  = ~ \$6 ;
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$1 ) begin end
    (* full_case = 32'd1 *)
    casez (\$1 )
      1'h1:
          out = \$3 ;
      default:
          out = \$5 ;
    endcase
  end
  assign \$3  = { in_[8:0], 1'h0 };
  assign \$6  = { in_[8:0], 1'h0 };
endmodule

module \lut$1 (out, in_);
  reg \$auto$verilog_backend.cc:2083:dump_module$2  = 0;
  wire \$1 ;
  wire [9:0] \$3 ;
  wire [9:0] \$5 ;
  wire [9:0] \$6 ;
  input [9:0] in_;
  wire [9:0] in_;
  output [9:0] out;
  reg [9:0] out;
  assign \$1  = ~ in_[9];
  assign \$5  = ~ \$6 ;
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$2 ) begin end
    (* full_case = 32'd1 *)
    casez (\$1 )
      1'h1:
          out = \$3 ;
      default:
          out = \$5 ;
    endcase
  end
  assign \$3  = { in_[8:0], 1'h0 };
  assign \$6  = { in_[8:0], 1'h0 };
endmodule

module mixer(rst, in_, frequency, i, q, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$3  = 0;
  wire [10:0] \$1 ;
  wire \$10 ;
  wire [10:0] \$2 ;
  wire \$4 ;
  wire \$6 ;
  wire \$8 ;
  reg [9:0] _phase = 10'h000;
  wire [9:0] \_phase$next ;
  input clk;
  wire clk;
  input [9:0] frequency;
  wire [9:0] frequency;
  output i;
  reg i;
  input in_;
  wire in_;
  output q;
  reg q;
  input rst;
  wire rst;
  assign \$10  = ~ $signed(in_);
  always @(posedge clk)
    _phase <= \_phase$next ;
  assign \$2  = _phase + frequency;
  assign \$4  = ~ $signed(in_);
  assign \$6  = ~ $signed(in_);
  assign \$8  = ~ $signed(in_);
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    (* full_case = 32'd1 *)
    casez (_phase[9:8])
      2'h0:
          i = in_;
      2'h1:
          i = in_;
      2'h2:
          i = \$4 ;
      2'h3:
          i = \$6 ;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    (* full_case = 32'd1 *)
    casez (_phase[9:8])
      2'h0:
          q = in_;
      2'h1:
          q = \$8 ;
      2'h2:
          q = \$10 ;
      2'h3:
          q = in_;
    endcase
  end
  assign \$1  = \$2 ;
  assign \_phase$next  = \$2 [9:0];
endmodule

module phase_detector(q, phase, i);
  reg \$auto$verilog_backend.cc:2083:dump_module$4  = 0;
  wire [9:0] \$1 ;
  wire \$10 ;
  wire \$13 ;
  wire \$15 ;
  wire \$17 ;
  wire [9:0] \$3 ;
  wire \$4 ;
  wire [9:0] \$7 ;
  wire [9:0] \$9 ;
  input [9:0] i;
  wire [9:0] i;
  output [2:0] phase;
  reg [2:0] phase;
  input [9:0] q;
  wire [9:0] q;
  assign \$10  = $signed(q) >= $signed(10'h000);
  assign \$9  = \$10  ? q : \$7 ;
  assign \$13  = $signed(\$3 ) > $signed(\$9 );
  assign \$15  = $signed(i) >= $signed(10'h000);
  assign \$17  = $signed(q) >= $signed(10'h000);
  assign \$1  = ~ $signed(i);
  assign \$4  = $signed(i) >= $signed(10'h000);
  assign \$3  = \$4  ? i : \$1 ;
  assign \$7  = ~ $signed(q);
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$4 ) begin end
    (* full_case = 32'd1 *)
    casez ({ \$17 , \$15 , \$13  })
      3'h7:
          phase = 3'h0;
      3'h6:
          phase = 3'h1;
      3'h4:
          phase = 3'h2;
      3'h5:
          phase = 3'h3;
      3'h1:
          phase = 3'h4;
      3'h0:
          phase = 3'h5;
      3'h2:
          phase = 3'h6;
      3'h3:
          phase = 3'h7;
    endcase
  end
endmodule

module phase_differentiator(rst, phase, out, valid, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$5  = 0;
  wire \$1 ;
  wire \$10 ;
  wire [10:0] \$12 ;
  wire [3:0] \$3 ;
  wire [3:0] \$4 ;
  wire [3:0] \$6 ;
  wire [3:0] \$7 ;
  wire [10:0] \$9 ;
  reg [2:0] _last_phase = 3'h0;
  wire [2:0] \_last_phase$next ;
  reg [9:0] _valid_counter = 10'h000;
  reg [9:0] \_valid_counter$next ;
  reg _valid_counter_reset;
  input clk;
  wire clk;
  output out;
  reg out = 1'h0;
  reg \out$next ;
  input [2:0] phase;
  wire [2:0] phase;
  input rst;
  wire rst;
  output valid;
  wire valid;
  assign \$10  = ~ valid;
  assign \$12  = _valid_counter + \$10 ;
  always @(posedge clk)
    _last_phase <= \_last_phase$next ;
  always @(posedge clk)
    out <= \out$next ;
  always @(posedge clk)
    _valid_counter <= \_valid_counter$next ;
  assign \$1  = _valid_counter == 10'h3ff;
  assign \$4  = phase - _last_phase;
  assign \$7  = phase - _last_phase;
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$5 ) begin end
    (* full_case = 32'd1 *)
    casez (\$3 [2:0])
      3'h0:
          _valid_counter_reset = 1'h0;
      3'h7:
          _valid_counter_reset = 1'h0;
      3'h1:
          _valid_counter_reset = 1'h0;
      default:
          _valid_counter_reset = 1'h1;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$5 ) begin end
    \out$next  = out;
    casez (\$6 [2:0])
      3'h0:
          /* empty */;
      3'h7:
          \out$next  = 1'h1;
      3'h1:
          \out$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$5 ) begin end
    (* full_case = 32'd1 *)
    casez (_valid_counter_reset)
      1'h1:
          \_valid_counter$next  = 10'h000;
      default:
          \_valid_counter$next  = \$12 [9:0];
    endcase
  end
  assign \$3  = \$4 ;
  assign \$6  = \$7 ;
  assign \$9  = \$12 ;
  assign \_last_phase$next  = phase;
  assign valid = \$1 ;
endmodule

module q_filter(rst, in_, out, clk);
  wire [31:0] \$1 ;
  wire [3:0] \$10 ;
  wire [26:0] \$100 ;
  wire [3:0] \$102 ;
  wire [27:0] \$104 ;
  wire [3:0] \$106 ;
  wire [28:0] \$108 ;
  wire [1:0] \$110 ;
  wire [29:0] \$112 ;
  wire [1:0] \$114 ;
  wire [30:0] \$116 ;
  wire [1:0] \$118 ;
  wire [4:0] \$12 ;
  wire [31:0] \$120 ;
  wire [3:0] \$14 ;
  wire [5:0] \$16 ;
  wire [3:0] \$18 ;
  wire [1:0] \$2 ;
  wire [6:0] \$20 ;
  wire [3:0] \$22 ;
  wire [7:0] \$24 ;
  wire [7:0] \$26 ;
  wire [8:0] \$28 ;
  wire [7:0] \$30 ;
  wire [9:0] \$32 ;
  wire [7:0] \$34 ;
  wire [10:0] \$36 ;
  wire [7:0] \$38 ;
  wire [2:0] \$4 ;
  wire [11:0] \$40 ;
  wire [7:0] \$42 ;
  wire [12:0] \$44 ;
  wire [7:0] \$46 ;
  wire [13:0] \$48 ;
  wire [7:0] \$50 ;
  wire [14:0] \$52 ;
  wire [7:0] \$54 ;
  wire [15:0] \$56 ;
  wire [7:0] \$58 ;
  wire [1:0] \$6 ;
  wire [16:0] \$60 ;
  wire [7:0] \$62 ;
  wire [17:0] \$64 ;
  wire [7:0] \$66 ;
  wire [18:0] \$68 ;
  wire [7:0] \$70 ;
  wire [19:0] \$72 ;
  wire [7:0] \$74 ;
  wire [20:0] \$76 ;
  wire [7:0] \$78 ;
  wire [3:0] \$8 ;
  wire [21:0] \$80 ;
  wire [7:0] \$82 ;
  wire [22:0] \$84 ;
  wire [7:0] \$86 ;
  wire [23:0] \$88 ;
  wire [7:0] \$90 ;
  wire [24:0] \$92 ;
  wire [3:0] \$94 ;
  wire [25:0] \$96 ;
  wire [3:0] \$98 ;
  reg [29:0] _x = 30'h00000000;
  wire [29:0] \_x$next ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  output [8:0] out;
  wire [8:0] out;
  input rst;
  wire rst;
  assign \$100  = \$96  + \$98 ;
  assign \$104  = \$100  + \$102 ;
  assign \$108  = \$104  + \$106 ;
  assign \$112  = \$108  + \$110 ;
  assign \$116  = \$112  + \$114 ;
  assign \$120  = \$116  + \$118 ;
  always @(posedge clk)
    _x <= \_x$next ;
  assign \$12  = \$8  + \$10 ;
  assign \$16  = \$12  + \$14 ;
  assign \$20  = \$16  + \$18 ;
  assign \$24  = \$20  + \$22 ;
  assign \$28  = \$24  + \$26 ;
  assign \$32  = \$28  + \$30 ;
  assign \$36  = \$32  + \$34 ;
  assign \$40  = \$36  + \$38 ;
  assign \$44  = \$40  + \$42 ;
  assign \$48  = \$44  + \$46 ;
  assign \$4  = in_ + \$2 ;
  assign \$52  = \$48  + \$50 ;
  assign \$56  = \$52  + \$54 ;
  assign \$60  = \$56  + \$58 ;
  assign \$64  = \$60  + \$62 ;
  assign \$68  = \$64  + \$66 ;
  assign \$72  = \$68  + \$70 ;
  assign \$76  = \$72  + \$74 ;
  assign \$80  = \$76  + \$78 ;
  assign \$84  = \$80  + \$82 ;
  assign \$88  = \$84  + \$86 ;
  assign \$8  = \$4  + \$6 ;
  assign \$92  = \$88  + \$90 ;
  assign \$96  = \$92  + \$94 ;
  assign \$1  = \$120 ;
  assign out = \$120 [8:0];
  assign \_x$next [29:1] = _x[28:0];
  assign \_x$next [0] = in_;
  assign \$2  = { 1'h0, _x[0] };
  assign \$6  = { _x[1], 1'h0 };
  assign \$10  = { 1'h0, _x[2], 2'h0 };
  assign \$14  = { 1'h0, _x[3], 2'h0 };
  assign \$18  = { _x[4], 3'h0 };
  assign \$22  = { _x[5], 3'h0 };
  assign \$26  = { 3'h0, _x[6], 4'h0 };
  assign \$30  = { 3'h0, _x[7], 4'h0 };
  assign \$34  = { 3'h0, _x[8], 4'h0 };
  assign \$38  = { 2'h0, _x[9], 5'h00 };
  assign \$42  = { 2'h0, _x[10], 5'h00 };
  assign \$46  = { 2'h0, _x[11], 5'h00 };
  assign \$50  = { 2'h0, _x[12], 5'h00 };
  assign \$54  = { 2'h0, _x[13], 5'h00 };
  assign \$58  = { 2'h0, _x[14], 5'h00 };
  assign \$62  = { 2'h0, _x[15], 5'h00 };
  assign \$66  = { 2'h0, _x[16], 5'h00 };
  assign \$70  = { 2'h0, _x[17], 5'h00 };
  assign \$74  = { 2'h0, _x[18], 5'h00 };
  assign \$78  = { 2'h0, _x[19], 5'h00 };
  assign \$82  = { 3'h0, _x[20], 4'h0 };
  assign \$86  = { 3'h0, _x[21], 4'h0 };
  assign \$90  = { 3'h0, _x[22], 4'h0 };
  assign \$94  = { _x[23], 3'h0 };
  assign \$98  = { _x[24], 3'h0 };
  assign \$102  = { 1'h0, _x[25], 2'h0 };
  assign \$106  = { 1'h0, _x[26], 2'h0 };
  assign \$110  = { _x[27], 1'h0 };
  assign \$114  = { 1'h0, _x[28] };
  assign \$118  = { 1'h0, _x[29] };
endmodule

module rx(rst, frequency, frequency_invert, in_, out, valid, clk);
  wire [9:0] \$1 ;
  wire [9:0] \$3 ;
  wire \$5 ;
  input clk;
  wire clk;
  input [9:0] frequency;
  wire [9:0] frequency;
  input frequency_invert;
  wire frequency_invert;
  wire i_filter_in_;
  wire [8:0] i_filter_out;
  input in_;
  wire in_;
  wire [9:0] mixer_frequency;
  wire mixer_i;
  wire mixer_in_;
  wire mixer_q;
  output out;
  wire out;
  wire [9:0] phase_detector_i;
  wire [2:0] phase_detector_phase;
  wire [9:0] phase_detector_q;
  wire phase_differentiator_out;
  wire [2:0] phase_differentiator_phase;
  wire phase_differentiator_valid;
  wire q_filter_in_;
  wire [8:0] q_filter_out;
  input rst;
  wire rst;
  output valid;
  wire valid;
  assign \$1  = i_filter_out - 8'hfc;
  assign \$3  = q_filter_out - 8'hfc;
  assign \$5  = phase_differentiator_out ^ frequency_invert;
  i_filter i_filter (
    .clk(clk),
    .in_(i_filter_in_),
    .out(i_filter_out),
    .rst(rst)
  );
  mixer mixer (
    .clk(clk),
    .frequency(mixer_frequency),
    .i(mixer_i),
    .in_(mixer_in_),
    .q(mixer_q),
    .rst(rst)
  );
  phase_detector phase_detector (
    .i(phase_detector_i),
    .phase(phase_detector_phase),
    .q(phase_detector_q)
  );
  phase_differentiator phase_differentiator (
    .clk(clk),
    .out(phase_differentiator_out),
    .phase(phase_differentiator_phase),
    .rst(rst),
    .valid(phase_differentiator_valid)
  );
  q_filter q_filter (
    .clk(clk),
    .in_(q_filter_in_),
    .out(q_filter_out),
    .rst(rst)
  );
  assign valid = phase_differentiator_valid;
  assign out = \$5 ;
  assign phase_differentiator_phase = phase_detector_phase;
  assign phase_detector_q = \$3 ;
  assign phase_detector_i = \$1 ;
  assign q_filter_in_ = mixer_q;
  assign i_filter_in_ = mixer_i;
  assign mixer_frequency = frequency;
  assign mixer_in_ = in_;
endmodule

module wg1(rst, frequency, out, clk);
  wire [10:0] \$1 ;
  wire [10:0] \$2 ;
  reg [9:0] _state = 10'h000;
  wire [9:0] \_state$next ;
  input clk;
  wire clk;
  input [9:0] frequency;
  wire [9:0] frequency;
  wire [9:0] lut_in_;
  wire [9:0] lut_out;
  output [9:0] out;
  wire [9:0] out;
  input rst;
  wire rst;
  assign \$2  = _state + frequency;
  always @(posedge clk)
    _state <= \_state$next ;
  lut lut (
    .in_(lut_in_),
    .out(lut_out)
  );
  assign \$1  = \$2 ;
  assign \_state$next  = \$2 [9:0];
  assign out = lut_out;
  assign lut_in_ = _state;
endmodule

module wg2(rst, frequency, out, clk);
  wire [10:0] \$1 ;
  wire [10:0] \$2 ;
  reg [9:0] _state = 10'h000;
  wire [9:0] \_state$next ;
  input clk;
  wire clk;
  input [9:0] frequency;
  wire [9:0] frequency;
  wire [9:0] lut_in_;
  wire [9:0] lut_out;
  output [9:0] out;
  wire [9:0] out;
  input rst;
  wire rst;
  assign \$2  = _state + frequency;
  always @(posedge clk)
    _state <= \_state$next ;
  \lut$1  lut (
    .in_(lut_in_),
    .out(lut_out)
  );
  assign \$1  = \$2 ;
  assign \_state$next  = \$2 [9:0];
  assign out = lut_out;
  assign lut_in_ = _state;
endmodule

