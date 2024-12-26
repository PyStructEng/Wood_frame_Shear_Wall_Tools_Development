import xlwings as xw
import numpy as np

def read_input_data(sheet):
    """
    Reads shear wall data from the Excel sheet.
    Assumes the following columns in the sheet:
    - A: Wall ID
    - B: Length (m)
    - C: Height (m)
    - D: X Coordinate (m)
    - E: Y Coordinate (m)

    Returns:
        walls: A list of dictionaries with shear wall properties.
    """
    walls = []
    last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row
    for row in range(2, last_row + 1):
        wall = {
            'id': sheet.range(f'A{row}').value,
            'length': sheet.range(f'B{row}').value,
            'height': sheet.range(f'C{row}').value,
            'x': sheet.range(f'D{row}').value,
            'y': sheet.range(f'E{row}').value,
        }
        walls.append(wall)
    return walls

def calculate_relative_rigidity(walls):
    """
    Calculates the relative rigidity of each wall using the formula:
    ∆i = 4 * (hi / Li)^3 + 3 * (hi / Li)
    Ri = 1 / ∆i

    Returns:
        rigidities: A list of rigidity values for the walls.
    """
    rigidities = []
    for wall in walls:
        height = wall['height']
        length = wall['length']
        delta = 4 * (height / length)**3 + 3 * (height / length)
        rigidity = 1 / delta
        rigidities.append(rigidity)
    return rigidities

def calculate_center_of_rigidity(walls, rigidities):
    """
    Calculates the Center of Rigidity (CoR) coordinates.

    Returns:
        CoR_x, CoR_y: Coordinates of the center of rigidity.
    """
    total_rigidity_x = 0
    total_rigidity_y = 0
    weighted_x = 0
    weighted_y = 0

    for wall, rigidity in zip(walls, rigidities):
        if rigidity > 0:  # Ensure non-zero rigidity
            weighted_x += rigidity * wall['x']
            weighted_y += rigidity * wall['y']
            total_rigidity_x += rigidity if wall['x'] != 0 else 0
            total_rigidity_y += rigidity if wall['y'] != 0 else 0

    CoR_x = weighted_x / total_rigidity_y if total_rigidity_y != 0 else 0
    CoR_y = weighted_y / total_rigidity_x if total_rigidity_x != 0 else 0

    return CoR_x, CoR_y

def calculate_polar_moment_of_inertia(walls, rigidities, CoR):
    """
    Calculates the polar moment of inertia (Jp).

    Parameters:
        walls: List of walls with properties.
        rigidities: List of rigidities for each wall.
        CoR: Tuple of Center of Rigidity coordinates (x, y).

    Returns:
        Jp: Polar moment of inertia.
    """
    Jp = 0
    for wall, rigidity in zip(walls, rigidities):
        x_bar = wall['x'] - CoR[0]
        y_bar = wall['y'] - CoR[1]
        Jp += rigidity * (x_bar**2 + y_bar**2)
    return Jp

def calculate_torsional_effects(walls, rigidities, CoM, CoR, longest_dimension, Jp):
    """
    Calculates torsional moments and the resulting forces due to torsion.

    Parameters:
        walls: List of walls with properties.
        rigidities: List of rigidities for each wall.
        CoM: Tuple of Center of Mass coordinates (x, y).
        CoR: Tuple of Center of Rigidity coordinates (x, y).
        longest_dimension: Longest building dimension for accidental torsion.
        Jp: Polar moment of inertia.

    Returns:
        torsion_effects: A list of torsional force contributions for each wall.
    """
    e_x_real = CoM[0] - CoR[0]
    e_y_real = CoM[1] - CoR[1]
    e_x_accidental = 0.1 * longest_dimension
    e_y_accidental = 0.1 * longest_dimension

    torsion_effects = []
    for wall, rigidity in zip(walls, rigidities):
        x_bar = wall['x'] - CoR[0]
        y_bar = wall['y'] - CoR[1]
        torsion_force_x = ((e_x_real + e_x_accidental) * rigidity * y_bar) / Jp
        torsion_force_y = ((e_y_real + e_y_accidental) * rigidity * x_bar) / Jp
        torsion_effects.append((torsion_force_x, torsion_force_y))

    return torsion_effects

def write_output_data(sheet, walls, torsion_effects, CoR):
    """
    Writes the calculated CoR and torsional effects directly beside input data and moves output data further away.
    """
    # Update the existing table with torsional forces
    for i, torsion in enumerate(torsion_effects):
        row = i + 2  # Assuming input data starts from row 2
        sheet.range(f'F{row}').value = torsion[0]  # Torsion X
        sheet.range(f'G{row}').value = torsion[1]  # Torsion Y

    # Add headers for torsional effects
    sheet.range('F1').value = 'Torsion X (kN)'
    sheet.range('G1').value = 'Torsion Y (kN)'

    # Move output data further away
    sheet.range('I1').value = 'Output'
    sheet.range('I2').value = 'Center of Rigidity (X)'
    sheet.range('J2').value = CoR[0]
    sheet.range('I3').value = 'Center of Rigidity (Y)'
    sheet.range('J3').value = CoR[1]

def main():
    # Open Excel Workbook
    wb = xw.Book('shearwall_data.xlsx')  # Replace with your file name
    sheet = wb.sheets['Sheet1']

    # Read Input Data
    walls = read_input_data(sheet)

    # Calculate Relative Rigidity
    rigidities = calculate_relative_rigidity(walls)

    # Perform Calculations
    CoM = (40, 25)  # Assume a predefined Center of Mass for this example
    longest_dimension = 50  # Assume longest dimension is 50m
    CoR = calculate_center_of_rigidity(walls, rigidities)
    Jp = calculate_polar_moment_of_inertia(walls, rigidities, CoR)
    torsion_effects = calculate_torsional_effects(walls, rigidities, CoM, CoR, longest_dimension, Jp)

    # Write Output Data
    write_output_data(sheet, walls, torsion_effects, CoR)

    print("Analysis complete. Results written to the spreadsheet.")

if __name__ == '__main__':
    main()


