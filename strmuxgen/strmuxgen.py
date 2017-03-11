#!/usr/bin/python3.4

#################################################################################
#                                                                               #
#   Генерация script.bash по схеме yaml, которая передается 1м аргументом       #
#                                                                               #
# Для теста подготовлено:                                                       #
# test_environment.sh - содежит переменные и ф-ции, специфичные для задачи      #
# test_filetodesc.c - исходный код программы, которая отправляет содержимое     #
# переданных ей файлов в файловые дескрипторы начиная с 100                     #
# a.out - скомпилированная программа test_filetodesc.c                          #
# test1, test2, test3, test4 - файлы, содержимое которых совпадает с названием  #
#                                                                               #
# Пример использования:                                                         #
# ./strmuxgen.py schema.yaml -o script.bash                                     #
# . ./test_environment.sh                                                       #
# ./script.bash ./a.out test1 test2 test3 ..., где порядок аргументов такой:    #
#       disp, info, warn, dbglog, dbg, syswarn, syserr, sysdbg                  #
#                                                                               #
# TODO1: FILEPATH_* можно тоже свернуть в ассоциативный массив bash             #
# TODO2: setuptools разобраться                                                 #
#################################################################################

import numbers

def strmuxgen(schema):
    output=""
    output+="# ---------------------------------------------------------\n"
    output+="# Thisscript is generated\n"
    output+="# ---------------------------------------------------------\n"
    output+="# --------------------------------------------\n"
    output+="#              FUNCTIONS \n"
    output+="# --------------------------------------------\n"
    output+='''ind_by_val() {
        val=$1
        array=(${!2})
        for ((ind=0;ind<${#array[@]};ind++));
        do
            [[ "${array[ind]}" == "$val" ]] && return $ind
            [[ "$val" == "$ind" ]] && return $ind
        done
    }\n\n'''
    output+="# --------------------------------------------\n"
    output+="#              SETTINGS\n"
    output+="# --------------------------------------------\n"
    # log variables
    output+="# log vars:\n"
    for fd in schema['files']:
        output+="FILEPATH_%s=${FILEPATH_%s:-%s}\n" % (fd, fd, schema['files'][fd]['path'])
    # Vars:
    # if args can take not number values
    output+="\n# Vars:\n"
    for arg in schema['args']:
        resault=isinstance(schema['args'][arg][0], numbers.Number)
        if resault==False:
            output+='VARS_%s=( ' % arg
            for value in schema['args'][arg]:
                 output+='%s ' % value
            output+=')\n'
    output+="\n"
    #initialize args
    for arg in schema['args']:
        default_val=str(schema['args'][arg][0])
        output+='%s=${%s:-%s}\n' % (arg, arg, default_val)
    output+="\n"    
    # "SEND FUNCTIONS" block
    output+="# SEND FUNCTIONS\n"
    for stream in schema['streams']:
        output+='send_%s() {\n' % stream
        for fd in schema['streams'][stream]:
            formatter=None
            ifblock=0
            for cond in schema['streams'][stream][fd]:
                if cond in schema['args']:
                    operator="=="
                    resault=isinstance(schema['streams'][stream][fd][cond], numbers.Number)
                    if resault==False:
                        value=schema['streams'][stream][fd][cond]
                        # analize the operator in condition: ==, >, <, >=, <=
                        if schema['streams'][stream][fd][cond][0]==">":
                            if schema['streams'][stream][fd][cond][1]=="=": 
                                operator=">="
                                value=schema['streams'][stream][fd][cond][2:]
                            else: 
                                operator=">"
                                value=schema['streams'][stream][fd][cond][1:]
                        if schema['streams'][stream][fd][cond][0]=="<": 
                            if schema['streams'][stream][fd][cond][1]=="=":
                                operator="<="
                                value=schema['streams'][stream][fd][cond][2:]
                            else:
                                operator="<"
                                value=schema['streams'][stream][fd][cond][1:]
                        output+="  ind_by_val $%s VARS_%s[@]\n" % (cond, cond)
                        value=schema['args'][cond].index(value)
                    if ifblock==0:
                        output+="  if "
                    if ifblock>0:
                        output+=" && "
                    output+="(( $? %s %s ))" % (operator, value)
                    ifblock+=1
                if cond=='formatter':
                    formatter=schema['streams'][stream][fd]['formatter']
            if ifblock>0: output+="; then\n"
            code=schema['formatter'][formatter].split("\n")
            code=["  {"]+["    "+line for line in code]+["  }"]
            if ifblock>0: code=["  "+line for line in code]
            code="\n".join(code)
            output+="%s >>\"$FILEPATH_%s\"" % (code, fd)
            if ifblock>0: output+=";\n  fi"
            output+="\n"
        output+='}\n\n'
    i=100
    for stream in schema['streams']:
        output+="eval \"exec {FILEDESC_%s}> >( while read line; do send_%s \\\"\\$line\\\"; done)\"\n" % (stream, stream)
        output+="export FILEDESC_%s\n" % stream
        i+=1
    output+="\n"
    output+="_P=$1\nshift\n$_P \"$@\"\n"
    return output

