#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <sys/socket.h>
#include <stdbool.h>
#include <net/ethernet.h>
#include <linux/if_packet.h>


/* gcc traceroute_server.c -o traceroute_server */


struct icmpheader {
    uint8_t type;
    uint8_t code;
    uint16_t checksum;
    uint32_t unused;
};


char * load_address(uint32_t saddr) {
    char *ipaddr = (char *) malloc(INET_ADDRSTRLEN);
    
    if (ipaddr == NULL) {
        fprintf(stderr, "Memory allocation failed");
        return NULL;
    }

    inet_ntop(AF_INET, &saddr, ipaddr, INET_ADDRSTRLEN);    // Convert binary IP to human-readable format
    
    if (ipaddr == NULL) {
        fprintf(stderr, "Conversion error");
        return NULL;
    }
    
    return ipaddr;
}


uint8_t * load_TTL(char *buffer) {
    uint8_t *ttl = (uint8_t *) malloc(sizeof(uint8_t));
    uint8_t *payload = (uint8_t *) (buffer + sizeof(struct iphdr) + sizeof(struct icmpheader) + sizeof(struct iphdr) + sizeof(struct udphdr));

    if (ttl == NULL) {
        fprintf(stderr, "Memory allocation failed");
        return NULL;
    }

    *ttl = *payload;     // Extract TTL value

    return ttl;
}


void filter_time_exceed(char *buffer) {
    struct iphdr *ip_hr = (struct iphdr *) (buffer);
    struct icmpheader *icmphdr = (struct icmpheader *) (buffer + sizeof(struct iphdr));
    char *ipaddr = load_address(ip_hr->saddr);      // Load source IP address
    uint8_t *ttl = load_TTL(buffer);                // Load TTL value

    if (ipaddr == NULL || ttl == NULL) return;

    if (icmphdr->code == 0 && icmphdr->type == 11) {
        printf("Source address = %s\n", ipaddr);
        printf("TTL = %d\n\n", *ttl);
    }
    
    free(ipaddr);
    free(ttl);
}


int main() {
    struct packet_mreq mr;
    char buffer[2048] = {0};
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);     // Create raw socket for ICMP packets
    size_t data_size = 0;
    
    mr.mr_type = PACKET_MR_PROMISC;
    setsockopt(sock, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr));   // Set socket options
    
    while (true) {
        bzero(buffer, 2048);
        data_size = recvfrom(sock, buffer, 2048, 0, NULL, NULL);
        
        if (data_size > 0) {
            filter_time_exceed(buffer);     // Filter and process time exceeded packets
        }
    }
    
    close(sock);

    return 0;
}
