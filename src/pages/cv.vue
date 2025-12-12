<script setup>
defineOptions({ name: 'CVPage' });

import Header from '@/components/header.vue'

const contacts = [{"label": "Google Scholar", "href": "https://scholar.google.com/citations?user=jktsx4EAAAAJ&hl=en"}, {"label": "Email", "href": "mailto:tailiamalloy@gmail.edu"}, {"label": "Personal Site", "href": "https://www.TailiaMalloy.com/"}, {"label": "ResearchGate", "href": "https://www.researchgate.net/profile/Tailia-Malloy"}, {"label": "LinkedIn", "href": "http://www.linkedin.com/in/TailiaMalloy"}];
const employmentHistory = [
  {
    period: '2025 – present',
    title: 'Research Associate, Natural Language Processing for Personality Diagnostics',
    organization: 'University of Luxembourg, Trustworthy Software Engineering, Interdisciplinary Center for Security, Reliability, and Trust.',
    details: 'Supervisors: Prof. Jaques Klein and Prof. Tegawendé F. Bissyande.'
  },
  {
    period: '2022 – 2025',
    title: 'Postdoctoral Researcher, Cognitive Modeling and Human-Computer Interaction',
    organization: 'Carnegie Mellon University, Social and Decision Sciences, Dynamic Decision Making Lab; AI Institute for Societal Decision Making.',
    details: 'Supervisor: Prof. Cleotilde Gonzalez.'
  },
  {
    period: '2019 – 2022',
    title: 'External Researcher, Reinforcement Learning Group',
    organization: 'IBM Research AI, RPI-IBM Artificial Intelligence Research Collaboration.',
    details: 'Supervisors: Dr. Tim Klinger and Dr. Gerald Tesauro.'
  },
  {
    period: '2018 – 2022',
    title: 'PhD Student and Research Assistant, Adaptive Computational Cognition Lab',
    organization: 'Rensselaer Polytechnic Institute, Department of Cognitive Science.',
    details: 'Supervisor: Assoc. Prof. Chris R. Sims.'
  },
  {
    period: '2017 – 2018',
    title: 'Research Assistant and Volunteer, Sensory Perception & Interaction Research Group',
    organization: 'University of British Columbia, Department of Computer Science; School of Population and Public Health.',
    details: 'Supervisors: Prof. Karon MacLean and Prof. Peter Danielson.'
  },
  {
    period: '2016 – 2017',
    title: 'Research Assistant and Lab Software Developer',
    organization: 'University of Innsbruck, Institute for Experimental Physics; Innsbruck Institute for Quantum Optics and Quantum Information.',
    details: 'Supervisors: Prof. Tracy Northup and Prof. Rainer Blatt.'
  }
];

const education = [
  {
    year: '2022',
    degree: 'Ph.D., Rensselaer Polytechnic Institute, Cognitive Science.',
    advisor: 'Advised by Chris R. Sims.',
    thesis: 'Thesis: Resource Rational Cognitive Modelling: An Information Theoretic Approach.'
  },
  {
    year: '2020',
    degree: 'M.Sc., Rensselaer Polytechnic Institute, Cognitive Science.',
    advisor: 'Advised by Chris R. Sims.',
    thesis: 'Thesis: Modelling Learning and Decision Making Under Information Processing Constraints.'
  },
  {
    year: '2018',
    degree: 'B.Sc., University of British Columbia.',
    advisor: null,
    thesis: 'Cognitive Systems: Computational Intelligence and Design with a dual degree in Philosophy.'
  }
];

