# CNS statistical reporting sources

Source review: 2026-09-20. CNS here means Cell, Nature, and Science. They do not share one statistical specification. The operational contract in this Skill is a repository synthesis; journal-specific submission compliance requires checking the named journal's current instructions and applicable article type.

## Nature

The [Nature Portfolio Reporting Summary](https://www.nature.com/documents/nr-reporting-summary-flat.pdf), Statistics and field-specific study-design sections, was retrieved directly. It requests per-group sample counts with unit definitions, repeated-measure identification, test sidedness, covariates, assumptions/corrections, estimates and variability or uncertainty. Inferential reporting includes test statistics, degrees of freedom where relevant, effect sizes, and suitable exact P values. It also covers hierarchical analyses, Bayesian priors/computation, sample-size decisions, exclusions, replication, randomization, and blinding.

Use these fields where applicable; explicitly disclose procedures not performed. The form's instructions govern actual submission wording, including its treatment of irrelevant fields. Internal `not_applicable` validation statuses are not text to paste into the form.

## Cell / Cell Press

Primary entry points: [STAR Methods](https://www.cell.com/star-methods), [authors guide](https://www.cell.com/star-authors-guide), and [Methods Guide](https://www.cell.com/pb-assets/journals/research/cell/methods/Methods%20Guide.pdf). Direct retrieval was blocked on the review date. The STAR Methods guide reproduced in [Sapienza's institutional document, pages 11–14](https://phd.uniroma1.it/dottorati/cartellaDocumentiWeb/1cf3fe41-2afc-42cb-9a8b-0d92eab69412.pdf) was readable; it is an older reproduced publisher document, not a verified current submission policy.

Its Quantification and Statistical Analysis section asks authors to identify analyses/software, explain exact n and its meaning, define summaries and precision measures, and locate those details in Methods/results/legends. It also requests the basis for significance, sample sizing, allocation, exclusions, and assumption assessment. Use this reporting structure as a baseline; verify current journal instructions before claiming Cell submission compliance.

## Science / AAAS

The current primary policy entry point is [Science Journals editorial policies, statistical analysis](https://www.science.org/content/page/science-journals-editorial-policies#statistical-analysis). Direct retrieval returned an access error on the review date; current flagship-specific wording remains unverified.

The official [Research author guidelines](https://spj.science.org/page/research/for-authors/) were available through indexed full text. Research is a Science Partner Journal, not Science. Its design/statistics sections support documenting sample-size/stopping decisions, prospective endpoints and exclusions, preprocessing, units, test/interval methods, multiplicity, assumptions, missingness, estimates and uncertainty, and complete test results. These are supporting guidance, not evidence that every Science journal mandates identical fields. Do not copy the page's apparent small-sample inequality or its mean-plus/minus-two-SD confidence-interval example as a computation rule.

Science's own [2014 editorial, Raising the bar](https://www.sciencemagazinedigital.org/sciencemagazine/04_july_2014?pg=9), was retrieved from its digital edition. It supports statistical scrutiny and unbiased retention of observations, but is not a current submission checklist.

## Repository application

The repository uses these reporting principles to make the approved analysis inspectable. Stable comparison IDs, structured checks, SHA-256 provenance, MATLAB production, and lifecycle predicates are local engineering conventions. No journal source above establishes a universal minimum n, mandatory t-test, alpha of 0.05, 95% interval, normality pretest, or mandatory power calculation for every study.

Specify only choices justified by the scientific question. Sample-size justification may use prospective power/precision, methodological precedent, or a fixed available dataset with explicit limits; distinguish these bases honestly. Missing journal access limits a compliance claim, not otherwise justified research work. Record the target journal, source URL, check date, access limitations, and applicable requirements with the figure plan or aggregation manifest; refresh the source when preparing a submission.
