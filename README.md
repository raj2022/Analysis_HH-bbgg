#  HH $\longrightarrow X \longrightarrow YH \longrightarrow bb̄\gamma\gamma$
---

The studies related to the searches for beyond the Standard
Model (BSM) scalars X and Y in the cascade decay X $\longrightarrow$ HY, H being the SM Higgs boson and X $\longrightarrow$ HH process (where X is spin-0 and spin-2 particle) in the decay mode of $\gamma\gamma$bb̄ final state at center-of-mass energy of 13 TeV with CMS Run 3(Post EE) data corresponding to a total integrated luminosity of -- fb^{-1} .

A few major backgrounds are resonant backgrounds (ggH, VBFH, VH, ttH, b-quarks, where H decays to two photons) and non-resonant backgrounds ($\gamma\gamma$+Jets, $\gamma$+Jets(20 < $P_T$ < 40), $\gamma$+Jets( $P_T$ > 40), $\gamma\gamma$+ b-jets. For precise selection criteria, refer to the previous analysis note: [CMS AN-2020/162](https://cms.cern.ch/iCMS/jsp/db_notes/noteInfo.jsp?cmsnoteid=CMS%20AN-2020/162), which provides detailed descriptions of all cuts and selection methods used to isolate the signal from backgrounds.


## Framework Setup
---
The github repo is https://gitlab.cern.ch/hhbbgg/HiggsDNA and a updated and maintained documentation is available [here](https://higgs-dna.readthedocs.io/en/latest/index.html#). A tutorial can also found [here](https://indico.cern.ch/event/1360961/contributions/5777678/attachments/2788218/4861762/HiggsDNA_tutorial.pdf)
All of the setup for the analysis can be done using `source setup_analysis.sh`

All the files are present in the form of .parquet files which can be converted as given [here](https://higgs-dna.readthedocs.io/en/latest/output_grooming.html)

`python3 scripts/postprocessing/convert_parquet_to_root.py ../Run3_2022postEE_merged/GGJets.parquet ../output_root/GGJets.root mc 
`

