import ast
import os
import pathlib
import refactortxt as refactor

class HashTable:

    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()
        self.count = 0
    def create_buckets(self):
        return [[] for _ in range(self.size)]

    def set_val(self, key, val):

        hashed_key = hash(key) % self.size

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record


            if record_key == key:
                found_key = True
                break


        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))
            self.count += 1


    def get_val(self, key):

        hashed_key = hash(key) % self.size

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record


            if record_key == key:
                found_key = True
                break


        if found_key:
            return record_val
        else:
            return "No record found"

    def check_val(self, key):


        hashed_key = hash(key) % self.size


        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record


            if record_key == key:
                found_key = True
                break


        if found_key:
            return True
        else:
            return False


    def clear_Hash(self,list):
        for i in list:
            self.delete_val(i)



    def delete_val(self, key):


        hashed_key = hash(key) % self.size

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    def __str__(self):
        return "".join(str(item) for item in self.hash_table)


class AnalysisNodeVisitor(ast.NodeVisitor):
    hash_table_method = HashTable(100)
    hash_table_var = HashTable(100)
    flag = 0
    c_var = 1
    c_method = 1
    listofhashmethod = list()
    listofhashvar = list()

    def reset_counters(self):
        AnalysisNodeVisitor.c_var = 1
        AnalysisNodeVisitor.c_method = 1

    def visit_Import(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print('Node type: Assign and fields: ', node._fields, node.targets)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node):
        print('Node type: BinOp and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print('Node type: Expr and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Num(self, node):
        print('Node type: Num and fields: ', node._fields , node.value , node.kind)

    def visit_Name(self, node):
        if AnalysisNodeVisitor.flag == 0:
            if AnalysisNodeVisitor.hash_table_var.check_val(node.id):
                val = AnalysisNodeVisitor.hash_table_var.get_val(node.id)
                node.id = 'Var_' + val.__str__()
            else:
                AnalysisNodeVisitor.hash_table_var.set_val(node.id, AnalysisNodeVisitor.c_var)
                print(node.id + ',' + AnalysisNodeVisitor.c_var.__str__())
                AnalysisNodeVisitor.listofhashvar.append(node.id)
                node.id = 'Var_' + AnalysisNodeVisitor.c_var.__str__()
                AnalysisNodeVisitor.c_var += 1
            print('Node type: Name and fields VAR: ', node._fields, node.id, )
        elif AnalysisNodeVisitor.flag == 1:
            if AnalysisNodeVisitor.hash_table_method.check_val(node.id):
                val = AnalysisNodeVisitor.hash_table_method.get_val(node.id)
                node.id = 'Method_' + val.__str__()
            else:
                AnalysisNodeVisitor.hash_table_method.set_val(node.id, AnalysisNodeVisitor.c_method)
                print(node.id + ',' + AnalysisNodeVisitor.c_method.__str__())
                AnalysisNodeVisitor.listofhashmethod.append(node.id)
                node.id = 'Method_' + AnalysisNodeVisitor.c_method.__str__()
                AnalysisNodeVisitor.c_method += 1
            print('Node type: Name and fields METHOD: ', node._fields, node.id, )
        AnalysisNodeVisitor.flag = 0
        ast.NodeVisitor.generic_visit(self, node)


    def visit_FunctionDef(self, node):
        if AnalysisNodeVisitor.hash_table_method.check_val(node.name):
            val = AnalysisNodeVisitor.hash_table_method.get_val(node.name)
            node.name = 'Method_' + val.__str__()
        else:
            AnalysisNodeVisitor.hash_table_method.set_val(node.name, AnalysisNodeVisitor.c_method)
            print(node.name + ',' + AnalysisNodeVisitor.c_method.__str__())
            AnalysisNodeVisitor.listofhashmethod.append(node.name)
            node.name = 'Method_' + AnalysisNodeVisitor.c_method.__str__()
            AnalysisNodeVisitor.c_method += 1
        ast.NodeVisitor.generic_visit(self, node)


    def visit_Call(self, node):
        print('Node type: Call and fields: ', node._fields, node.func)
        AnalysisNodeVisitor.flag = 1
        ast.NodeVisitor.generic_visit(self, node)


    def visit_Return(self, node):
        print('Node type: Return and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_arg(self, node):
        if AnalysisNodeVisitor.hash_table_var.check_val(node.arg ):
            val = AnalysisNodeVisitor.hash_table_var.get_val(node.arg )
            node.arg = 'Var_' + val.__str__()
        else:
            AnalysisNodeVisitor.hash_table_var.set_val(node.arg , AnalysisNodeVisitor.c_var)
            print(node.arg + ',' + AnalysisNodeVisitor.c_var.__str__())
            AnalysisNodeVisitor.listofhashvar.append(node.arg)
            node.arg  = 'Var_' + AnalysisNodeVisitor.c_var.__str__()
            AnalysisNodeVisitor.c_var += 1
        print('Node type: Arg and fields: ', node._fields, node.arg )
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print('Node type: Str and fields: ', node._fields)

    def visit_AsyncFunctionDef(self, node):
        print('Node type: AsyncFunctionDef and fields: ', node._fields, node.arg)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Constant(self, node):
        if type(node.value) == str:
            if AnalysisNodeVisitor.hash_table_var.check_val(node.value):
                val = AnalysisNodeVisitor.hash_table_var.get_val(node.value)
                node.value= 'Var_' + val.__str__()
            else:
                AnalysisNodeVisitor.hash_table_var.set_val(node.value, AnalysisNodeVisitor.c_var)
                print(node.value + ',' + AnalysisNodeVisitor.c_var.__str__())
                AnalysisNodeVisitor.listofhashvar.append(node.value)
                node.value = 'Var_' + AnalysisNodeVisitor.c_var.__str__()
                AnalysisNodeVisitor.c_var += 1
        print('Node type: Constant and fields: ', node._fields, node.value)




def astrewrite(path, type):

    if type == 'fixed':
        filetype = open("../fixed.txt", "a+")
    elif type == 'buggy':
        filetype = open("../buggy.txt", "a+")

    try:
        with open(path, "r") as source:
            file = ast.parse(source.read())
            flag = 0
            v = AnalysisNodeVisitor()
            v.visit(file)
            v.hash_table_var.clear_Hash(v.listofhashvar)
            v.hash_table_method.clear_Hash(v.listofhashmethod)
            v.reset_counters()
            str = ast.unparse(file)
            str_list = str.split()
            new_str = " ".join(str_list)
            filetype.write(new_str + '\n')
            filetype.close()
            source.close()
            print(new_str)
    except:
        filetype.write('CAN NOT EVEN COMPILE' + '\n')
        filetype.close()
        source.close()
        print("Can not even compile")


def refactor():
    with open('fixed.txt', 'r') as fixedfile, open('buggy.txt', 'r') as buggyfile:
        fixedlines = fixedfile.readlines()
        buggylines = buggyfile.readlines()
    with open('fixed.txt', 'w') as fixedfile, open('buggy.txt', 'w') as buggyfile:
        for fixedline, buggyline in zip(fixedlines, buggylines):
            if fixedline.strip("\n") != "CAN NOT EVEN COMPILE" and buggyline.strip("\n") != "CAN NOT EVEN COMPILE":
                    buggyfile.write(buggyline)
                    fixedfile.write(fixedline)


path = pathlib.Path(__file__).parent.resolve()
fullpath = str(path) + "\pythonfiles\\fixedfiles"
const_path = fullpath
os.chdir(fullpath)

resetfixedfile = open("../fixed.txt", "r+")
resetfixedfile.truncate(0)
resetfixedfile.close()
for dosya in os.listdir():
    if dosya.endswith(".txt"):
        file_path = f"{const_path}\{dosya}"
        file_name = os.path.basename(file_path)
        astrewrite(file_path, 'fixed')

path = pathlib.Path(__file__).parent.resolve()
fullpath = str(path) + "\pythonfiles\\buggyfiles"
const_path = fullpath
os.chdir(fullpath)

resetbuggyfile = open("../buggy.txt", "r+")
resetbuggyfile.truncate(0)
resetbuggyfile.close()
for dosya in os.listdir():
    if dosya.endswith(".txt"):
        file_path = f"{const_path}\{dosya}"
        file_name = os.path.basename(file_path)
        astrewrite(file_path, 'buggy')

path = pathlib.Path(__file__).parent.resolve()
fullpath = str(path) + "\pythonfiles\\buggyfiles"
const_path = fullpath
os.chdir(fullpath)
os.chdir("../")
refactor()








