using System;
using System.Diagnostics;

namespace Day16;

public class Day16 {
    private Day16() {}
    public static void Main(string[] args) {
        Console.WriteLine("Hello, World!");
        Tests.RunTests();

        var input = "A20D790042F1274011955491808B802F1C60B20030327AF2CC248AA800E7CDD726F3D78F4966F571A300BA54D668E2519249265160803EA9DE562A1801204ACE53C954ACE53C94C659BDF318FD1366EF44D96EB11005FB39154E0068A7C3A6B379646C80348A0055E6642B332109B8D6F0F12980452C9D322B28012EC72D51B300426CF70017996DE6C2B2C70C01A04B67B9F9EC8DAFE679D0992A80380104065FA8012805BD380120051E380146006380142004A00E920034C0801CA007B0099420053007144016E28018800CCC8CBB5FE79A3D91E1DC9FB151A1006CC0188970D6109803B1D61344320042615C198C2A014C589D00943096B3CCC081009173D015B004C401C8E10421E8002110BA18C193004A52257E0094BCE1ABB94C2C9005112DFAA5E80292B405927020106BC01494DFA6E329BF4DD273B69E233DB04C435BEF7A0CC00CFCDF31DC6AD20A3002A498CC01D00042229479890200E4438A91700010F88F0EA251802D33FE976802538EF38E2401B84CA05004833529CD2A5BD9DDAC566009CC33E8024200CC528E71F40010A8DF0C61D8002B5076719A5D418034891895CFD320730F739A119CB2EA0072D25E870EA465E189FDC1126AF4B91100A03600A0803713E2FC7D00043A25C3B8A12F89D2E6440242489A7802400086C788FB09C0010C8BB132309005A1400D2CBE7E7F2F9F9F4BB83803B25286DFE628E129EBCB7483C8802F3D0A2542E3004AC0169BD944AFF263361F1B48010496089807100BA54A66675769B1787D230C621EF8B9007893F058A009AE4ED7A5BBDBE05262CEC0002FC7C20082622E0020D0D66A2D04021D5003ED3D396E19A1149054FCA3586BD00020129B0037300042E0CC1184C000874368F70A251D840239798AC8DC9A56F7C6C0E0728015294D9290030B226938A928D0";
        Console.WriteLine(Packet.ParsePacket(input).SumVersions());
        Console.WriteLine(Packet.ParsePacket(input).Value());
    }
}

internal abstract class Packet {
    private const int LITERAL = 4;
    public int Version { get; protected set; }
    public int TypeId { get; protected set; }

    public static Packet ParsePacket(string s) {
        return ParsePacket(new Bitreader(s));
    }

    public static Packet ParsePacket(Bitreader br) {
        var version = br.take(3);
        var type_id = br.take(3);

        if (type_id == LITERAL) {
            return new LiteralPacket(version, br);
        } else {
            return new OperatorPacket(version, type_id, br);
        }
    }

    public abstract int SumVersions();
    public abstract long Value();
}

internal class LiteralPacket: Packet {
    private readonly long _value;
    public override long Value() { return (long)_value; }

    public LiteralPacket(int version, Bitreader bits) {
        Version = version;
        TypeId = 4; 

        long val = 0;
        var last_group = false;
        while (!last_group) {
            last_group = (bits.take(1) == 0);
            val <<= 4;
            val += bits.take(4);
        }
        Debug.Assert(val >= 0); // Verifies we haven't overrun the int size
        _value = val;
    }

    public override int SumVersions() { return Version; }
}

internal class OperatorPacket: Packet {
    private readonly List<Packet> _subPackets = new List<Packet>();
    public int NPackets { get { return _subPackets.Count; }}

    public OperatorPacket(int version, int type_id, Bitreader bits) {
        Version = version;
        TypeId = type_id;

        if (bits.take(1) == 0) {
            // The next 15 bits are a number showing remaining length in bits
            var bit_len = bits.take(15);
            var new_br = new Bitreader(bits, bit_len);
            while (new_br.Remaining > 6) {  // Slight hack to ignore remaining 0-pads (a valid packet will always have at least the version & type headers)
                _subPackets.Add(Packet.ParsePacket(new_br));
            }
            Debug.Assert(new_br.take(new_br.Remaining) == 0);
        } else {
            // The next 11 bits say how many packets are in this packet
            var n_packets = bits.take(11);
            for (var _i=0; _i<n_packets; _i++) {
                _subPackets.Add(Packet.ParsePacket(bits));
            }
        }
    }

    public override int SumVersions() {
        return Version + _subPackets.Sum(p => p.SumVersions());
    }

    public override long Value() {
        switch (TypeId) {
            case 0: // Sum packet
                return _subPackets.Sum(p => p.Value());
            case 1: // Product packet
                return _subPackets.Aggregate((long)1, (acc, p) => acc * p.Value());
            case 2: // Minimum
                return _subPackets.Select(p => p.Value()).Min();
            case 3: // Max
                return _subPackets.Select(p => p.Value()).Max();
            case 5: // Greater Than
                return _subPackets[0].Value() > _subPackets[1].Value() ? 1 : 0;
            case 6: // Less Than
                return _subPackets[0].Value() < _subPackets[1].Value() ? 1 : 0;
            case 7: // Equal
                return _subPackets[0].Value() == _subPackets[1].Value() ? 1 : 0;
            default:
                Debug.Assert(false, $"Invalid TypeId: {TypeId}");
                return -1;
        } 
    }
}

internal class Bitreader {
    private readonly Queue<byte> _vals = new Queue<byte>();

    public int Remaining { get { return _vals.Count; } }

    public Bitreader(byte[] bytes) {
        foreach (var b in bytes) {
            _vals.Enqueue(b);
        }
    }

