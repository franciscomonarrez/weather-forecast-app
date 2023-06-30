import unittest
from weather import kelvin_to_fahrenheit, get_outfit_recommendation

# Define a test class that inherits from unittest.TestCase
class TestWeather(unittest.TestCase):

    # Test case for kelvin_to_fahrenheit function
    def test_kelvin_to_fahrenheit(self):
        # Test conversion of 273.15 Kelvin to Fahrenheit
        self.assertAlmostEqual(kelvin_to_fahrenheit(273.15), 32.0, places=2)
        # Test conversion of 300 Kelvin to Fahrenheit
        self.assertAlmostEqual(kelvin_to_fahrenheit(300), 80.33, places=2)
        # Test conversion of 0 Kelvin to Fahrenheit
        self.assertAlmostEqual(kelvin_to_fahrenheit(0), -459.67, places=2)

    # Test case for get_outfit_recommendation function
    def test_get_outfit_recommendation(self):
        # Test outfit recommendation for 30 degrees Fahrenheit
        self.assertEqual(get_outfit_recommendation(30), "Heavy coat, hat, gloves, and scarf")
        # Test outfit recommendation for 40 degrees Fahrenheit
        self.assertEqual(get_outfit_recommendation(40), "Coat, hat and gloves")
        # Test outfit recommendation for 60 degrees Fahrenheit
        self.assertEqual(get_outfit_recommendation(60), "Jacket or sweater")
        # Test outfit recommendation for 80 degrees Fahrenheit
        self.assertEqual(get_outfit_recommendation(80), "Shorts and a t-shirt")
        # Test outfit recommendation for 100 degrees Fahrenheit
        self.assertEqual(get_outfit_recommendation(100), "Shorts, t-shirt and stay hydrated")


# Run the test cases if the script is executed directly
if __name__ == "__main__":
    unittest.main()