const publications = {
  journals: [
    'Du, Yinuo; Baptiste Prebot; Tailia Malloy; Fei Fang; Cleotilde Gonzalez. "Experimental Evaluation of Cognitive Agents for Collaboration in Human-Autonomy Cyber Defense Teams." Computers and Human Behavior: Artificial Agents, 2025.',
    'Malloy, Tailia; Laura Bernardy; Omar El Bachyr; Fred Phillipy; Jordan Samhi; Jacques Klein; Tegawendé F. Bissyande. "You Got Phished! Analyzing how to Provide Useful Feedback in Anti-Phishing Training with LLM Teacher Models." Under review for MDPI Electronics, 2025.',
    'Malloy, Tailia; Maria Ferriera; Fei Fang; Cleotilde Gonzalez. "Improving Online Anti-Phishing Training Using Cognitive Large Language Models." Computers and Human Behavior, 2025.',
    'Du, Yinuo; Baptiste Prebot; Tailia Malloy; Cleotilde Gonzalez. "A Cyber-War Between Bots: Cognitive Attackers are More Challenging for Defenders than Strategic Attackers." ACM Transactions on Social Computing, 2024.',
    'Malloy, Tailia; Cleotilde Gonzalez. "Applying Generative Artificial Intelligence to Cognitive Models of Decision Making." Frontiers in Psychology, 2024.',
    'Malloy, Tailia; Chris R. Sims. "Efficient Visual Representations in Learning and Decision Making." Psychological Review, 2024.',
    'Malloy, Tailia; Chris R. Sims. "A Beta-Variational Auto-Encoder Model of Human Visual Representation Formation in Utility-Based Learning." Journal of Vision, 2022.'
  ],
  proceedings: [
    'Malloy, Tailia; David Hagmann; Cleotilde Gonzalez. "Hierarchical Instance-Based Learning for Decision Making from Delayed Feedback." 2025 Conference in Cognitive Science, 2025.',
    'Malloy, Tailia; Maria Ferriera; Fei Fang; Cleotilde Gonzalez. "Using Cognitive Models to Improve Training Against Human and GPT-4 Generated Social Engineering Attacks." International Conference on Human Computer Interaction, 2025.',
    'Malloy, Tailia; Roderick Seow; Cleotilde Gonzalez. "Modeling Attention during Dimensional Shifts with Counterfactual and Delayed Feedback." Reinforcement Learning and Decision Making, 2025.',
    'Malloy, Tailia; Maria Ferriera; Fei Fang; Cleotilde Gonzalez. "Leveraging a Cognitive Model to Measure Subjective Similarity of Human and GPT-4 Written Content." Conference on Natural Language Learning, 2024.',
    'Malloy, Tailia; Cleotilde Gonzalez. "Learning to Defend by Attacking (and Vice-Versa): Transfer Learning in Cyber-Security Games." IEEE European Symposium on Security and Privacy Workshop Series, 2023.',
    'Malloy, Tailia; Yinuo Du; Fei Fang; Cleotilde Gonzalez. "Accounting for Transfer of Learning in Human Behavior Models." Human Computation and Crowdsourcing, 2023.',
    'Malloy, Tailia; Yinuo Du; Fei Fang; Cleotilde Gonzalez. "Generative Environment-Representation Instance-Based Learning: A Cognitive Model." AAAI Symposium on Integration of Cognitive Architectures and Generative Models, 2023.',
    'Malloy, Tailia; Tim Klinger; Chris R. Sims. "Modeling Human Reinforcement Learning with Disentangled Visual Representations." Reinforcement Learning and Decision Making, 2022.',
    'Malloy, Tailia; Chris R. Sims; Tim Klinger; Matthew D. Riemer; Miao Liu; Gerald Tesauro. "Learning in Factored Domains with Information-Constrained Visual Representations." NeurIPS Workshop on Information-Theoretic Principles in Cognitive Systems, 2022.',
    'Malloy, Tailia; Tim Klinger; Miao Liu; Matthew Riemer; Gerald Tesauro; Chris R. Sims. "Consolidation via Policy Information Regularization in Deep RL for Multi-Agent Games." AAAI Reinforcement Learning in Games Workshop, 2021.',
    'Malloy, Tailia; Tim Klinger; Miao Liu; Gerald Tesauro; Matthew Riemer; Chris R. Sims. "Modeling Capacity-Limited Decision Making Using a Variational Autoencoder." Proceedings of the Annual Meeting of the Cognitive Science Society, 2021.',
    'Malloy, Tailia; Tim Klinger; Miao Liu; Gerald Tesauro; Matthew Riemer; Chris R. Sims. "RL Generalization in a Theory of Mind Game Through a Sleep Metaphor (Student Abstract)." AAAI Student Abstract Workshop, 2021.',
    'Malloy, Tailia; Chris R. Sims. "Modelling Visual Decision Making Using a Variational Autoencoder." Proceedings of the 19th International Conference on Cognitive Modelling, 2021, pp. 177-183.',
    'Malloy, Tailia; Chris R. Sims; Tim Klinger; Miao Liu; Matthew Riemer; Gerald Tesauro. "Capacity-Limited Decentralized Actor-Critic for Multi-Agent Games." IEEE Conference on Games, 2021.',
    'Malloy, Tailia; Chris R. Sims. "Modelling Human Information Processing Limitations in Learning Tasks with Reinforcement Learning." Proceedings of the 18th International Conference on Cognitive Modelling, Applied Cognitive Science Lab, Penn State, 2020, pp. 159-160.',
    'Malloy, Tailia; Chris R. Sims; Tim Klinger; Miao Liu; Matthew Riemer; Gerald Tesauro. "Deep RL with Information Constrained Policies: Generalization in Continuous Control." arXiv preprint arXiv:2010.04646, 2020.'
  ]
};