    private static readonly Dictionary<char, byte[]> hexToBytes = new Dictionary<char, byte[]>() {
            {'0', new byte[] {0,0,0,0}},
            {'1', new byte[] {0,0,0,1}},
            {'2', new byte[] {0,0,1,0}},
            {'3', new byte[] {0,0,1,1}},
            {'4', new byte[] {0,1,0,0}},
            {'5', new byte[] {0,1,0,1}},
            {'6', new byte[] {0,1,1,0}},
            {'7', new byte[] {0,1,1,1}},
            {'8', new byte[] {1,0,0,0}},
            {'9', new byte[] {1,0,0,1}},
            {'A', new byte[] {1,0,1,0}},
            {'B', new byte[] {1,0,1,1}},
            {'C', new byte[] {1,1,0,0}},
            {'D', new byte[] {1,1,0,1}},
            {'E', new byte[] {1,1,1,0}},
            {'F', new byte[] {1,1,1,1}},
    };

    public Bitreader(string hex) {
        foreach (var c in hex.ToCharArray()) {
            foreach (var b in hexToBytes[c]) {
                _vals.Enqueue(b);
            }
        }
    }

    public Bitreader(Bitreader br, int n) {
        // Return a new bitreader created from the first n bits of this one
        for (var i=0; i<n; i++) {
            _vals.Enqueue((byte)br.take(1));
        }
    }

    public int take(int n) {
        var val = 0;
        for (var i=0; i<n; i++) {
            val <<= 1;
            val += _vals.Dequeue();
        }
        return val;
    }
}

public class Tests {
    public static void RunTests() {
        Console.WriteLine("Running tests...");
        BrTestFromBytes();
        BrTestFromHex();
        BrTestFromBr();
        TestLiteralPacket();
        TestOperatorPacket();
        TestVersionSums();
        TestValues();
        Console.WriteLine("...all passed");
    }

    private static void TestTemplate() {
        Console.Write(": ");
        Console.WriteLine("passed");
    }

    private static void BrTestFromBytes() {
        Console.Write("Bitreader TestFromBytes: ");
        var br = new Bitreader(new byte[] {1,1,0,0,1});
        Debug.Assert(br.Remaining == 5);
        Debug.Assert(br.take(3) == 6);
        Debug.Assert(br.Remaining == 2);
        Debug.Assert(br.take(2) == 1);
        Debug.Assert(br.Remaining == 0);
        Console.WriteLine("passed");
    }

    private static void BrTestFromHex() {
        Console.Write("Bitreader TestFromHex: ");
        var br = new Bitreader("D2FE28");
        Debug.Assert(br.take(3) == 6);
        Debug.Assert(br.take(3) == 4);
        Debug.Assert(br.take(5) == 23); // 1,0,1,1,1
        Debug.Assert(br.take(5) == 30); // 1,1,1,1,0
        Debug.Assert(br.take(5) == 5); // 0,0,1,0,1
        Debug.Assert(br.take(3) == 0);
        Debug.Assert(br.Remaining == 0);
        Console.WriteLine("passed");
    }

    private static void BrTestFromBr() {
        Console.Write("BrTestFromBr: ");
        var br1 = new Bitreader("F5");
        var br2 = new Bitreader(br1, 4);
        Debug.Assert(br2.take(4) == 15);
        Debug.Assert(br1.take(4) == 5);
        Console.WriteLine("passed");
    }

    private static void TestLiteralPacket() {
        Console.Write("TestLiteralPacket: ");
        var lit = (LiteralPacket) Packet.ParsePacket(new Bitreader("D2FE28"));
        Debug.Assert(lit.Version == 6);
        Debug.Assert(lit.TypeId == 4);
        Debug.Assert(lit.Value() == 2021);
        Console.WriteLine("passed");
    }

    private static void TestOperatorPacket() {
        Console.Write("TestOperatorPacket: ");
        var lit_one = (OperatorPacket) Packet.ParsePacket(new Bitreader("38006F45291200"));
        Debug.Assert(lit_one.NPackets == 2);
        var lit_two = (OperatorPacket) Packet.ParsePacket(new Bitreader("EE00D40C823060"));
        Debug.Assert(lit_two.NPackets == 3);
        Console.WriteLine("passed");
    }

    private static void TestVersionSums() {
        Console.Write("TestVersionSums: ");
        Debug.Assert(Packet.ParsePacket("8A004A801A8002F478").SumVersions() == 16);
        Debug.Assert(Packet.ParsePacket("620080001611562C8802118E34").SumVersions() == 12);
        Debug.Assert(Packet.ParsePacket("C0015000016115A2E0802F182340").SumVersions() == 23);
        Debug.Assert(Packet.ParsePacket("A0016C880162017C3686B18A3D4780").SumVersions() == 31);
        Console.WriteLine("passed");
    }

    private static void TestValues() {
        Console.Write("TestValues: ");
        Debug.Assert(Packet.ParsePacket("C200B40A82").Value() == 3); // Sum
        Debug.Assert(Packet.ParsePacket("04005AC33890").Value() == 54); // Product
        Debug.Assert(Packet.ParsePacket("880086C3E88112").Value() == 7); // Min
        Debug.Assert(Packet.ParsePacket("CE00C43D881120").Value() == 9); // Max
        Debug.Assert(Packet.ParsePacket("D8005AC2A8F0").Value() == 1); // LT
        Debug.Assert(Packet.ParsePacket("F600BC2D8F").Value() == 0); // GT
        Debug.Assert(Packet.ParsePacket("9C005AC2F8F0").Value() == 0); // EQ
        Debug.Assert(Packet.ParsePacket("9C0141080250320F1802104A08").Value() == 1); // 1+3==2*2
        Console.WriteLine("passed");
    }
}