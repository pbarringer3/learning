from openpyxl import load_workbook
from random import shuffle
import os

num_drawing = 1
results = {}


def main():
    original_path = os.getcwd()
    os.chdir("../../../../DataFiles")
    wb = load_workbook("Test.xlsx")
    hat_sheet = wb['Hat']
    row_num = 2
    while hat_sheet['A'+str(row_num)].value is not None:
        results[hat_sheet['A'+str(row_num)].value] = get_restrictions_and_links(hat_sheet, row_num)
        row_num += 1
    hat = []
    for name in results:
        for i in range(num_drawing):
            hat.append(name)
    shuffle(hat)
    pick_names(hat)

    for person in results:
        create_assignments_file(person)
		
    print(results)

def pick_names(hat):
    for person in results:
        if len(results[person][2]) != num_drawing:
            success = False
            for name in hat:
                if allowed_to_draw(person, name):
                    hat.remove(name)
                    results[person][2].add(name)
                    success = pick_names(hat)
                    if success:
                        break
                    hat.append(name)
                    results[person][2].remove(name)
            return success
    return True


def allowed_to_draw(person, name):
    return not in_restrictions(person, name) and not in_link_restrictions(person, name) and not in_gift_set(person, name)

def in_restrictions(person, name):
    return name in results[person][0] or person == name

def in_link_restrictions(person, name):
    for link in results[person][1]:
        if in_gift_set(link, name) or link == name:
            return True
    return False

def in_gift_set(person, name):
    return name in results[person][2]

def create_assignments_file(person):
    file = open(person+".txt", "w")
    for assignment in results[person][2]:
        file.write(assignment+"\n")
    file.close()

#     successful = False
#     while not successful:
#         outcome = attempt_drawing(results, hat)
#         results = outcome(0)
#         successful = outcome(1)
#
# def attempt_drawing(results, hat):
#     for person in results:
#         results[person](2).add(draw_name(results, person))
#         results[person](2).add(draw_name(results, person))


def get_restrictions_and_links(hat, row_num):
    restrictions = set()
    if hat['B'+str(row_num)].value is not None:
        restrictions = set(hat['B'+str(row_num)].value.split(','))
    links = set()
    if hat['C'+str(row_num)].value is not None:
        links = set(hat['C'+str(row_num)].value.split(','))
    return restrictions, links, set()

if __name__ == '__main__':
    main()
