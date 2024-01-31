"""
Author: Carter Young
Date: 1/30/24
Description: Reads in average_grades.txt and filters them according to the project description:
1. Department level:
    Function: User specifies a natural science department, and the average_grades.txt is filtered to show %As,
    %Ds/Fs, and total # of times the course was taught for every course.
    Input: average_grades.txt, Department
    Output: dept_{dept name}.txt
2. Class level:
    Function: User specifies a natural science course, and the average_grades.txt is filtered to show %As, %Ds/%Fs,
    and total # of times the course was taught per instructor for the course.
    Input: average_grades.txt, Course
    Output: class_{class name}.txt
3. Level level:
    Function: User specifies a natural science department, and the average_grades.txt is filtered to show %As, %Ds/%Fs,
    and total # of times the course was taught for every course of a specified level.
    Input: average_grades.txt, Department, Level
    Output: level_{department}_{level}.txt
"""


def read_average_grades(filename):
    """ Read in average_grades.txt """
    data = {}  # Set data to empty
    with open(filename, 'r') as file:  # Read data
        for line in file:  # Iterate
            # Split line according to format
            if line.startswith('Course'):
                parts = line.split(',')
                course = parts[0].split(':')[1].strip()
                taught_count = int(parts[2].split(':')[1].strip())
                aprec_avg = float(parts[3].split(':')[1].strip().rstrip('%').strip())
                failprec_avg = float(parts[4].split(':')[1].strip().rstrip('%').strip())

                # Error case: course not in data
                # All fields default to 0
                if course not in data:
                    data[course] = {
                        'total_taught_count': 0,
                        'aprec_avg': 0,
                        'failprec_avg': 0,
                        'count': 0
                    }

                # Treat 'taught_count' as sum
                # Treat 'aprec_avg' as avg
                # Treat 'failprec_avg' as avg
                # +1 Index for counting
                data[course]['total_taught_count'] += taught_count
                data[course]['aprec_avg'] += aprec_avg
                data[course]['failprec_avg'] += failprec_avg
                data[course]['count'] += 1

    for course in data:
        data[course]['aprec_avg'] /= data[course]['count']
        data[course]['failprec_avg'] /= data[course]['count']
        del data[course]['count']  # Remove index

    # Return average data
    return data


def filter_by_course(data, course):
    """ Filters average_data.txt by course. """
    filtered_data = {}  # Sets data to empty
    # Iterate
    for entry in data:
        # Split line according to format
        if entry.startswith('Course: ' + course):
            parts = entry.split(',')
            instructor = parts[1].split(': ')[1].strip()
            taught_count = int(parts[2].split(': ')[1].strip())
            aprec_avg = float(parts[3].split(': ')[1].strip().rstrip('%').strip())
            failprec_avg = float(parts[4].split(': ')[1].strip().rstrip('%').strip())

            # Error case: If instructor is not present...
            if instructor not in filtered_data:
                # Default to 0
                filtered_data[instructor] = {'Teaching Count': 0, 'Aprec Avg': 0, 'Failprec Avg': 0}

            # Iterate
            filtered_data[instructor]['Teaching Count'] += taught_count
            filtered_data[instructor]['Aprec Avg'] += aprec_avg
            filtered_data[instructor]['Failprec Avg'] += failprec_avg

    # Average out the aprec_avg and failprec_avg
    for instructor in filtered_data:
        count = filtered_data[instructor]['Teaching Count']
        filtered_data[instructor]['Aprec Avg'] /= count
        filtered_data[instructor]['Failprec Avg'] /= count

    # Return
    return filtered_data


def filter_by_department(data, department, level=None):
    """ Filters average_data.txt by department and, if selected, level."""
    filtered_data = {}  # Sets data to empty
    # Iterate
    for entry in data:
        # Split line according to format
        if entry.startswith('Course:'):
            parts = entry.split(',')
            course_with_code = parts[0].split(':')[1].strip()
            # Split dept and level appropriately
            course_dept = ''.join(filter(str.isalpha, course_with_code))  # Dept portion are alphabetical
            course_level = ''.join(filter(str.isdigit, course_with_code)) # Dept portion are numerical

            # Checks on two conditions
            # If level is none, consider all levels in department
            # If level is not none, consider only those courses which start with the specified digit
            if course_dept == department and (level is None or course_level.startswith(level)):
                # Split
                course = course_with_code
                instructor = parts[1].split(': ')[1].strip()
                taught_count = int(parts[2].split(': ')[1].strip())
                aprec_avg = float(parts[3].split(':')[1].strip().rstrip('%').strip())
                failprec_avg = float(parts[4].split(':')[1].strip().rstrip('%').strip())

                # Error case: course is not included in filtered_data...
                if course not in filtered_data:
                    # Default to 0
                    filtered_data[course] = {'Teaching Count': 0, 'Aprec Avg': 0, 'Failprec Avg': 0}

                # Iterate
                filtered_data[course]['Teaching Count'] += taught_count
                filtered_data[course]['Aprec Avg'] += aprec_avg
                filtered_data[course]['Failprec Avg'] += failprec_avg

    # Average out the aprec_avg and failprec_avg
    for course in filtered_data:
        count = filtered_data[course]['Teaching Count']
        filtered_data[course]['Aprec Avg'] /= count
        filtered_data[course]['Failprec Avg'] /= count

    # Return
    return filtered_data


def display_instructor_data(data, course):
    # Displays data for course filter
    print(f"Data for Course: {course}")
    # Iterates on instructions
    for instructor, info in data.items():
        # Data being displayed
        print(f"\tInstructor: {instructor}, Teaching Count: {info['Teaching Count']}, Aprec Avg: {info['Aprec Avg']}%, Failprec Avg: {info['Failprec Avg']}%")


def display_data(data):
    # Displays data for non-course filter
    for course, info in data.items():
        print(f"Course: {course}, Total Taught Count: {info['Teaching Count']}, Aprec Avg: {info['Aprec Avg']}%, Failprec Avg: {info['Failprec Avg']}%")


def main():
    filename = "average_grades.txt"
    with open(filename, 'r') as file:
        average_grades = file.readlines()

    # 1st choice: What do we want to filter by?
    choice = input("Do you want to query by department, level, or class? Enter 'department', 'level' or 'class: ").lower()
    # Department level filter and entries
    if choice == 'department':
        department = input("Enter a department (e.g., 'BI'): ")
        department_data = filter_by_department(average_grades, department)
        display_data(department_data)
    # Class level filter and entries
    elif choice == 'class':
        class_code = input("Enter a class code (e.g., 'BI121'): ")
        class_data = filter_by_course(average_grades, class_code)
        display_instructor_data(class_data, class_code)
    # Level filter and entries
    elif choice == 'level':
        department = input("Enter a department (e.g., 'BI'): ")
        level = input("Enter the course level (e.g., '1l' for 100-level courses): ")
        department_data = filter_by_department(average_grades, department, level)
        display_data(department_data)
    # Error
    else:
        print("Invalid.")


if __name__ == "__main__":
    main()