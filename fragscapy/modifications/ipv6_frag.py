"""Fragments the IPv6 packets at the L3-layer."""

from fragscapy.modifications.mod import Mod
from fragscapy.modifications.utils import fragment6
from fragscapy.packetlist import PacketList


class Ipv6Frag(Mod):
    """Fragments the IPv6 packets at the L3-layer.

    Fragment each IPv6 packet. the fragmentation size must be specified. It
    represents the maximum size of each packet (including headers). It uses
    the scapy's fragmentation function.

    Args:
        *args: The arguments of the mods.

    Attributes:
        fragsize: The fragmentation size (maximum length of a fragment).

    Raises:
        ValueError: Unrecognized or incorrect number of parameters.

    Examples:
        >>> Ipv6Frag(1280).fragsize  # Minimum MTU for IPv6
        1280
    """

    name = "Ipv6Frag"
    doc = ("Fragments the IPv6 packets at the L3-layer\n"
           "ipv6_frag <size>")
    _nb_args = 1

    def parse_args(self, *args):
        """See base class."""
        try:
            self.fragsize = int(args[0])
        except ValueError:
            raise ValueError("Parameter 1 unrecognized. "
                             "Got {}".format(args[0]))

    def apply(self, pkt_list):
        """Fragment each IPv6 packet. See `Mod.apply` for more details."""
        new_pl = PacketList()

        for pkt in pkt_list:
            # Checks the packet length to avoid creating atomic fragments
            if pkt.pkt.haslayer('IPv6') and len(pkt.pkt) > self.fragsize:
                fragments = fragment6(pkt.pkt, self.fragsize)

                index = len(new_pl) - 1
                for fragment in fragments:
                    new_pl.add_packet(fragment)
                new_pl.edit_delay(index, pkt.delay)
            else:
                # Not IPv6 or too small so no fragmentation
                new_pl.add_packet(pkt.pkt, pkt.delay)

        return new_pl
