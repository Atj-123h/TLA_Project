# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Module.
"""
import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
    پیاده‌سازی گیت‌های منطقی AND و NOT با استفاده از گلایدرها در Game of Life.

    سیگنال‌ها:
      - حضور گلایدر  = بیت 1
      - عدم حضور     = بیت 0

    AND Gate:
      گلایدر A (SE) از گوشه بالا-چپ و گلایدر B (SW) از بالا-راست حرکت می‌کنند.
      برخورد 90 درجه → دو بلوک ثابت 2×2 (خروجی 1)
      یک گلایدر تنها → از گرید خارج می‌شود (خروجی 0)

    NOT Gate:
      گلایدر کنترل (SE) همیشه شلیک می‌شود.
      اگر A=0: کنترل رد می‌شود (خروجی 1)
      اگر A=1: گلایدر A (NW) head-on با کنترل برخورد کرده، هر دو نابود می‌شوند (خروجی 0)
    """

    # شکل گلایدر استاندارد SE (پایین-راست):
    #  .X.
    #  ..X
    #  XXX
    _GLIDER_SE = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    # گلایدر SW (پایین-چپ) - آینه افقی SE:
    #  .X.
    #  X..
    #  XXX
    _GLIDER_SW = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

    # گلایدر NW (بالا-چپ) - برای head-on با SE:
    #  XXX
    #  X..
    #  .X.
    _GLIDER_NW = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1)]

    def setup_and_gate(self, grid_size=50, input_a_present=False, input_b_present=False):
        """
        راه‌اندازی گرید برای گیت AND.

        گلایدر A: SE از مختصات (2,2)
        گلایدر B: SW از مختصات (2,22)
        نقطه برخورد: حدود (12,12) - دو بلوک 2×2 ثابت تشکیل می‌شود

        Args:
            grid_size (int): اندازه گرید.
            input_a_present (bool): اگر True، گلایدر A قرار داده می‌شود.
            input_b_present (bool): اگر True، گلایدر B قرار داده می‌شود.

        Returns:
            GameOfLife: شیء بازی زندگی آماده‌شده.
        """
        GOL = GameOfLife(grid_size)

        if input_a_present:
            row_a, col_a = 2, 2
            for i, j in self._GLIDER_SE:
                GOL.grid[row_a + i, col_a + j] = 1

        if input_b_present:
            row_b, col_b = 2, 22
            for i, j in self._GLIDER_SW:
                GOL.grid[row_b + i, col_b + j] = 1

        return GOL

    def setup_not_gate(self, grid_size=40, input_a_present=False):
        """
        راه‌اندازی گرید برای گیت NOT.

        گلایدر کنترل: SE از (2,2) - همیشه وجود دارد
        گلایدر A:     NW از (28,28) - فقط وقتی A=1

        اگر A=0: کنترل بدون مانع رد می‌شود → خروجی 1
        اگر A=1: A و کنترل head-on برخورد کرده، هر دو نابود می‌شوند → خروجی 0

        Args:
            grid_size (int): اندازه گرید.
            input_a_present (bool): اگر True، گلایدر ورودی A قرار داده می‌شود.

        Returns:
            GameOfLife: شیء بازی زندگی آماده‌شده.
        """
        GOL = GameOfLife(grid_size)

        # گلایدر کنترل: همیشه وجود دارد
        for i, j in self._GLIDER_SE:
            GOL.grid[2 + i, 2 + j] = 1

        # گلایدر ورودی A: فقط اگر A=1
        if input_a_present:
            for i, j in self._GLIDER_NW:
                GOL.grid[28 + i, 28 + j] = 1

        return GOL

    def run_and_gate(self, input_a_present, input_b_present):
        """
        اجرای شبیه‌سازی AND gate و بازگشت خروجی.

        منطق تشخیص خروجی:
          - AND(1,1): دو گلایدر برخورد 90 درجه → دو بلوک ثابت 2×2 (8 سلول) → True
          - بقیه حالات: خروجی False (بدون نیاز به شبیه‌سازی)

        Args:
            input_a_present (bool): ورودی A.
            input_b_present (bool): ورودی B.

        Returns:
            bool: True اگر خروجی AND فعال باشد.
        """
        # حالات (0,0)، (1,0)، (0,1): طبق تعریف AND همیشه False
        if not (input_a_present and input_b_present):
            return False

        # حالت (1,1): شبیه‌سازی و بررسی تشکیل بلوک‌های ثابت
        GOL = self.setup_and_gate(50, input_a_present, input_b_present)
        for _ in range(60):
            GOL.evolve()

        final_population = np.sum(GOL.grid)
        # برخورد دو گلایدر SE و SW → دو بلوک 2×2 ثابت = 8 سلول
        return final_population >= 6

    def run_not_gate(self, input_a_present):
        """
        اجرای شبیه‌سازی NOT gate و بازگشت خروجی.

        منطق تشخیص خروجی:
          - NOT(0): گلایدر کنترل رد می‌شود → سلول‌هایی باقی می‌مانند → True
          - NOT(1): هر دو گلایدر نابود می‌شوند → 0 سلول → False

        Args:
            input_a_present (bool): ورودی A.

        Returns:
            bool: True اگر خروجی NOT فعال باشد.
        """
        GOL = self.setup_not_gate(40, input_a_present)
        for _ in range(60):
            GOL.evolve()

        final_population = np.sum(GOL.grid)
        # اگه سلولی باقی مانده = کنترل رد شده = خروجی 1
        # اگه 0 سلول = هر دو نابود شدند = خروجی 0
        return final_population > 0


if __name__ == "__main__":
    logic = GliderLogicGates()

    print("=== AND Gate Truth Table ===")
    for a in [False, True]:
        for b in [False, True]:
            result = logic.run_and_gate(a, b)
            a_str = "1" if a else "0"
            b_str = "1" if b else "0"
            r_str = "1" if result else "0"
            print(f"  A={a_str}, B={b_str} → {r_str}")

    print("\n=== NOT Gate Truth Table ===")
    for a in [False, True]:
        result = logic.run_not_gate(a)
        a_str = "1" if a else "0"
        r_str = "1" if result else "0"
        print(f"  A={a_str} → NOT(A)={r_str}")