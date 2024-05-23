# Invariant variables for the photon(mass, eta,phi, ...)



import ROOT


def create_lorentz_vector(pt, eta, phi, energy):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiE(pt, eta, phi, energy)
    return lv



def process_file(file_path, tree_name):
    file = ROOT.TFile(file_path, "READ")
    tree = file.Get(tree_name)

    invariant_masses = []

    if not tree:
        print(f"Tree not found in file: {file_path}")
    else:
        for event in tree:
            lead_pt = event.lead_pt
            lead_eta = event.lead_eta
            lead_phi = event.lead_phi
            lead_energyRaw = event.lead_energyRaw

            sublead_pt = event.sublead_pt
            sublead_eta = event.sublead_eta
            sublead_phi = event.sublead_phi
            sublead_energyRaw = event.sublead_energyRaw

            lv1 = create_lorentz_vector(lead_pt, lead_eta, lead_phi, lead_energyRaw)
            lv2 = create_lorentz_vector(sublead_pt, sublead_eta, sublead_phi, sublead_energyRaw)

            invariant_mass = (lv1 + lv2).M()
            invariant_masses.append(invariant_mass)

    file.Close()
    return invariant_masses




# File paths
data_file_paths = ["../output_root/Data_EraE.root", "../output_root/Data_EraF.root", "../output_root/Data_EraG.root"]
background_files = [
    ("../output_root/GGJets.root", "Gluon-Gluon Jets"),
    ("../output_root/GJetPt20To40.root", "GJet Pt20To40"),
    ("../output_root/GJetPt40.root", "GJet Pt40"),
    ("../output_root/GluGluHToGG.root", "H->gamma gamma"),
    ("../output_root/ttHToGG.root", "H->gamma gamma"),
    ("../output_root/VBFHToGG.root", "H->gamma gamma"),
    ("../output_root/VHToGG.root", "H->gamma gamma")
]


# Tree and variable names
tree_name = "DiphotonTree/data_125_13TeV_NOTAG"




# Process each data file
for data_file_path in data_file_paths:
    invariant_masses = process_file(data_file_path, tree_name)
    print(f"Invariant masses from {data_file_path}:")
    for mass in invariant_masses:
        print(mass)

# Process each background file
for file_path, background_name in background_files:
    invariant_masses = process_file(file_path, tree_name)
    print(f"Invariant masses from {background_name}:")
    for mass in invariant_masses:
        print(mass)
