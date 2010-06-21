/* Slice-side code to allocate tuntap interface in root slice
 * Based on bmsocket.c
 *  Thom Haddow - 08/10/09
 *
 * Call tun_alloc() with IFFTUN or IFFTAP as an argument to get back fd to
 * new tuntap interface. Interface name can be acquired via TUNGETIFF ioctl.
 */

#include <sys/un.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>

#define VSYS_TUNTAP "/vsys/fd_tuntap.control"

/* Reads vif FD from "fd", writes interface name to vif_name, and returns vif FD.
 * vif_name should be IFNAMSIZ chars long. */
int receive_vif_fd(int fd, char *vif_name)
{
	struct msghdr msg;
	struct iovec iov;
	int rv;
	size_t ccmsg[CMSG_SPACE(sizeof(int)) / sizeof(size_t)];
	struct cmsghdr *cmsg;

    /* Use IOV to read interface name */
	iov.iov_base = vif_name;
	iov.iov_len = IFNAMSIZ;

	msg.msg_name = 0;
	msg.msg_namelen = 0;
	msg.msg_iov = &iov;
	msg.msg_iovlen = 1;
	/* old BSD implementations should use msg_accrights instead of
	 * msg_control; the interface is different. */
	msg.msg_control = ccmsg;
	msg.msg_controllen = sizeof(ccmsg);

	while(((rv = recvmsg(fd, &msg, 0)) == -1) && errno == EINTR);
	if (rv == -1) {
		perror("recvmsg");
		return -1;
	}
	if(!rv) {
		/* EOF */
		return -1;
	}

	cmsg = CMSG_FIRSTHDR(&msg);
	if (!cmsg->cmsg_type == SCM_RIGHTS) {
		fprintf(stderr, "got control message of unknown type %d\n",
			cmsg->cmsg_type);
		return -1;
	}
	return *(int*)CMSG_DATA(cmsg);
}


int tun_alloc(int iftype, char *if_name)
{
    int control_fd;
    struct sockaddr_un addr;
    int remotefd;

    control_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (control_fd == -1) {
        perror("Could not create UNIX socket\n");
        exit(-1);
    }

    memset(&addr, 0, sizeof(struct sockaddr_un));
    /* Clear structure */
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, VSYS_TUNTAP,
            sizeof(addr.sun_path) - 1);

    if (connect(control_fd, (struct sockaddr *) &addr,
                sizeof(struct sockaddr_un)) == -1) {
        perror("Could not connect to Vsys control socket");
        exit(-1);
    }

    /* passing type param */
    if (send(control_fd, &iftype, sizeof(iftype), 0) != sizeof(iftype)) {
        perror("Could not send paramater to Vsys control socket");
        exit(-1);
    }

    remotefd = receive_vif_fd(control_fd, if_name);
    return remotefd;
}
