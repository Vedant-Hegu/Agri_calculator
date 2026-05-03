import math
import statistics

class AgriBackend:
    def __init__(self):
        # --- Configuration Data ---
        self.FIXED_SAMPLE_COUNT = 50
        
        # Crop Weight Data (g per 50 seeds)
        self.CROP_DATA = {
            "Pavta (Lima Bean)": 13.0,
            "Matar (Green Pea)": 9.0,
            "Mung (Green Gram)": 2.3
        }

        # Historical Germination Rates (0.0 - 1.0)
        self.GERM_RATES = {
            "Pavta (Lima Bean)": 0.84,  # 84%
            "Matar (Green Pea)": 0.74,  # 74%
            "Mung (Green Gram)": 0.78   # 78%
        }

        # Crop Insights / Analysis Text
        self.INSIGHTS = {
            "Pavta (Lima Bean)": (
                "Seed = Pavta\n\n"
                "In case of Pavta, the optimum condition turned out to be in range of temperature range of 21°C to 23°C.\n\n"
                "Also, having the humidity in fixed range is beneficial.\n\n"
                "Moisture Control\n"
                "According to data generated, when soil moisture is controlled in the range 76% ± 5%, balancing this range for germination appeared to be beneficial."
            ),
            "Matar (Green Pea)": (
                "Seed = Matar\n\n"
                "Temperature and Humidity\n"
                "According to the graph, the seed showed germination of 86.60% when the temperature was not allowed to fluctuate beyond the range of 21°C to 23°C, and when temperature was fluctuating the germination rate was 60%.\n\n"
                "Moisture Control\n"
                "Consistent soil moisture helps to balance the fluctuation in other parameters. Overall, when soil moisture was controlled it showed germination rate of 73.33% and when there was no regulation over soil moisture germination rate was 60%."
            ),
            "Mung (Green Gram)": (
                "Seed = Mung\n\n"
                "Temperature and Humidity\n"
                "This was the only seed in which the germination success rate of temperature and humidity controlled showed to be 33.33% against the germination rate of no controlled parameter condition of 40%.\n\n"
                "Moisture Control\n"
                "According to the data, it was beneficial to control the soil moisture as it showed germination success rate of 53.33%."
            )
        }

        # Historical Comparison Data
        self.COMPARE_DATA = {
            "No Control": {
                "Pavta (Lima Bean)": {20:0, 21:0, 22:1, 23:1, 24:3, 25:2, 26:0, 27:0},
                "Matar (Green Pea)": {20:0, 21:0, 22:0, 23:1, 24:0, 25:4, 26:3, 27:1},
                "Mung (Green Gram)": {20:0, 21:0, 22:0, 23:0, 24:0, 25:2, 26:3, 27:1}
            },
            "Soil Controlled": {
                "Pavta (Lima Bean)": {20:0, 21:0, 22:2, 23:2, 24:4, 25:2, 26:0, 27:2},
                "Matar (Green Pea)": {20:0, 21:0, 22:0, 23:3, 24:2, 25:3, 26:1, 27:2},
                "Mung (Green Gram)": {20:0, 21:0, 22:0, 23:0, 24:2, 25:3, 26:1, 27:2}
            },
            "Humidity and Moisture Control": {
                "Pavta (Lima Bean)": {20:0, 21:0, 22:0, 23:3, 24:4, 25:2, 26:3, 27:1},
                "Matar (Green Pea)": {20:0, 21:0, 22:1, 23:2, 24:1, 25:3, 26:2, 27:2},
                "Mung (Green Gram)": {20:0, 21:0, 22:2, 23:0, 24:0, 25:1, 26:2, 27:0}
            }
        }

        # Monitoring Log Data
        self.MONITOR_DATA = {
            "time": ["04:46", "05:45", "06:44", "07:43", "08:42", "09:41", "10:40", "11:39", "12:38", "13:37", "14:36", "15:35", "16:34", "17:33", "18:32", "19:31"],
            "temp": [21.5, 21.7, 21.7, 22.0, 22.0, 22.2, 22.3, 22.5, 22.5, 22.5, 22.5, 22.5, 22.6, 22.6, 22.6, 22.6],
            "humidity": [58, 48, 45, 60, 52, 48, 46, 47, 46, 52, 53, 52, 53, 51, 51, 51],
            "soil": [98, 80, 78, 97, 89, 98, 97, 88, 96, 75, 75, 75, 68, 64, 63, 63]
        }

    # --- Calculations ---

    def calculate_seeds_from_weight(self, crop, total_weight):
        """Calculates total seeds based on weight."""
        if crop not in self.CROP_DATA:
            raise ValueError("Unknown crop")
        
        sample_weight = self.CROP_DATA[crop]
        if total_weight < 0:
            raise ValueError("Negative weight")

        total_seeds = (self.FIXED_SAMPLE_COUNT / sample_weight) * total_weight
        return int(total_seeds), sample_weight

    def calculate_germination_needs(self, crop, target_seeds):
        """Calculates expected germination and extra seeds needed."""
        if crop not in self.GERM_RATES:
            raise ValueError("Unknown crop")
        
        rate = self.GERM_RATES[crop]
        
        # Calculations
        expected_viable = int(target_seeds * rate)
        needed_for_target = math.ceil(target_seeds / rate)
        extra_seeds = needed_for_target - target_seeds
        
        return {
            "rate_percent": rate * 100,
            "expected_viable": expected_viable,
            "needed_total": needed_for_target,
            "extra_seeds": extra_seeds
        }

    def get_monitoring_stats(self):
        """Returns average stats for monitoring data."""
        t_avg = statistics.mean(self.MONITOR_DATA["temp"])
        h_avg = statistics.mean(self.MONITOR_DATA["humidity"])
        s_avg = statistics.mean(self.MONITOR_DATA["soil"])
        return t_avg, h_avg, s_avg

    def get_graph_data(self, mode, crop):
        """Returns comparison data for the graph."""
        data_main = self.COMPARE_DATA.get(mode, {}).get(crop, {})
        data_ref = self.COMPARE_DATA.get("No Control", {}).get(crop, {})
        return data_main, data_ref