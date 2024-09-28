import random
from typing import List


class DifferentialBonus:
    def __init__(self, ibo1: 'AmwayIBO', ibo2: 'AmwayIBO'):
        """
        Calculate the Differential Bonus between two IBOs.

        Args:
            ibo1 (AmwayIBO): The first IBO.
            ibo2 (AmwayIBO): The second IBO.
        """
        self.ibo1 = ibo1
        self.ibo2 = ibo2

    def __repr__(self):
        """
        Return a string representation of the Differential Bonus details.

        Returns:
            str: A string containing Differential Bonus details.
        """
        gpv_str = f"PV/BV: {self.ibo2.calculate_group_pv():.2f}/{self.ibo2.calculate_group_bv():.2f}\n"
        diff_bonus_str = f"Differential Bonus: {self.calculate_amount():.2f}\n"
        diff_multiplier_str = f"Differential Multiplier: {self.calculate_multiplier() * 100:.0f}% " \
                              f"({self.ibo1.calculate_bonus_percentage() * 100:.0f}% - {self.ibo2.calculate_bonus_percentage() * 100:.0f}%)\n"

        # Calculate the maximum width for the right-justified values
        max_width = max(len(diff_bonus_str), len(diff_multiplier_str), len(gpv_str))

        # Format the output with right-justified values
        gpv_str = f"PV/BV:".ljust(
            max_width) + f"{self.ibo2.calculate_group_pv():.2f}/{self.ibo2.calculate_group_bv():.2f}\n"
        diff_bonus_str = f"Differential Bonus:".ljust(
            max_width) + f"{self.calculate_amount():.2f}\n"
        diff_multiplier_str = f"Differential Multiplier:".ljust(
            max_width) + f"{self.calculate_multiplier() * 100:.0f}% " \
                         f"({self.ibo1.calculate_bonus_percentage() * 100:.0f}% - {self.ibo2.calculate_bonus_percentage() * 100:.0f}%)\n"

        return gpv_str + diff_multiplier_str + diff_bonus_str

    def calculate_multiplier(self) -> float:
        """
        Calculate the Differential Bonus multiplier.

        Returns:
            float: The Differential Bonus multiplier.
        """
        return max(0.0,
                   self.ibo1.calculate_bonus_percentage() - self.ibo2.calculate_bonus_percentage())

    def calculate_amount(self) -> float:
        """
        Calculate the Differential Bonus amount.

        Returns:
            float: The Differential Bonus amount.
        """
        return self.calculate_multiplier() * self.ibo2.calculate_group_pv() * AmwayIBO.BV_TO_PV_RATIO


