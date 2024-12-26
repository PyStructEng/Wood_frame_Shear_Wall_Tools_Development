# We will have all the functions 

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

def calculate_center_of_rigidity(walls):
    """
    Calculate the center of rigidity (CoR).
    CoR is determined by weighting each wall's stiffness by its position.

    Returns:
        CoR_x, CoR_y: Coordinates of the center of rigidity.
    """
    total_stiffness = 0
    weighted_x = 0
    weighted_y = 0

    for wall in walls:
        stiffness = wall['length'] / wall['height']  # Simplified stiffness calculation
        weighted_x += stiffness * wall['x']
        weighted_y += stiffness * wall['y']
        total_stiffness += stiffness

    CoR_x = weighted_x / total_stiffness if total_stiffness != 0 else 0
    CoR_y = weighted_y / total_stiffness if total_stiffness != 0 else 0

    return CoR_x, CoR_y

def calculate_center_of_mass(walls):
    """
    Calculate the center of mass (CoM).
    CoM is determined by weighting each wall's area by its position.

    Returns:
        CoM_x, CoM_y: Coordinates of the center of mass.
    """
    total_area = 0
    weighted_x = 0
    weighted_y = 0

    for wall in walls:
        area = wall['length'] * wall['height']
        weighted_x += area * wall['x']
        weighted_y += area * wall['y']
        total_area += area

    CoM_x = weighted_x / total_area if total_area != 0 else 0
    CoM_y = weighted_y / total_area if total_area != 0 else 0

    return CoM_x, CoM_y

def write_output_data(sheet, CoR, CoM):
    """
    Writes the calculated CoR and CoM to the Excel sheet.
    """
    sheet.range('G1').value = 'Output'
    sheet.range('G2').value = 'Center of Rigidity (X)'
    sheet.range('H2').value = CoR[0]
    sheet.range('G3').value = 'Center of Rigidity (Y)'
    sheet.range('H3').value = CoR[1]

    sheet.range('G5').value = 'Center of Mass (X)'
    sheet.range('H5').value = CoM[0]
    sheet.range('G6').value = 'Center of Mass (Y)'
    sheet.range('H6').value = CoM[1]

def main():
    # Open Excel Workbook
    wb = xw.Book('shearwall_data.xlsx')  # Replace with your file name
    sheet = wb.sheets['Sheet1']

    # Read Input Data
    walls = read_input_data(sheet)

    # Perform Calculations
    CoR = calculate_center_of_rigidity(walls)
    CoM = calculate_center_of_mass(walls)

    # Write Output Data
    write_output_data(sheet, CoR, CoM)

    print("Analysis complete. Results written to the spreadsheet.")

if __name__ == '__main__':
    main()
