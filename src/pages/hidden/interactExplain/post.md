---
template: post.html
title: What Have Language Models Learned?
summary: By asking language models to fill in the blank, we can probe their understanding of the world.
shareimg: https://pair.withgoogle.com/explorables/images/fill-in-the-blank.png
shareimgabstract: https://pair.withgoogle.com/explorables/images/fill-in-the-blank-abstract.png
permalink: /fill-in-the-blank/
date: 2021-07-28
---

# Cattle or Clothes?

Besides Hamlet's existential dread, the text BERT was trained on also contains more patterns: 

<div class='sent texas'></div>

Cattle and horses aren't top purchase predictions in every state, though! In New York, some of the most likely words are clothes, books and art:

<div class='sent new-york'></div>

There are more than 30,000 words, punctuation marks and word fragments in BERT's [vocabulary](https://huggingface.co/transformers/tokenizer_summary.html). Every time BERT fills in a hidden word, it assigns each of them a probability. By looking at how slightly different sentences shift those probabilities, we can get a glimpse at how purchasing patterns in different places are understood.     

<div class='pair texas-ohio'></div>

You can **edit these sentences**. Or try one of these comparisons to get started: <span class='texas-ohio-alts'></span>

To the extent that a computer program can "know" something, what does BERT know about where you live? 