const grants = [
  '2024-2025 - $180,000 Co-PI (Invited Presentation). Carnegie Bosch Institute Postdoctoral Research Grant: "Improving Cyber Defense Against Foundation Models with Cognitive Models." Introduced a framework for integrating foundation models with cognitive modeling to mitigate adversarial misuse.',
  '2023-2024 - $20,000 PI (Awarded). Microsoft Accelerating Foundation Models Research Grant: "Personalized Education with Foundation Models via Cognitive Modeling." Led a study on human educational tools using ChatGPT and cognitive modeling, supported by Azure credits.',
  '2024-2025 - $180,000 Co-PI (Applied). Oak Ridge Institute for Science and Education Postdoctoral Fellowship: "Applying Cognitive Models and Generative Artificial Intelligence to Counter Automated Online Influence Campaigns." Proposed defenses against influence operations that leverage generative models.',
  '2024-2025 - $180,000 Co-PI (Applied). Oak Ridge Institute for Science and Education Postdoctoral Fellowship: "Improving Human-AI Collaboration in Intelligence Analysis by Integrating Cognitive Models and Generative Artificial Intelligence." Focused on enhancing analytical workflows through joint cognitive and foundation model approaches.',
  '2019-2022 - ~$300,000 Co-PI (Awarded). RPI-IBM Artificial Intelligence Research Collaboration Fellowship: "Human Inspired Reinforcement Learning." Provided tuition and salary support across the PhD program.'
];

const teaching = [
  '2025 - Code, Create, & Innovate with AI. Guided students from Python programming and prompt engineering to large language model APIs and retrieval-augmented generation pipelines.',
  '2024 - Human and Machine Decisions from Experience, Carnegie Mellon University, Department of Social and Decision Sciences. Head lecturer and course designer for an upper-year course on experiential decision making in humans and machines.'
];

const awards = [
  '2025 - Keynote: "Human-AI Interdependence in Security and Privacy" delivered at the TU Delft Workshop on Generative AI and Privacy/Security.',
  '2025 - Best Paper Award for "Using Cognitive Models to Improve Training Against Human and GPT-4 Generated Social Engineering Attacks" at Human Computer Interaction International (Cybersecurity, Privacy, and Trust).'
];

const mentoring = [
  '2023-2025 - Graduate mentor for the Adaptive Computational Cognition Lab (RPI) and the Dynamic Decision Making Lab (CMU), supporting grant proposals, study design, manuscript preparation, and data analysis.',
  '2022-2025 - Undergraduate mentor at Carnegie Mellon University and New York University; senior mentor for the University of British Columbia Cognitive Systems program, advising on research, internships, and industry paths.'
];

