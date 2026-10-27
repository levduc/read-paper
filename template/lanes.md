# The three lanes

Each lane is one reviewer subagent. The lanes run in parallel and do not
see each other's reports. Each lane reads the whole paper but checks its
own focus in depth.

## theory

Correctness of the definitions, the model and the proofs.

- State the model: parties, adversary, what the adversary sees, the assumptions.
- Check each definition. Is it the standard one? If not, what does it change?
- Check each theorem and lemma step by step. Find the step that needs an
  unstated assumption.
- Check the security class: statistical, computational, ROM, standard model.
  Check the concrete bound, if the paper gives one.
- Check each bound and each asymptotic claim against the algorithm as written.
- Check the positioning against lower bounds and against the closest theory work.
- Build a small model or script when a claim needs a counter-example.

## systems

The evaluation and the numbers.

- Recompute each headline number from the paper's own formulas and tables.
- Check the baselines. Are they the state of the art? Are they tuned?
  Do the comparisons count the same thing on both sides?
- Check what is measured and what is modelled or extrapolated. At which scale?
- Check the setup: hardware, network, workload, number of runs, variance.
- Check for an artifact. Can someone else run it?
- Check that the cost model has every term (round trips, bytes, storage, compute).
- Fetch the baseline papers and compare their own numbers with the paper's quotes.

## protocol

The design, the threat model and deployment.

- Walk through one run, message by message. What does each party learn?
- Check what leaks: sizes, timing, counts, depth, access patterns, metadata.
- Check failure cases: a crash, a restore, a lost device, a second client,
  a malicious server, a replay.
- Check the interface: is it complete for the stated use?
- Find the closest system design. What does it already do?
- Check that each design choice is needed. Would a simpler choice do the same job?
