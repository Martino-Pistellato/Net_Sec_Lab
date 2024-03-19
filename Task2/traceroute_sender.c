#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>

#define SRC_IP "10.0.2.15"	// Change It to your respective IP address
#define DST_IP "8.8.8.8"
#define DST_PORT 53


/* gcc task1.c -o task1 */


void send_packet(int ttl) {
    int sockfd;
    struct sockaddr_in dest_addr;
    unsigned char packet[2048] = {0};

    // Create raw socket
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sockfd < 0) {
        perror("Socket creation failed");
        exit(1);
    }

    // IP header
    struct iphdr * ip_header = (struct iphdr *) packet;
    ip_header->version = 4;
    ip_header->ihl = 5;
    ip_header->tos = 0;
    ip_header->tot_len = htons(20);
    ip_header->id = 0;
    ip_header->frag_off = 0;
    ip_header->ttl = ttl;
    ip_header->protocol = IPPROTO_UDP;
    ip_header->check = htons(0);
    ip_header->saddr = inet_addr(SRC_IP);
    ip_header->daddr = inet_addr(DST_IP);

    // UDP header
    struct udphdr * udp_header = (struct udphdr *) (packet + sizeof(struct iphdr));
    udp_header->source = htons(9090);
    udp_header->dest = htons(DST_PORT);
    udp_header->len = htons(8 + 1);
    udp_header->check = htons(0);
    
    // Payload (TTL value)
    char * payload = packet + sizeof(struct iphdr) + sizeof(struct udphdr);
    *payload = ttl;

    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(DST_PORT);
    dest_addr.sin_addr.s_addr = inet_addr(DST_IP);

    // Send packet to destination
    sendto(sockfd, packet, sizeof(struct iphdr) + sizeof(struct udphdr) + 1, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));

    close(sockfd);
}


int main() {
    for (unsigned int ttl = 1; ttl <= 64; ++ ttl) {
        send_packet(ttl);
        printf("Packet sent with TTL: %d\n", ttl);
        usleep(1000000);		// Delay between packets (1 second(s))
    }

    return 0;
}

