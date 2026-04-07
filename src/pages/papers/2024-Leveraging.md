---
title: "Subjective Similarity of AI Written Content"
date: 2023-03-30 
draft: false
toc: false
layout: post
location: online
permalink: /papers/2023-Learning
author_profile: false
tags:
  - Reinforcement Learning
  - Cognitive Modeling
projects:
  - reinforcementLearning
  - cognitiveModeling
---

# Leveraging a Cognitive Model to Measure Subjective Similarity of Human and GPT-4 Written Content

## Paper Abstract 

Cosine similarity between two documents can be computed using token embeddings formed by Large Language Models (LLMs) such as GPT-4, and used to categorize those documents across a range of uses. However, these similarities are ultimately dependent on the corpora used to train these LLMs, and may not reflect subjective similarity of individuals or how their biases and constraints impact similarity metrics. This lack of cognitively-aware personalization of similarity metrics can be particularly problematic in educational and recommendation settings where there is a limited number of individual judgements of category or preference, and biases can be particularly relevant. To address this, we rely on an integration of an Instance-Based Learning (IBL) cognitive model with LLM embeddings to develop the Instance-Based Individualized Similarity (IBIS) metric. This similarity metric is beneficial in that it takes into account individual biases and constraints in a manner that is grounded in the cognitive mechanisms of decision making. To evaluate the IBIS metric, we also introduce a dataset of human categorizations of emails as being either dangerous (phishing) or safe (ham). This dataset is used to demonstrate the benefits of leveraging a cognitive model to measure the subjective similarity of human participants in an educational setting.