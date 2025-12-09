class OurfirstClass:
    white_board = 1
    chair = 0
    projector = 1
    table = 0
    pass


lecture_room_101 = OurfirstClass()
lecture_room_102 = OurfirstClass()
# print(lecture_room_101.projector)


class Laboratory(OurfirstClass):  # Inheritance
    safety_box = 2
    chemical_rack = 3
    pass


lab_room_101 = Laboratory()
print(lab_room_101.projector)


if __name__ == "__main__":
    ...