const committee = [
  'Association for the Advancement of Artificial Intelligence Program Committee (2025).',
  'Association for the Advancement of Artificial Intelligence Demonstration Program.'
];

const journalReviewer = [
  'Nature Communications Psychology',
  'Institute of Electrical and Electronics Engineers journals',
  'Journal of Cognitive Science',
  'Nature Scientific Reports',
  'Discover Sustainability',
  'PLOS Computational Biology'
];

const bookReviewer = ['CRC Press: Taylor & Francis Group'];

const memberships = [
  'Cognitive Science Society',
  'American Psychological Association',
  'Institute of Electrical and Electronics Engineers',
  'Association for the Advancement of Artificial Intelligence',
  'Association for Computing Machinery',
  'Association for Computational Linguistics'
];

const presentations = [
  {
    year: '2025',
    talks: [
      '"Human-AI Interdependence in Security and Privacy" - TU Delft Workshop on Generative AI and Privacy/Security.',
      '"Hierarchical Instance-Based Learning for Decision Making from Delayed Feedback." - Cognitive Science Society Conference.',
      '"Using Cognitive Models to Improve Training Against Human and GPT-4 Generated Social Engineering Attacks." - Human Computer Interaction International (Cybersecurity, Privacy, and Trust).',
      '"Modeling Attention during Dimensional Shifts with Counterfactual and Delayed Feedback." - Reinforcement Learning and Decision Making Conference.'
    ]
  },
  {
    year: '2024',
    talks: [
      '"Grounding Human-AI Collaboration with Cognitive Models" - Leiden Institute of Advanced Computer Science, University of Leiden.',
      '"Leveraging a Cognitive Model to Measure Subjective Similarity of Human and GPT-4 Written Content" - Conference on Natural Language Learning (co-located with EMNLP).',
      '"Efficient Visual Representations for Learning and Decision Making" - Human and Machine Cognition Lab, University of Tubingen.',
      '"Cognitive Large Language Models" - Dynamic Decision Making Lab, Carnegie Mellon University.',
      '"Improving Human-LLM Collaboration in Cybersecurity using Cognitive Models" - Software Engineering Institute, Carnegie Mellon University.',
      '"Human AI Teaming in Cyberdefense" - Cybersecurity Assurance for Teams of Computers and Humans Multi-University Research Initiative.',
      '"Efficient Visual Representations for Learning and Decision Making" - Dynamic Decision Making Lab, Carnegie Mellon University.',
      '"Improving Cyber Defense Against Foundation Models with Cognitive Models" - Carnegie Bosch Institute.',
      '"Cognitive Modeling of Decision Making in Cybersecurity" - Cognitive Security Institute.',
      '"Computational Behavior Modeling" - University of Virginia course on Computational Behavior Modeling.'
    ]
  },
  {
    year: '2023',
    talks: [
      '"Accounting for Transfer of Learning Using Human Behavior Models" - AAAI Conference on Human Computation and Crowdsourcing (HCOMP 2024).',
      '"Phishing Education and Detection: Integrating Large Language and Cognitive Models" - Army Research Office Conference.',
      '"Learning to Defend by Attacking (and Vice-Versa): Transfer of Learning in Cyber-Security Games" - IEEE European Symposium on Security and Privacy.',
      '"Designing Effective Masking Strategies for Cyberdefense through Human Experimentation and Cognitive Models in CyberVan" - Army Research Laboratory Conference.',
      '"Comparing Models of Dynamic Adaptation from Crowd-Sourced Human Decision-Making" - University of Alicante.',
      '"Overcoming Biases and Constraints in Multi-Agent Games" - University of Alicante.',
      '"Generative Environment-Representation Instance-Based Learning: A Cognitive Model" - AAAI Conference on Artificial Intelligence Fall Symposium Series.'
    ]
  },
  {
    year: '2022',
    talks: [
      '"Resource Rational Cognitive Modeling: An Information Theoretic Approach" - PhD Thesis Defense, Rensselaer Polytechnic Institute.',
      '"A Beta-Variational Auto-Encoder Model of Human Visual Representation Formation in Utility-Based Learning" - Vision Sciences Society.',
      '"Learning in Factored Domains with Information-Constrained Visual Representations" - NeurIPS Workshop on Information-Theoretic Principles in Cognitive Systems.'
    ]
  },
  {
    year: '2021',
    talks: [
      '"Theory of Mind Planning" - Neuro-Symbolic AI Workshop, IBM Research AI.',
      '"Human Inspired RL: Theory of Mind Games" - RPI-IBM Artificial Intelligence Horizons Network Scholar Seminar Series.'
    ]
  },
  {
    year: '2020',
    talks: [
      '"Deep RL with Information Constrained Policies: Generalization in Continuous Control" - Pompeu Fabra University, Theoretical and Cognitive Neuroscience.'
    ]
  }
];
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
      <ul class="space-y-4">
        <li v-for="role in employmentHistory" :key="role.period + role.title" class="space-y-1">
          <p><strong>{{ role.period }}</strong> · {{ role.title }}</p>
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ role.organization }}</p>
          <p v-if="role.details" class="text-sm text-gray-700 dark:text-gray-300">{{ role.details }}</p>
        </li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Education</h2>
      <ul class="space-y-4">
        <li v-for="item in education" :key="item.year + item.degree" class="space-y-1">
          <p><strong>{{ item.year }}</strong> · {{ item.degree }}</p>
          <p v-if="item.advisor" class="text-sm text-gray-700 dark:text-gray-300">{{ item.advisor }}</p>
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ item.thesis }}</p>
        </li>
      </ul>
    </div>

    <div class="mb-8 space-y-6">
      <h2 class="text-2xl font-semibold">Publications & Proceedings</h2>
      <div>
        <h3 class="font-medium mb-2">Journal Articles</h3>
        <ol class="list-decimal pl-6 space-y-2">
          <li v-for="(item, idx) in publications.journals" :key="'journal-'+idx">{{ item }}</li>
        </ol>
      </div>
      <div>
        <h3 class="font-medium mb-2">Conference Proceedings</h3>
        <ol class="list-decimal pl-6 space-y-2">
          <li v-for="(item, idx) in publications.proceedings" :key="'proceeding-'+idx">{{ item }}</li>
        </ol>
      </div>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Grants & Fellowships</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in grants" :key="'grant-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Teaching</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in teaching" :key="'teach-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Mentoring</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in mentoring" :key="'mentor-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Awards & Keynotes</h2>
      <ul class="list-disc pl-6 space-y-2">
        <li v-for="(item, idx) in awards" :key="'award-'+idx">{{ item }}</li>
      </ul>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-3">Service</h2>
      <div class="space-y-4">
        <div>
          <h3 class="font-medium">Editorial/Committee</h3>
          <ul class="list-disc pl-6 space-y-1">
            <li v-for="(item, idx) in committee" :key="'committee-'+idx">{{ item }}</li>
          </ul>
        </div>
        <div>
          <h3 class="font-medium">Journal Reviewer</h3>
          <ul class="list-disc pl-6 space-y-1">
            <li v-for="(item, idx) in journalReviewer" :key="'jr-'+idx">{{ item }}</li>
          </ul>
        </div>
        <div>
          <h3 class="font-medium">Book Reviewer</h3>
          <ul class="list-disc pl-6 space-y-1">
            <li v-for="(item, idx) in bookReviewer" :key="'br-'+idx">{{ item }}</li>
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

    <div class="mb-8 space-y-4">
      <h2 class="text-2xl font-semibold">Presentations & Invited Lectures</h2>
      <div v-for="section in presentations" :key="section.year" class="space-y-2">
        <h3 class="font-medium">{{ section.year }}</h3>
        <ul class="list-disc pl-6 space-y-1">
          <li v-for="(item, idx) in section.talks" :key="section.year + '-' + idx">{{ item }}</li>
        </ul>
      </div>
    </div>
  </section>
  </div>
</template>
