#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <stdlib.h>

struct udpheader{
    u_int16_t udph_sport;
    u_int16_t udph_dport;
    u_int16_t udph_ulen;
    u_int16_t upd_sum;
};

struct ipheader{
    unsigned char iph_ihl:4, 
                  iph_ver:4;
    unsigned char iph_tos;
    unsigned short int iph_len;
    unsigned short int iph_ident;
    unsigned short int iph_flag:3,
                     iph_offset:13;
    unsigned char iph_ttl;
    unsigned char iph_protocol;
    unsigned short int iph_chksum;
    struct in_addr iph_sourceip;
    struct in_addr iph_destip;
};

struct ipheader * fill_ip_header(char * buffer, char * s_addr, int packet_size){
    struct ipheader * ip = (struct ipheader *) buffer;
    ip->iph_ver = 4;
    ip->iph_ihl = 5;
    ip->iph_ttl = 20;
    ip->iph_protocol = IPPROTO_UPD;
    ip->iph_sourceip.s_addr = inet_addr(s_addr);
    ip->iph_destip.s_addr = inet_addr("127.0.0.1");
    ip->iph_len = htons(sizeof(struct ipheader) + packet_size);
    return ip;
}

struct updheader * fill_upd_header(char * buffer, int msg_len){
    struct updheader * upd = (struct updheader *) (buffer);
    upd->udph_sport = htons(12345);
    upd->udph_dport = htons(9090);
    upd->udph_ulen = htons(sizeof(struct updheader) + msg_len);
    upd->upd_sum = 0;
    return upd;
}

void main(int argc, char **argv) {
    char buffer[1500];
    char * src_ip = "8.8.8.8";
    struct sockadddr_in dest;
    char * message = "Test message\n";
    int msg_len = strlen(message);
    int iph_len = sizeof(struct ipheader);
    int upd_len = sizeof(struct updheader);
    int total_lenght = iph_len + upd_len + msg_len;
    if (argc > 1){
        src_ip = argv[1];
    }
    struct ipheader * ip = fill_ip_header(buffer, src_ip, upd_len + msg_len);
    struct updheader * upd = fill_upd_header(buffer + iph_len, msg_len);

    strncpy(buffer + iph_len + upd_len, message, msg_len);

    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    dest.sin_family = AF_INET;
    dest.sin_addr = ip->iph_destip;
    sendto(sock, ip, ntohs(ip->iph_len), 0, (struct sockaddr *) &dest, sizeof(dest));
    close(sock);
}

//the forge has to be run as administrator