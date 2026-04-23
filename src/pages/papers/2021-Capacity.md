---
title: "Capacity Limited Deep Reinforcement Learning"
date: 2021-08-17
draft: false
toc: false
layout: post
location: online
permalink: /papers/2023-Learning
author_profile: false
tags:
  - Reinforcement Learning
  - Artificial Intelligence 
projects:
  - reinforcementLearning
  - artificialIntelligence
  - visualAritificalIntelligence
---

## Paper Abstract 

This paper explores information-theoretic constraints on methods for multi-agent reinforcement learning (MARL) in mixed cooperative and competitive games. Within this domain, decentralized training has been employed to increase learning sample efficiency. However, these approaches do not explicitly discourage complex policies, which can lead to overf itting. To address this, we apply an information theoretic constraint onto agents’ policies that discourages overly complex behaviour when it is not associated with a significant increase in reward. A second challenge in MARL is the non-stationarity of the environment introduced by other agents’ changing policies. Previous methods in MARL have sought to reduce the impact of non-stationarity by inferring other agents’ policies, but this can lead to over-fitting to previously observed behaviour. To avoid this, a similar information-theoretic constraint is applied onto the inference of other agents’ policies, resulting in a more robust estimate. We evaluate the effects of these information-theoretic constraints on a test suite of multi-agent games, and report an overall improvement in performance, with greater improvements found in competitive domains compared to cooperative games.