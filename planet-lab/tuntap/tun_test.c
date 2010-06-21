#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <string.h>

#include "tunalloc.h"

int main(void)
{

struct ifreq ifr;
memset(&ifr, 0, sizeof(ifr));

    printf("Allocating tap device via VSYS\n");

    char if_name[IFNAMSIZ];

    int tun_fd = tun_alloc(IFF_TAP, if_name);

    printf("Allocated tap device: %s fd=%d\n", if_name, tun_fd);

     //Scrive il nome della tap su un file
     FILE *f;
     f=fopen("tap_name.txt","w");
     fprintf(f,"%s",if_name);
     fclose(f);
    //crea il fil eper creare la tap    
//     int one= rand() % 255 + 1;
	int one=5;
     FILE* ifile;
     ifile=fopen("file","w");
     fprintf(ifile,"%s\n172.16.2.%d\n24\n",if_name,one);
     fclose(ifile);
     printf("Sleeping...\n");
     while(1){
          sleep(120000);
     }
     printf("Closing\n");
     return 0;
}                                                                                                    
