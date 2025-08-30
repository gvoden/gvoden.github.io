---
layout: post
title: "Snyk — The Big Fix and how to make it to the top as a DevSecOps Engineer"
date: 2023-03-22T18:13:36
---

* * *

![](/assets/images/snyk-the-big-fix-and-how-to-make-it-to-the-top-as-a-devsecops-engineer-0.png)

* * *

### What is this all about?

_From Snyk Blog:_ The Big Fix is a month-long fix-a-thon that brings developers and security professionals together to fix vulnerabilities and help make the software ecosystem safer for everyone! The Big Fix helps any developer (with any level of security experience) find and fix vulnerabilities in their software. <https://snyk.io/blog/the-big-fix-2023/>

I am not a developer however I work as a DevSecOps engineer so this immediately peaked my interest. I had used Snyk at work and it’s a pretty comprehensive AppSec platform that can scan your code, dependencies, embed in your IDE, GitHub, Kubernetes, container registries and so on. I saw this as an opportunity to have some fun with the platform and take my security skills even further. AppSec is a hot topic and it is made out to be this exclusive niche of InfoSec where only the super coders are allowed. I will dispel this myth in this blog post. It is all about risk management and how to leverage the tools at your disposal.

### How to get started?

This was super easy, following these steps:

  1. Sign-up for The Big Fix here: [**https://snyk.io/events/the-big-fix**](https://snyk.io/events/the-big-fix#sign-up)
  2. Register for a free Snyk account (<https://snyk.io/plans/>)
  3. Add your projects to The Big Fix (these can be any projects, such as public GitHub, Azure DevOps repos etc. For public GitHub, you can fork a repo and use the fork as a project if the repo does not allow direct changes).

![](/assets/images/snyk-the-big-fix-and-how-to-make-it-to-the-top-as-a-devsecops-engineer-1.png)Add a project from your personal Snyk tenant:

I imported some of my personal GitHub repos that I had used in other projects. Snyk would immediately add the projects and scan them for vulnerabilities. It has a very comprehensive scoring system as well as out of the box solutions on how to fix vulnerabilities in code, Kubernetes RBAC etc. I played around updating a few YAML definitions that had excessive permissions or allowed pods to run as root. However I quickly realized this would not get me enough points in the competition and just does not scale.

### Strategy change

I decided to search public GitHub for purposefully vulnerable projects that I could use for the competition and that are also a great learning resource for AppSec, here are a few:

[**GitHub - ne0z/DamnVulnerableMicroServices: This is vulnerable microservice written in many language…**  
 _Damn Vulnerable Microservices (DVMS) is microservices that is damn vulnerable with no exception. These project goals…_ github.com](https://github.com/ne0z/DamnVulnerableMicroServices "https://github.com/ne0z/DamnVulnerableMicroServices")[](https://github.com/ne0z/DamnVulnerableMicroServices)

[**GitHub - vulhub/vulhub: Pre-Built Vulnerable Environments Based on Docker-Compose**  
 _Vulhub is an open-source collection of pre-built vulnerable docker environments. No pre-existing knowledge of docker is…_ github.com](https://github.com/vulhub/vulhub "https://github.com/vulhub/vulhub")[](https://github.com/vulhub/vulhub)

[**GitHub - madhuakula/kubernetes-goat: Kubernetes Goat is a "Vulnerable by Design" cluster…**  
 _Kubernetes Goat is a "Vulnerable by Design" cluster environment to learn and practice Kubernetes security using an…_ github.com](https://github.com/madhuakula/kubernetes-goat "https://github.com/madhuakula/kubernetes-goat")[](https://github.com/madhuakula/kubernetes-goat)

Turns out that Snyk is really effective and efficient when it comes to Docker image vulnerabilities. For example looking at this specific image, you would notice that Snyk would suggest minor or alternative upgrades you could apply and that would immediately kill off 100+ vulnerabilities:

![](/assets/images/snyk-the-big-fix-and-how-to-make-it-to-the-top-as-a-devsecops-engineer-2.png)

You can then open a fix PR (pull request) in order to apply the update in your own repo (Azure DevOps in this scenario):

This would take you to Azure DevOps where you could review the change and then approve and merge it into your main branch:

![](/assets/images/snyk-the-big-fix-and-how-to-make-it-to-the-top-as-a-devsecops-engineer-3.png)Azure DevOps Pull Request

Snyk would automatically re-scan your repo and report the fixed vulnerabilities to Bix Fix website where your score will be calculated and added to the leaderboard. So as you can see, fixing container vulnerabilities is super easy as you do not have to research what base image to upgrade to and the tool will make recommendations for you. In the case of public GitHub, there is also a Snyk bot that can open PR automatically for you.

### Final Thoughts

I hope I was able to demonstrate how this fun exercise can teach you more about application security, prioritization and vulnerabilities found in containers in a very fun and gamified way. I am now waiting for my Snyk T-shirt that would be awarded to all participants who fixed at least one exploit or vulnerability.

Happy fixing! And check out the Snyk Learn portal to sharpen your AppSec skills and knowledge, it is a free resource: https://learn.snyk.io/

By [Georgi_V](https://www.linkedin.com/in/gvoden/) on [March 20, 2023].
