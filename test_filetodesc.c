/******************************************************************************
 * 																			  *
 *  Открывает N файлов и отправляет их содержимое в N файловых дескрипторов.  *
 *  Пути к файлам — аргументы к программе.
 *  disp info warn dbglog dbg syswarn syserr sysdbg                           *
 * 																			  *
 * ***************************************************************************/
 
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main (int argc, char **argv)
{
	FILE * files[8];
	FILE * streams[8];
    extern char **environ;
    char* order[] = {"disp", "info", "warn", "dbglog", "dbg", "syswarn", "syserr", "sysdbg"};    
    
    int descs[10];
    char th_name[8][16];
    size_t sz;
	char buf[128];
    int i=0,j=0, k=0;
    
    while (environ[i]!=NULL && j<10)
    {
        if ( strncmp(environ[i], "FILEDESC_", 9) == 0)
        {
           for(k=0;environ[i][k]!='=';k++);
           descs[j]=atoi(environ[i]+k+1);
           strncpy(th_name[j], environ[i]+9,k-9);
           th_name[j][k-9]='\0';
           j++;
        }
        i++;
    }    
    
	for (i=0; i<argc-1;i++)
	{
		files[i]=fopen(argv[i+1], "r");
		if (files[i] <= 0) printf("File %s doesn't exist.\n", argv[i+1]), exit(1);
        
        for (j=0;j<8;j++) if( strcmp(order[i], th_name[j]) == 0 ) break;
      
		streams[i]=fdopen(descs[j], "w");
		if(streams[i]==0) printf("Can't open desc %d.\n", descs[i], i), exit(2);
		
		do
		{
			sz = fread( buf, 1, 128, files[i] );
			fwrite(buf, 1, sz, streams[i]);
		} while ( sz > 0);
		
		fclose(files[i]);
		fclose(streams[i]);
	}
	return 0;
}








