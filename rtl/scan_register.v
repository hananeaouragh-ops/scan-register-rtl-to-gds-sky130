module scan_register (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       scan_enable,
    input  wire       scan_in,
    input  wire       load,
    input  wire [7:0] data_in,
    output wire       scan_out,
    output reg  [7:0] q
);

assign scan_out = q[7];

always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        q <= 8'h00;
    else if (scan_enable)
        q <= {q[6:0], scan_in};
    else if (load)
        q <= data_in;
end

endmodule
