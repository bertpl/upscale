from dataclasses import dataclass


@dataclass(frozen=True)
class TileDimSpec:
    """
    A class to represent the specifications to which a tile dimension needs to adhere.
    e.g. if a tile dimension should be >=64 and <=256, and a multiple of 4, this class allows to specify that.
    """

    min_value: int
    max_value: int
    multiplier: int

    def __post_init__(self):
        if not self.is_valid(self.min_value):
            raise ValueError(f"min_value {self.min_value} must be a multiple of {self.multiplier}.")
        if not self.is_valid(self.max_value):
            raise ValueError(f"max_value {self.max_value} must be a multiple of {self.multiplier}.")

    def valid_values(self) -> list[int]:
        return [value for value in range(self.max_value + 1) if self.is_valid(value)]

    def is_valid(self, value: int) -> bool:
        return (self.min_value <= value <= self.max_value) and (value % self.multiplier == 0)

    def round_down(self, value: int) -> int:
        """
        Provides largest valid value such that rounded_value <= value, unless there is no
        smaller value that is valid, in which case it returns the min_value.
        """
        if self.is_valid(value):
            return value
        elif value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        else:
            return value - (value % self.multiplier)

    def round_up(self, value: int) -> int:
        """
        Provides smallest valid value such that rounded_value >= value, unless there is no
        larger value that is valid, in which case it returns the max_value.
        """
        if self.is_valid(value):
            return value
        elif value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        else:
            return value + self.multiplier - (value % self.multiplier)

    def next(self, value: int) -> int:
        """
        Provides next valid value for the given value. i.e. such that next_value > value, unless there is no larger
        value that is valid, in which case it returns the same value.
        """
        if self.is_valid(value):
            return self.round_up(value + 1)
        else:
            return self.round_up(value)

    def prev(self, value: int) -> int:
        """
        Provides previous valid value for the given value. i.e. such that prev_value < value, unless there is no smaller
        value that is valid, in which case it returns the same value.
        """
        if self.is_valid(value):
            return self.round_down(value - 1)
        else:
            return self.round_down(value)
