#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <netinet/ip.h>
#include <sys/socket.h>
#include <stdbool.h>
#include <net/ethernet.h>
#include <linux/if_packet.h>
#include <netinet/udp.h>


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


struct udpheader{
    u_int16_t udph_sport;
    u_int16_t udph_dport;
    u_int16_t udph_ulen;
    u_int16_t upd_sum;
};

struct icmpheader {
    uint8_t type;
    uint8_t code;
    uint16_t checksum;
    uint32_t unused;
    // struct ipheader iphdr;
    // uint64_t datagram_data;
};

struct payload {
    struct iphdr ip_h;
    struct udpheader udp_h;
    uint8_t TTL;
};

char* load_address(uint32_t saddr, char* buffer) {
    inet_ntop(AF_INET, &saddr, buffer, INET_ADDRSTRLEN);
    return buffer;
}

char* load_TTL(char* buffer) {
    struct payload* pl = (struct payload*) (buffer + sizeof(struct iphdr) + sizeof(struct icmpheader));
    printf("%d\n", pl->TTL);
}

void filter_time_exceed(char* buffer) {
    struct iphdr* ip_hr = (struct iphdr*) (buffer);
    struct icmpheader* icmphdr = (struct icmpheader*) (buffer+sizeof(struct iphdr));
    char buff[1500];
    // printf("%s\n", return_address(ip_hr->saddr, buff));
    if (icmphdr->code == 0 && icmphdr->type == 11) {
        load_address(ip_hr->saddr, buff);
        printf("Source address = %s\n", buff);
        load_TTL(buffer);
    }
}


int main() {
    struct packet_mreq mr;
    char buffer[2500];
    memset(buffer,0, 2500);
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    mr.mr_type = PACKET_MR_PROMISC;
    setsockopt(sock, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr));
    while(true) {
        bzero(buffer, 2500);
        int data_size = recvfrom(sock, buffer, 2500, 0, NULL, NULL);
        if (data_size > 0) {
            // printf("%d\n", data_size);
            filter_time_exceed(buffer);
        } 

    }
    close(sock);

    return 0;
}