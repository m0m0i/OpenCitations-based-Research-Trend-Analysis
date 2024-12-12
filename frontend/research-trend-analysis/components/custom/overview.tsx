import { motion } from "framer-motion";

import { LogoGoogle, MessageIcon } from "./icons";

export const Overview = () => {
  return (
    <motion.div
      key="overview"
      className="max-w-[500px] mt-20 mx-4 md:mx-0"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ delay: 0.5 }}>
      <div className="border-none bg-muted/50 rounded-2xl p-6 flex flex-col gap-4 text-zinc-500 text-sm dark:text-zinc-400 dark:border-zinc-700">
        <p className="flex flex-row justify-center gap-4 items-center text-zinc-900 dark:text-zinc-50">
          <LogoGoogle />
          <span>+</span>
          <MessageIcon />
        </p>
        <p>
          Our project aims to analyze citation patterns within the OpenCitations
          dataset to identify and visualize emerging research trends across
          various academic fields. By leveraging additional datasets from
          Wikidata and DBpedia, we will track the growth of citations in
          specific research areas, pinpoint influential publications and
          authors, and visualize the evolution of these fields over time. We
          will focus on developing innovative metrics for citation analysis,
          such as measuring citation velocity and impact score, which will help
          capture the nuances of how different research areas develop and shift.
          Our interactive visualizations will allow users to explore trends
          dynamically, enhancing their understanding of the academic landscape.
          To ensure feasibility within our time constraints, we will concentrate
          on a specific research domain, allowing for in-depth analysis. Our
          goal is to create a comprehensive tool that not only provides valuable
          insights into citation dynamics but also contributes to the academic
          community by fostering a deeper understanding of research impact and
          future directions. Ultimately, our project aims to empower researchers
          and institutions to make informed decisions based on evolving research
          trends.
        </p>
      </div>
    </motion.div>
  );
};
