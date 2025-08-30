---
layout: post
title: "AWS Transit Gateway Connect to Palo Alto Firewalls -SD-WAN like architecture?"
date: 2023-06-30T18:13:34
---

* * *

AWS announced the TGW Connect attachment a couple of years ago, in the hopes of making SD-WAN connectivity to the cloud seamless and vendor agnostic with a couple of deployment architectures. I decided to give it a spin and see what it is all about and whether it is as easy to setup as it looks.

Context: My lab and blog are based on the design described in this blog post: <https://aws.amazon.com/blogs/networking-and-content-delivery/simplify-sd-wan-connectivity-with-aws-transit-gateway-connect/> with a twist — I do not have an on prem SD-WAN device and opted for a regular IPSEC tunnel to a mock site using AWS VGW as the termination device.

![](/assets/images/aws-transit-gateway-connect-to-palo-alto-firewalls-sd-wan-like-architecture-0.jpeg)

### The steps to configure AWS Transit Gateway are posted in the Amazon blog post referenced above. Some gotchas/tips:

  1. Make sure you have assigned a CIDR to your Transit Gateway ss it will be acting as a GRE peer to your NVA/firewalls.
  2. When you create a Connect Peer AWS will provide you with 2 BGP peers — you do not need to peer your firewall to both but you could choose to do so if you want some additional redundancy:



![](/assets/images/aws-transit-gateway-connect-to-palo-alto-firewalls-sd-wan-like-architecture-1.png)

3\. Ensure that you use distinct BGP ASN for your firewall, Transit Gateway and VPN Gateway for eBGP peering

### Palo Alto Firewall side configuration tips:

  1. You will require 2 x tunnel interfaces, one tunnel interface facing Transit Gateway and acting as BGP peer and a second tunnel interface acting as the BGP peer towards the AWS VGW gateway. What can be confusing initially is what IP addresses to assign, you will have to carve out 169.254.x.x IP addresses for this: <https://docs.aws.amazon.com/vpc/latest/tgw/tgw-connect.html>
  2. GRE Tunnel config: Palo Alto requires a static IP for the Local Address configuration, this threw me off quite a bit:

![](/assets/images/aws-transit-gateway-connect-to-palo-alto-firewalls-sd-wan-like-architecture-2.png)

Amazon VPC assigns IP addresses to your ENI via DHCP, you cannot have a statically assigned IP on your interface. You need to take the VPC assigned ENI IP and configure the same IP for your firewall ethernet interface, otherwise you will not be able to configure the GRE tunnel facing Transit Gateway. Hopefully Palo will find a cleaner way of doing this and it is not very well documented. Most documentation I found was for on prem networking and not AWS TGW.

3\. eBGP Multihop is required for your peer to come up, as per AWS:

  * Exterior BGP (eBGP): Used for connecting to routers that are in a different autonomous system than the transit gateway. If you use eBGP, you must configure ebgp-multihop with a time-to-live (TTL) value of 2. Some useful docs here:



<https://docs.aws.amazon.com/vpc/latest/tgw/tgw-connect.html> and <https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClKkCAK>

4\. IPSEC Tips: This is another gotcha which is particular to deploying PAN in a public cloud. When configuring your IKE gateway you need to leave the Local IP Address setting as None (in the physical world this is never the case). Instead you supply a Local Identification IP and Peer Identification IP as per the screenshot:

![](/assets/images/aws-transit-gateway-connect-to-palo-alto-firewalls-sd-wan-like-architecture-3.png)

More details as to why this is needed over here:

[**IKE Phase-1 negotiation failure due to missing identification for PA-VM deployed in Azure**  
 _Navigate to Firewall WebUI &gt; Network &gt; Network Profile &gt; IKE Gateways &gt; Configure Local Identification as…_knowledgebase.paloaltonetworks.com](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000PP5OCAW&refURL=http%3A%2F%2Fknowledgebase.paloaltonetworks.com%2FKCSArticleDetail "https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000PP5OCAW&refURL=http%3A%2F%2Fknowledgebase.paloaltonetworks.com%2FKCSArticleDetail")[](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000PP5OCAW&refURL=http%3A%2F%2Fknowledgebase.paloaltonetworks.com%2FKCSArticleDetail)

### Final Thoughts

Above are some tips that will help you get started with Palo Alto and Amazon Transit Gateway Connect. I did not list each individual step since that will take away from learning but the tips I am providing will definitely save you time and effort. This proves that traditional network architecture can be replicated in the cloud, GRE is recommended if you want to bundle up several tunnels for increased throughput between your TGW and NVA/firewall.

Additional resources for learning which I found very useful:

[**Scaling VPN throughput using AWS Transit Gateway | Amazon Web Services**  
 _A virtual private network (VPN) is one of the most common ways that customers connect securely to the AWS Cloud from…_ aws.amazon.com](https://aws.amazon.com/blogs/networking-and-content-delivery/scaling-vpn-throughput-using-aws-transit-gateway/ "https://aws.amazon.com/blogs/networking-and-content-delivery/scaling-vpn-throughput-using-aws-transit-gateway/")[](https://aws.amazon.com/blogs/networking-and-content-delivery/scaling-vpn-throughput-using-aws-transit-gateway/)

[**How to verify GRE tunnel operation using CLI commands**  
 _This article explains CLI commands that can be used to verify working of a GRE tunnel._ knowledgebase.paloaltonetworks.com](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA14u000000wkpBCAQ "https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA14u000000wkpBCAQ")[](https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA14u000000wkpBCAQ)

Cisco Live 2023 Las Vegas — <https://www.ciscolive.com/on-demand/on-demand-details.html?#/session/1686177773738001VLzw>

![](/assets/images/aws-transit-gateway-connect-to-palo-alto-firewalls-sd-wan-like-architecture-4.png)

By [Georgi_V](https://www.linkedin.com/in/gvoden/) on [June 30, 2023].
