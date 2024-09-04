#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#define PORT 8080
#define BACKLOG 16

void handle_client(int client_socket) {
    char buffer[1024] = {0};
    char *message = "Hello from server\n";
    
    // Send a welcome message to the client
    send(client_socket, message, strlen(message), 0);
    printf("Message sent to client\n");

    // Continuously read and respond to client messages
    int bytes_read;
    while ((bytes_read = read(client_socket, buffer, sizeof(buffer))) > 0) {
        printf("Received from client: %s", buffer);
        // Echo the message back to the client
        send(client_socket, buffer, bytes_read, 0);
        memset(buffer, 0, sizeof(buffer));
    }

    // Client disconnected
    printf("Client disconnected\n");
    close(client_socket);
}

void sigchld_handler(int s) {
    // Wait for all dead processes
    // We use a loop to handle multiple children that terminated simultaneously
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    // Set up the SIGCHLD signal handler to clean up zombie processes
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    if (sigaction(SIGCHLD, &sa, NULL) == -1) {
        perror("sigaction failed");
        exit(EXIT_FAILURE);
    }

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Binding the socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Start listening on the socket with a backlog of 16
    if (listen(server_fd, BACKLOG) < 0) {
        perror("listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d with a backlog size of %d\n", PORT, BACKLOG);

    // Server runs indefinitely
    while (1) {
        // Accept a new connection
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept failed");
            continue;
        }

        // Fork a new process to handle the client
        if (fork() == 0) {
            // Child process
            close(server_fd); // Child doesn't need the listener
            handle_client(new_socket);
            exit(0);
        }

        // Parent process
        close(new_socket); // Parent doesn't need this socket
    }

    // Close the server socket (unreachable in this example)
    close(server_fd);

    return 0;
}
