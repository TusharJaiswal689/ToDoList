# import pytest

# class Student:
#     def __init__(self, first_name, last_name, course, years):
#         self.first_name= first_name
#         self.last_name= last_name
#         self.course= course
#         self.years= years

# @pytest.fixture
# def default_expmployee():
#     return Student("John", "Doe", "CS", 3)

# def test_person_initialization():
#     p= Student("John", "Doe", "CS", 3)
#     assert p.first_name== "John", "First name should be John."
#     assert p.last_name== "Doe", "Last name should be Doe."
#     assert p.course== "CS"
#     assert p.years== 3

# def test_person_init_fixtures(default_expmployee):
#     assert default_expmployee.first_name== "John", "First name should be John."
#     assert default_expmployee.last_name== "Doe", "Last name should be Doe."
#     assert default_expmployee.course== "CS"
#     assert default_expmployee.years== 3
    