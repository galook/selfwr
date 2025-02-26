SUFFIX = 'new.py'
# This is a script that generates a new file with the same content as itself
print_statements = [r"def main():", r"    print_statements.insert(0, 'print_statements = [r\042' + '\042, r\042'.join(print_statements) + '\042]')",  r"    f = open(__file__ + 'new.py', 'w')", r"    f.write('\n'.join(print_statements))", r"    f.close()", r"    for statement in print_statements:", r"        print(statement)", r"", r"if __name__ == '__main__':", r"    main()"]
def main():
    print_statements.insert(0, 'print_statements = [r\042' + '\042, r\042'.join(print_statements) + '\042]')
    f = open(__file__ + SUFFIX, 'w')
    f.write('\n'.join(print_statements))
    f.close()
    for statement in print_statements:
        print(statement)

if __name__ == '__main__':
    main()