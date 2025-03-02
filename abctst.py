SUFFIX = 'new.py'
# This is a script that generates a new file with the same content as itself
print_statements = [r"SUFFIX = 'new.py'", r"# This is a script that generates a new file with the same content as itself", r"def main():", r"    # Add the first line containing the file line array, use the unicode character to work both here and in the declaration line", r"    print_statements.insert(2, 'print_statements = [r\042' + '\042, r\042'.join(print_statements) + '\042]')", r"    # Open a new file and write the content", r"    f = open(__file__ + SUFFIX, 'w', encoding='utf-8')", r"    f.write('\n'.join(print_statements))", r"    f.close()", r"    # Write the content to the console", r"    for statement in print_statements:", r"        print(statement)", r"", r"if __name__ == '__main__':", r"    main()"]
def main():
    # Add the first line containing the file line array, use the unicode character to work both here and in the declaration line
    print_statements.insert(2, 'print_statements = [r\042' + '\042, r\042'.join(print_statements) + '\042]')
    # Open a new file and write the content
    f = open(__file__ + SUFFIX, 'w', encoding='utf-8')
    f.write('\n'.join(print_statements))
    f.close()
    # Write the content to the console
    for statement in print_statements:
        print(statement)

if __name__ == '__main__':
    main()