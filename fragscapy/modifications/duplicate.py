"""Duplicates one of the packets."""

import random

from fragscapy.modifications.mod import Mod


class Duplicate(Mod):
    """Duplicates one of the packets.

    The duplicate is placed juste after the original one in the list. Can be
    either the first one, the last one, a random one or a specific one (by
    id).

    Args:
        *args: The arguments of the mods.

    Attributes:
        duplicate_index: The index to duplicate. None if random.

    Raises:
        ValueError: Unrecognized or incorrect number of parameters.

    Examples:
        >>> Duplicate("first").duplicate_index
        0
        >>> Duplicate(18).duplicate_index
        18
    """

    name = "Duplicate"
    doc = ("Duplicate one of the packets.\n"
           "duplicate {first|last|random|<id>}")
    _nb_args = 1

    def parse_args(self, *args):
        """See base class."""
        self.duplicate_index = None
        if args[0] == "first":
            self.duplicate_index = 0
        elif args[0] == "last":
            self.duplicate_index = -1
        elif args[0] == "random":
            pass  # Duplicate index will be calculated later
        else:
            try:
                self.duplicate_index = int(args[0])
            except ValueError:
                raise ValueError("Parameter 1 unrecognized. "
                                 "Got {}".format(args[0]))

    def is_deterministic(self):
        """See base class."""
        return self.duplicate_index is not None  # i.e. not random

    def apply(self, pkt_list):
        """Duplicates one packet. See `Mod.apply` for more details."""
        l = len(pkt_list)
        if not l:  # Avoid the trivial case
            return pkt_list

        i = self.duplicate_index

        if i is None:  # Random
            if l == 1:  # Avoid the case of randint(0, 0)
                i = 0
            else:
                i = random.randint(-l, l-1)

        if -l <= i <= l-1:
            duplicate_packet = pkt_list[i].pkt.copy()
            pkt_list.insert_packet(i, duplicate_packet)

        return pkt_list

    def get_params(self):
        """See base class."""
        return {k: v if v is not None else "random"
                for k, v in super(Duplicate, self).get_params().items()}
