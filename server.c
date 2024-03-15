// CLIENT

// sorry per i commenti :) -g

#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <stdlib.h>

void main()
{

    struct sockaddr_in server; // tipo stockaddr_in viene chiamato server

    char buf[1500]; // crea buffer di 1500 byte.

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); // dentro sock ci sarà l'id del socket
    memset((char *)(&server), 0, sizeof(struct sockaddr_in));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);
    server.sin_port = htons(9090);
    if (bind(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        perror("Can not bind to port or address");
        exit(1);
    }
    while (1)
    {
        bzero(buf, 1500);
        read(sock, buf, 1500);
        printf("%S\n", buf);
    }
    close(sock);
}