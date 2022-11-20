import xlsxwriter

def generate_custom_schedule():
    filename = 'Custom Week 1 Schedule'
    number_of_tutorials = 3
    groups_per_tutorial = 36
    tutorials = []
    group_counter = 0
    for tutorial in range(1, number_of_tutorials + 1):
        current_tutorial = {
            'Tutorial': tutorial,
            'Debates': []
        }
        table_counter = 0
        for debate in range(1, groups_per_tutorial + 1, 2):
            group_counter = group_counter + 1
            table_counter = table_counter + 1
            table_number = table_counter
            debate = {
                'Table': table_number,
                'Group X': group_counter
            }
            group_counter = group_counter + 1
            debate['Group Y'] = group_counter
            current_tutorial['Debates'].append(debate)
        tutorials.append(current_tutorial)
    workbook = xlsxwriter.Workbook('Custom Generated Schedule.xlsx')
    for tutorial in tutorials:
        current_worksheet = workbook.add_worksheet(f'Tutorial {tutorial["Tutorial"]}')
        row = 0
        col = 0
        current_worksheet.write(row, col, 'Table Number')
        current_worksheet.write(row, col+1, 'Group X')
        current_worksheet.write(row, col + 2, 'Group Y')
        row = 1
        # Iterate over the data and write it out row by row.
        for debate in tutorial['Debates']:
            current_worksheet.write(row, col, debate['Table'])
            current_worksheet.write(row, col + 1, debate['Group X'])
            current_worksheet.write(row, col + 2, debate['Group Y'])
            row += 1
    workbook.close()


if __name__ == '__main__':
    generate_custom_schedule()