class AmwayIBO:
    BONUS_SCHEDULE = {
        '0.03': {'min': 100, 'max': 299.99},
        '0.06': {'min': 300, 'max': 599.99},
        '0.09': {'min': 600, 'max': 999.99},
        '0.12': {'min': 1000, 'max': 1499.99},
        '0.15': {'min': 1500, 'max': 2499.99},
        '0.18': {'min': 2500, 'max': 3999.99},
        '0.21': {'min': 4000, 'max': 5999.99},
        '0.23': {'min': 6000, 'max': 7499.99},
        '0.25': {'min': 7500, 'max': float('inf')},
    }

    BV_TO_PV_RATIO = 3.36

    IBO_LEVELS = {
        'IBO': 0,
        'Silver Producer': 1,
        'Gold Producer': 2,
        'Platinum': 3,
        'Founders Platinum': 4,
        'Ruby': 5,
        'Founders Ruby': 6,
        'Sapphire': 7,
        'Founders Sapphire': 8,
        'Emerald': 9,
        'Founders Emerald': 10,
        'Diamond': 11,
        'Founders Diamond': 12,
        'Executive Diamond': 13,
        'Founders Executive Diamond': 14,
        'Double Diamond': 15,
        'Founders Double Diamond': 16,
        'Triple Diamond': 17,
        'Founders Triple Diamond': 18,
        'Crown': 19,
        'Founders Crown': 20,
        'Crown Ambassador': 21,
        'Founders Crown Ambassador': 8,
    }

    def __init__(self, sponsor=None, registration_month=1):
        """
        Initialize an AmwayIBO object.

        Args:
            sponsor (AmwayIBO, optional): The sponsor of this IBO. Defaults to None.
            registration_month (int, optional): The registration month of this IBO. Defaults to 1.
        """
        self.sponsor = sponsor
        self.registration_month = registration_month
        self.frontline = []  # List of AmwayIBO objects representing the frontlines
        self._personal_pv = 150  # Starting personal PV for every IBO is 150
        self._vcs_pv = 90  # Verified Customer Sales PV
        self.level = AmwayIBO.IBO_LEVELS['IBO']  # Default level is IBO for new IBOs

        if self.sponsor is not None:
            self.sponsor.add_frontline(self)

    @staticmethod
    def create_random_downline(ibo: 'AmwayIBO', month_number: int, frontline_count: int,
                               downline_count: int):
        """
        Create a random downline for the given IBO.

        Args:
            ibo (AmwayIBO): The IBO for which to create a random downline.
            month_number (int): The month number for the calculation.
            frontline_count (int): The number of IBOs to add to the frontline.
            downline_count (int): The number of IBOs to add randomly down the line.

        Returns:
            List[AmwayIBO]: A list of downline IBOs created randomly.
        """
        random.seed(month_number)  # Seed the random number generator for reproducibility

        downline_ibo_list = []

        # Add IBOs to the frontline
        for i in range(frontline_count):
            new_ibo = AmwayIBO(sponsor=ibo, registration_month=month_number)
            downline_ibo_list.append(new_ibo)

        # Add IBOs randomly down the line
        current_frontline = ibo.frontline.copy()
        for _ in range(downline_count):
            if not current_frontline:
                break

            random_frontline = random.choice(current_frontline)
            new_ibo = AmwayIBO(sponsor=random_frontline, registration_month=month_number)
            downline_ibo_list.append(new_ibo)

            current_frontline.extend(new_ibo.frontline)

        return downline_ibo_list

    def add_frontline(self, ibo):
        """
        Add an IBO to the frontline.

        Args:
            ibo (AmwayIBO): The IBO to add to the frontline.
        """
        self.frontline.append(ibo)

    def get_tree_structure(self, depth=0, last_frontline=False) -> str:
        """
        Get the tree structure of an IBO.

        Args:
            depth (int, optional): The depth of the IBO in the tree structure. Defaults to 0.
            last_frontline (bool, optional): True if the IBO is the last one in the frontline. Defaults to False.

        Returns:
            str: The tree structure of the IBO as a string.
        """
        indent = "│    " * depth
        branch = "└─ " if last_frontline else "├─ "
        info = f"{indent}{branch}[{int(self.calculate_bonus_percentage() * 100)}%] Group PV/BV: {self.calculate_group_pv():.2f}/{self.calculate_group_bv():.2f}, Personal PV/BV: {self._personal_pv:.2f}/{self.calculate_personal_bv():.2f}"
        for index, frontline in enumerate(self.frontline):
            last = index == len(self.frontline) - 1
            info += f"\n{frontline.get_tree_structure(depth + 1, last)}"
        return info

    def calculate_bonus_percentage(self) -> float:
        """
        Calculate the bonus percentage based on the total PV.

        Returns:
            float: The calculated bonus percentage.
        """
        total_pv = self.calculate_group_pv()
        bonus_percentage = 0.0  # Default bonus percentage if total PV is below the minimum threshold

        # Find the appropriate bonus percentage based on the total PV
        for percent, pv_range in AmwayIBO.BONUS_SCHEDULE.items():
            if pv_range["min"] <= total_pv <= pv_range["max"]:
                bonus_percentage = float(percent)
                break

        return bonus_percentage

    def calculate_group_pv(self) -> float:
        """
        Calculate the group PV (Point Value) of the IBO, which includes personal PV and frontline PV.

        Returns:
            int: The group PV of the IBO.
        """
        return self._personal_pv + sum(
            frontline.calculate_group_pv() for frontline in self.frontline)

    def calculate_group_bv(self) -> float:
        """
        Calculate the group BV (Business Volume) of the IBO, which is calculated based on group PV.

        Returns:
            float: The group BV of the IBO.
        """
        return self.calculate_group_pv() * AmwayIBO.BV_TO_PV_RATIO

    def calculate_personal_bv(self) -> float:
        """
        Calculate the personal BV (Business Volume) of the IBO.

        Returns:
            float: The personal BV of the IBO.
        """
        return self._personal_pv * AmwayIBO.BV_TO_PV_RATIO

    def calculate_personal_bonus(self) -> float:
        """
        Calculate the personal performance bonus.

        Returns:
            float: The calculated personal performance bonus.
        """
        if self._vcs_pv < 0.6 * self._personal_pv:
            raise ValueError(
                "VCS PV must be at least 60% of personal PV to qualify for the bonus.")

        return self.calculate_bonus_percentage() * self.calculate_personal_bv()

    @property
    def differential_bonus_list(self) -> List[DifferentialBonus]:
        """
        Get the list of DifferentialBonus objects for each personally sponsored downline.

        Returns:
            List[DifferentialBonus]: The list of DifferentialBonus objects.
        """
        return [DifferentialBonus(self, ibo) for ibo in self.frontline]

    def calculate_differential_bonus(self) -> float:
        """
        Calculate the total Differential Bonus amount for all personally sponsored downlines.

        Returns:
            float: The total Differential Bonus amount.
        """
        return sum(
            differential_bonus.calculate_amount() for differential_bonus in
            self.differential_bonus_list)

    def calculate_csi_percentage(self) -> float:
        """
        Calculate the Customer Sales Incentive (CSI) percentage.

        Returns:
            float: The calculated CSI percentage.
        """
        return max(0.0, 0.1 - self.calculate_bonus_percentage())

    def calculate_csi_bonus(self) -> float:
        """
        Calculate the Customer Sales Incentive (CSI) bonus amount.

        Returns:
            float: The calculated CSI bonus amount.
        """
        csi_percentage = self.calculate_csi_percentage()
        csi_bonus = csi_percentage * self._vcs_pv * AmwayIBO.BV_TO_PV_RATIO
        return min(csi_bonus, 75.0)  # Cap CSI bonus at $75 USD per month

    def calculate_retail_profit(self) -> float:
        """
        Calculate the retail profit for the IBO.

        Returns:
            float: The calculated retail profit.
        """
        return 0.1 * self._vcs_pv * AmwayIBO.BV_TO_PV_RATIO

    def calculate_total_earnings(self) -> float:
        """
        Calculate the total earnings from all bonuses and retail profit.

        Returns:
            float: The total earnings.
        """
        return (
                self.calculate_personal_bonus() +
                self.calculate_differential_bonus() +
                self.calculate_csi_bonus() +
                self.calculate_retail_profit()
        )

    def print_detailed_earnings(self):
        """
        Print detailed earnings data in a tabular format.

        The method prints the earnings data collected through the add_earnings_entry method
        in a tabular format with two columns: "Description" and "Amount".
        The "Amount" column is right-justified, aligning the numbers on the right edge (last digit).
        """

        headers = ["Earnings Type", "Amount ($)"]
        earnings_data = [
            ("Personal Bonus", self.calculate_personal_bonus()),
            ("Differential Bonus", self.calculate_differential_bonus()),
            ("CSI Bonus", self.calculate_csi_bonus()),
            ("Retail Profit", self.calculate_retail_profit()),
            ("Total Earnings", self.calculate_total_earnings())
        ]
        max_description_length = max(len(desc) for desc, _ in earnings_data)

        # Print title
        print("\nDetailed Earnings Breakdown")
        # Print separator
        print("-" * (max_description_length + 13))

        # Print header
        print(f"{headers[0]:<{max_description_length}} | {headers[1]:>10}")

        # Print separator
        print("-" * (max_description_length + 13))

        # Print data rows
        for description, amount in earnings_data:
            if description == "Total Earnings":
                # Print separator
                print("-" * (max_description_length + 13))
            print(f"{description:<{max_description_length}} | {amount:>10.2f}")

        print()




if __name__ == '__main__':
    # Input parameters for testing
    month_number = 12
    frontline_count = 20
    random_downline_count = 30

    # Month 1
    ibo1 = AmwayIBO(registration_month=month_number)

    # Generate random downline
    random_downline = AmwayIBO.create_random_downline(ibo1, month_number, frontline_count, random_downline_count)

    print("Tree Structure:")
    print(ibo1.get_tree_structure())

    ibo1.print_detailed_earnings()
