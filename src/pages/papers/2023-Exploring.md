---
title: "Exploring the Path from Instructions to Rewards"
date: 2023-06-30
draft: false
toc: false
layout: post
location: online
permalink: /papers/2023-Exploring
author_profile: false
tags:
  - Large Language Models
  - Cognitive Modeling
projects:
  - reinforcementLearning
  - artificialIntelligence 
---

# Exploring the path from instructions to rewards with large language models in instance-based learning

## Paper Abstract 

A prominent method to model human learning is through experiential learning, where decisions are influenced by the outcomes observed in previous actions. The decisions-from-experience approach often excludes other forms of learning in humans, such as learning from descriptive information. In humans, descriptive information can enhance learning by providing a denser signal, achieved through understanding the relationship between intermediate decisions and their future outcomes, instead of relying solely on observed outcomes. To account for experiential and descriptive information, we propose the use of large language models (LLMs) to convert descriptive information into dense signals that can be used by computational models that learn from experience. Building on past work in cognitive modeling, we utilize task instructions and prompt an LLM to define and quantify the critical actions an agent must take to succeed in the task. In an initial experiment, we test this approach using an Instance-Based Learning cognitive model of experiential decisions in a gridworld task. We demonstrate how the LLM can be prompted to provide a series of actions and relative values given the task instructions, then show how these values can be used in place of sparse outcome signals to improve the model’s learning of the task significantly.