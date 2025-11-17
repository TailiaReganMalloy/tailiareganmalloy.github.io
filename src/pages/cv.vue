<script setup>
defineOptions({ name: 'CVPage' });

import Header from '@/components/header.vue'

const contacts = [{"label": "Google Scholar", "href": "https://scholar.google.com/citations?user=jktsx4EAAAAJ&hl=en"}, {"label": "Email", "href": "mailto:tailiamalloy@gmail.edu"}, {"label": "Personal Site", "href": "https://www.TailiaMalloy.com/"}, {"label": "ResearchGate", "href": "https://www.researchgate.net/profile/Tailia-Malloy"}, {"label": "LinkedIn", "href": "http://www.linkedin.com/in/TailiaMalloy"}];
const employmentHistory = ["2025 –", "Research Associate Natural Language Processing for Personality D...Trust. Under Prof. Jaques Klein and Prof. Tegawendé F. Bissyande", "2022 – 2025", "Postdoctoral Researcher Cognitive Modeling and Human-Computer...e for Societal Decision Making. Under Prof. Cleotilde Gonzalez", "2019 – 2022", "External Researcher IBM Research AI, Reinforcement Learning G...ch Collaboration, Under Dr. Tim Klinger and Dr. Gerald Tesauro", "2018 – 2022", "PhD Student/Research Assistant Rensselaer Polytechnic Institu... Computational Cognition Lab, Under Assoc. Prof. Chris R. Sims", "2017 – 2018", "Research Assistant/Volunteer University of British Columbia, ...l of Population and Public Health Under Prof. Peter Danielson", "2016 – 2017", "Research Assistant/Lab Software Developer University of Innsbruck, Institute for Experimental Physics Under Prof. Tracy Northup; Innsbruck Institute for Quantum Optics and Quantum Information Under Prof. Rainer Blatt."];
const education = ["Ph.D., Rensselaer Polytechnic Institute Cognitive Science. Ad...ational Cognitive Modelling: An Information Theoretic Approach", "M.Sc., Rensselaer Polytechnic Institute Cognitive Science. Ad...g and Decision Making Under Information Processing Constraints", "B.Sc., University of British Columbia Cognitive Systems: Computational Intelligence and Design; Dual Degree in Philosophy"];
const publications = ["Y. Du, B. Prebot, T. Malloy, F. Fang, and G. Cleotilde, “Expe...e teams,” Computers and Human Behavior: Artiﬁcial Agents, 2025", "T. Malloy, M. Ferriera, F. Fang, and G. Cleotilde, “Improving...ive large language models,” Computers and Human Behavior, 2025", "Y. Du, B. Prebot, T. Malloy, and G. Cleotilde, “A cyber-war between bots: Cognitive attackers are more challenging for defenders than strategic attackers,” ACM Transactions on Social Computing, 2024.", "T. Malloy and C. Gonzalez, “Applying generative artiﬁcial intelligence to cognitive models of decision making,” Frontiers in Psychology, 2024.", "T. Malloy and C. R. Sims, “Eﬃcient visual representations in learning and decision making,” ...", "T. Malloy, H. David, and G. Cleotilde, “Hierarchical instance-based learning for decision making from delayed feedback,” in 2025 Conference in Cognitive Science, 2025.", "T. Malloy, M. Ferriera, F. Fang, and G. Cleotilde, “Using cognitive models to improve training against human and gpt-4 generated social engineering attacks,” in International Conference on Human Computer Interaction, 2025.", "T. Malloy, T. Klinger, M. Liu, G. Tesauro, M. Riemer, and C. R. Sims, “Modeling capacity-limited decision making using a variational autoencoder,” in Proceedings of the Annual Meeting of the Cognitive Science Society, vol. 43, 2021.", "T. Malloy, T. Klinger, M. Liu, G. Tesauro, M. Riemer, and C. R. Sims, “Rl generalization in a theory of mind game through a sleep metaphor (student abstract),” in AAAI Student Abstract Workshop, 2021.", "T. Malloy and C. R. Sims, “Modelling visual decision making using a variational autoencoder,” in Proceedings of the 19th International Conference on Cognitive Modelling, 2021, pp. 177–183.", "T. Malloy, C. R. Sims, T. Klinger, M. Liu, M. Riemer, and G. Tesauro, “Capacity-limited decentralized actor-critic for multi-agent games,” in IEEE Conference on Games, 2021.", "T. Malloy and C. R. Sims, “Modelling human information processing limitations in learning tasks with reinforcement learning,” in Proceedings of the 18th International Conference on Cognitive Modelling, Applied Cognitive Science Lab, PennState, 2020, pp. 159–160.", "T. Malloy, C. R. Sims, T. Klinger, M. Liu, M. Riemer, and G. Tesauro, “Deep rl with information constrained policies: Generalization in continuous control,” in arXiv preprint arXiv:2010.04646, 2020."];
const grants = ["Human and Machine Decisions from Experience: Carnegie Mellon ... and course designer for a new upper year undergraduate course", "Best Paper Award for the paper entitled ‘Using Cognitive Mode...rnational Conference area on Cybersecurity, Privacy, and Trust", "Mentor for Graduate Students Served as a mentor for graduate ..., designing studies, preparing manuscripts, or analyzing data", "Modeling and Learning Research Award ...", "CMU AI Institute for Societal Decision Making ...", "NSF/ONR/AFOSR-related support ...", "(additional items extracted from CV)"];
const awards = ["Editorial Board", "Frontiers in Computer Science Research Topic Editor (2026) Hu...ment of Artiﬁcial Intelligence conference Demo Program (2024)", "Additional awards/fellowships as listed in the CV..."];
const service = ["Editorial Board and Conference Service (see below)", "Additional service entries as listed in the CV..."];
const committee = ["Association for the Advancement of Artiﬁcial Intelligence Demonstration Program"]; 
const journalReviewer = ["Nature Communications Psychology, Institute of Electrical and..., Discover Sustainability Journal, PLOS Computational Biology"]; 
const bookReviewer = ["CRC Press: Taylor & Francis Group"]; 
const memberships = ["Cognitive Science Society, American Psychological Association...omputing Machinery, Association for Computational Linguistics"]; 
const presentations = ["“Using Cognitive Models to Improve Training Against Human and...action International area in Cybersecurity, Privacy, and Trust", "'Grounding Human-AI Collaboration with Cognitive Models' Leiden Institute of Advanced Computer Science University of Leiden", "“Leveraging a Cognitive Model to Measure Subjective Similarit...-located with Empirical Methods in Natural Language Processing", "“Eﬃcient Visual Representations for Learning and Decision Making Cognition Lab University of Tubingen", "“Cognitive Large Language Models: Dynamic Decision Making Lab Carnegie Mellon University", "“Improving Human-LLM Collaboration in Cybersecurity using Cognitive Models", "Software Engineering Institute Carnegie Mellon University", "“Human AI Teaming in Cyberdefense: Cybersecurity Assurance for Teams of Computers and Humans Multi-University Research Initiative", "“Eﬃcient Visual Representations for Learning and Decision Making:Dynamic Decision Making Lab Carnegie Mellon University", "“Improving Cyber Defense Against Foundation Models with Cognitive Models:Carnegie Bosch Institute", "“Cognitive Modeling of Decision Making in Cybersecurity: Cognitive Security Institute", "“Modeling Learning and Decision Making Under Information Processing Constraints: Rensselaer Polytechnic Institute", "“Deep RL with information constrained policies: Generalization in continuous control: Pompeu Fabra University: Theoretical and Cognitive Neuroscience"]; 
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header /> 

    <section class="pt-20 p-8 max-w-4xl mx-auto leading-relaxed">
    <h1 class="text-4xl font-bold mb-2">Tailia Malloy, Ph.D.</h1>
    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Contact</h2>
      <ul class="flex flex-wrap gap-3">
        <li v-for="c in contacts" :key="c.label">
          <a :href="c.href" target="_blank" rel="noopener" class="text-blue-600 hover:underline">{{ c.label }}</a>
        </li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Employment History</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in employmentHistory" :key="'emp-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Education</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in education" :key="'edu-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Publications & Proceedings</h2>
      <ul class="list-decimal pl-6 space-y-2">
        <li v-for="(item, idx) in publications" :key="'pub-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Grants & Fellowships</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in grants" :key="'grant-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Awards</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in awards" :key="'award-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Service</h2>
      <div class="space-y-4">
        <div>
          <h3 class="font-medium">Editorial/Committee</h3>
          <ul class="list-disc pl-6">
            <li v-for="(item, idx) in committee" :key="'committee-'+idx">{{ item }}</li>
          </ul>
        </div>
        <div>
          <h3 class="font-medium">Journal Reviewer</h3>
          <ul class="list-disc pl-6">
            <li v-for="(item, idx) in journalReviewer" :key="'jr-'+idx">{{ item }}</li>
          </ul>
        </div>
        <div>
          <h3 class="font-medium">Book Reviewer</h3>
          <ul class="list-disc pl-6">
            <li v-for="(item, idx) in bookReviewer" :key="'br-'+idx">{{ item }}</li>
          </ul>
        </div>
        <div>
          <h3 class="font-medium">Other Service</h3>
          <ul class="list-disc pl-6">
            <li v-for="(item, idx) in service" :key="'svc-'+idx">{{ item }}</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Memberships</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in memberships" :key="'mem-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Presentations & Invited Lectures</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in presentations" :key="'pres-'+idx">{{ item }}</li>
      </ul>
    </div>
  </section>
  </div>
</template>
