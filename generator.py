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
# python3.4 generator.py schema.yaml                                            #
# . ./test_environment.sh                                                       #
# ./script.bash ./a.out test1 test2 test3                                       #
#                                                                               #
# 
#################################################################################

import yaml
import sys

schema=sys.argv[1]

yaml_code=open(schema).read()
res=yaml.load(yaml_code)

res['formatter'][None] = "echo \"$1\""

bash_script = open('script.bash', 'w')

bash_script.write("# --------------------------------------------\n")
bash_script.write("#              SETTINGS\n")
bash_script.write("# --------------------------------------------\n")

# log variables
bash_script.write("# log vars:\n")
for fd in res['files']:
    bash_script.write("FILEPATH_%s=${FILEPATH_%s:-%s}\n" % (fd, fd, res['files'][fd]['path']))

# Vars:
bash_script.write("\n# Vars:\n")
for arg in res['args']:
    default_val=str(res['args'][arg][0])
    bash_script.write('%s=${%s:-%s}\n' % (arg, arg, default_val))
bash_script.write("\n")


# "SEND FUNCTIONS" block
bash_script.write("# SEND FUNCTIONS\n")
for stream in res['streams']:
    bash_script.write('send_%s() {\n' % stream)
    for fd in res['streams'][stream]:
        formatter=None
        ifblock=0
        for cond in res['streams'][stream][fd]:
            if cond in res['args']:
                if ifblock==0:
                    bash_script.write("  if ")
                if ifblock>0:
                    bash_script.write(" && ")
                bash_script.write("(( $%s == %s ))" % (cond, res['streams'][stream][fd][cond]))
                ifblock+=1
            if cond=='formatter':
                formatter=res['streams'][stream][fd]['formatter']
        if ifblock>0: bash_script.write("; then\n")
        code=res['formatter'][formatter].split("\n")
        code=["  {"]+["    "+line for line in code]+["  }"]
        if ifblock>0: code=["  "+line for line in code]
        code="\n".join(code)
        bash_script.write("%s >>\"$FILEPATH_%s\"" % (code, fd))
        if ifblock>0: bash_script.write(";\n  fi")
        bash_script.write("\n")
    bash_script.write('}\n\n')

i=100
for stream in res['streams']:
    bash_script.write("eval \"exec {FILEDESC_%s}> >( while read line; do send_%s \\\"\\$line\\\"; done)\"\n" % (stream, stream) )
    bash_script.write("export FILEDESC_%s\n" % stream)
    i+=1

bash_script.write("\n")

bash_script.write("_P=$1\nshift\n$_P \"$@\"\n")
