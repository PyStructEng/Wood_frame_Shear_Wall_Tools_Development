# We will be testing the functions 

import unittest
from rigid_diaphragm_analysis import calculate_center_of_rigidity, calculate_center_of_mass

class TestRigidDiaphragmAnalysis(unittest.TestCase):

    def test_calculate_center_of_rigidity(self):
        # Define test input: Walls with simplified properties
        walls = [
            {'length': 4, 'height': 3, 'x': 1, 'y': 2},
            {'length': 5, 'height': 2, 'x': 3, 'y': 4},
            {'length': 6, 'height': 4, 'x': 5, 'y': 6}
        ]
        # Expected output: Manually calculate CoR based on stiffness
        expected_CoR_x = (4/3 * 1 + 5/2 * 3 + 6/4 * 5) / (4/3 + 5/2 + 6/4)
        expected_CoR_y = (4/3 * 2 + 5/2 * 4 + 6/4 * 6) / (4/3 + 5/2 + 6/4)

        # Call the function and check the result
        CoR_x, CoR_y = calculate_center_of_rigidity(walls)
        self.assertAlmostEqual(CoR_x, expected_CoR_x, places=5)
        self.assertAlmostEqual(CoR_y, expected_CoR_y, places=5)

    def test_calculate_center_of_mass(self):
        # Define test input: Walls with simplified properties
        walls = [
            {'length': 4, 'height': 3, 'x': 1, 'y': 2},
            {'length': 5, 'height': 2, 'x': 3, 'y': 4},
            {'length': 6, 'height': 4, 'x': 5, 'y': 6}
        ]
        # Expected output: Manually calculate CoM based on area
        expected_CoM_x = (4*3 * 1 + 5*2 * 3 + 6*4 * 5) / (4*3 + 5*2 + 6*4)
        expected_CoM_y = (4*3 * 2 + 5*2 * 4 + 6*4 * 6) / (4*3 + 5*2 + 6*4)

        # Call the function and check the result
        CoM_x, CoM_y = calculate_center_of_mass(walls)
        self.assertAlmostEqual(CoM_x, expected_CoM_x, places=5)
        self.assertAlmostEqual(CoM_y, expected_CoM_y, places=5)

if __name__ == '__main__':
    unittest.main()
