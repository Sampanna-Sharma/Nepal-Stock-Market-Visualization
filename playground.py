list1 = ["['Nepal', 'Inida']", "['South Africa']", "['France','Belgium']"]
print(list1)
list1 = [val for sublist in list1 for val in eval(sublist)]
print(list1)