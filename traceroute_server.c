#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <netinet/ip.h>
#include <sys/socket.h>
#include <stdbool.h>
#include <net/ethernet.h>
#include <linux/if_packet.h>

typedef struct {
    uint8_t type;
    uint8_t code; 
    uint16_t chk_sum;
} icmp_header;


typedef struct {
    icmp_header icmp_h;
    uint32_t unsed;
    struct iphdr ip_h;

} time_exceed_message;

icmp_header* fill_icmp_header(char* buffer) {
    icmp_header* icmp = (icmp_header*) buffer;
    icmp->type = 11;
}



int main() {
    struct packet_mreq mr;
    char buffer[1500];
    int sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    mr.mr_type = PACKET_MR_PROMISC;
    setsockopt(sock, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr));
    
    while(true) {
        bzero(buffer, 1500);
        int data_size = recvfrom(sock, buffer, 1500, 0, NULL, NULL);

        if (data_size > 0) {
            printf("SONO QUA");
            printf("%d-%s\n", data_size, buffer);
        } 

    }
    close(sock);


    return 0;
}