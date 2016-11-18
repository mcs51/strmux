/******************************************************************************
 * 																			  *
 * Открывает N файлов и отправляет их содержимое в N файловых дескрипторов.   *
 * Пути к файлам — аргументы к программе.									  *
 * 																			  *
 * ***************************************************************************/
 
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

int main (int argc, char **argv)
{
	FILE * files[8];
	FILE * streams[8];
	int descs[10] = {100, 101, 102, 103, 104, 105, 106, 107, 108};
	size_t sz;
	int i;
	char buf[128];
	for (i=0; i<argc-1;i++)
	{
		files[i]=fopen(argv[i+1], "r");
		if (files[i] <= 0) printf("File %s doesn't exist.\n", argv[i+1]), exit(1);
		streams[i]=fdopen(descs[i], "w");
		if(streams[i]==0) printf("Can't open desc %d.\n", descs[i]), exit(2);
		
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








