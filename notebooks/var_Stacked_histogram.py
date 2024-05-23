import ROOT

def create_lorentz_vector(pt, eta, phi, m):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, m)
    return lv

def process_file(file_path, tree_name):
    # Open the ROOT file in read mode
    file_1 = ROOT.TFile(file_path, "READ")
    tree = file_1.Get(tree_name)

    # Array to store the invariant mass values
    invariant_masses = []

    if not tree:
        print(f"Tree not found in file: {file_path}")
    else:
        for event in tree:
            lead_bjet_pt = event.lead_bjet_pt
            lead_bjet_eta = event.lead_bjet_eta
            lead_bjet_phi = event.lead_bjet_phi
            lead_bjet_mass = event.lead_bjet_mass
            sublead_bjet_pt = event.sublead_bjet_pt
            sublead_bjet_eta = event.sublead_bjet_eta
            sublead_bjet_phi = event.sublead_bjet_phi
            sublead_bjet_mass = event.sublead_bjet_mass

            # Create Lorentz vectors for the lead and sublead b-jets
            lv1 = create_lorentz_vector(lead_bjet_pt, lead_bjet_eta, lead_bjet_phi, lead_bjet_mass)
            lv2 = create_lorentz_vector(sublead_bjet_pt, sublead_bjet_eta, sublead_bjet_phi, sublead_bjet_mass)

            # Calculate the total Lorentz vector
            lv = lv1 + lv2

            # Get the invariant mass
            invariant_mass = lv.M()

            # Store the invariant mass
            invariant_masses.append(invariant_mass)

    # Close the ROOT file
    file_1.Close()

    # Return the invariant mass values
    return invariant_masses

# Data file path
data_file_path = "output_root/Data_EraE.root"
background_files = [
    ("output_root/GGJets.root", "Gluon-Gluon Jets"),
    ("output_root/GJetPt20To40.root", "GJet Pt20To40"),
    ("output_root/GJetPt40.root", "GJet Pt40")
]

# Tree and variable names
tree_name = "DiphotonTree/data_125_13TeV_NOTAG"

# Process data file
data_invariant_masses = process_file(data_file_path, tree_name)

# Process background files
background_hists = {}

# Colors for different backgrounds
background_colors = [ROOT.kBlue-9, ROOT.kOrange-2, ROOT.kYellow-7]

for background_file, bg_name in background_files:
    bg_invariant_masses = process_file(background_file, tree_name)
    bg_hist = ROOT.TH1F(f"hist_{bg_name}", f"{bg_name} Invariant Mass", 20, 80, 180)
    for mass in bg_invariant_masses:
        bg_hist.Fill(mass)
    bg_hist.SetFillColor(background_colors[len(background_hists)])
    background_hists[bg_name] = bg_hist

# Create a canvas
canvas = ROOT.TCanvas("canvas", "Invariant Mass", 800, 600)

# Draw the background histograms
stack = ROOT.THStack("stack", "Background Invariant Masses")
for bg_name, bg_hist in background_hists.items():
    stack.Add(bg_hist)

# Set the minimum value of the y-axis to 0 for each histogram in the stack
minimum_value = 0
for bg_hist in background_hists.values():
    bg_hist.SetMinimum(minimum_value)

# Draw the stack
stack.Draw("HIST")

# Create a histogram for data invariant masses
hist_data = ROOT.TH1F("hist_data", "", 20, 80, 180)
for mass in data_invariant_masses:
    hist_data.Fill(mass)

# Set the minimum value of the y-axis to 0 for the data histogram
hist_data.SetMinimum(0)

# Set histogram style for data
hist_data.SetMarkerStyle(20)
hist_data.SetMarkerSize(1.2)
hist_data.SetMarkerColor(ROOT.kBlack)

# Draw the data histogram on top
hist_data.Draw("SAME E1")

# Add legend
legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
legend.AddEntry(hist_data, "Data", "lep")
for bg_name, bg_hist in background_hists.items():
    legend.AddEntry(bg_hist, bg_name, "f")
legend.Draw()

# Add labels and title
stack.GetXaxis().SetTitle("Invariant Mass [GeV]")
stack.GetYaxis().SetTitle("Events")
stack.SetTitle("Stacked Backgrounds vs Data")

# Draw ratio plot
canvas.cd()
pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
pad2.SetTopMargin(1)
pad2.SetBottomMargin(0.3)
pad2.Draw()
pad2.cd()

# Create a histogram for the ratio
hist_ratio = hist_data.Clone("hist_ratio")
mc_hist = stack.GetStack().Last().Clone("mc_hist")

hist_ratio.Divide(mc_hist)
hist_ratio.SetMarkerStyle(20)
hist_ratio.SetMarkerSize(1.2)
hist_ratio.SetMarkerColor(ROOT.kBlack)

# Remove statistics box from the ratio plot
hist_ratio.SetStats(0)

# Increase text size for labels and titles
hist_ratio.GetXaxis().SetLabelSize(0.1)
hist_ratio.GetXaxis().SetTitleSize(0.12)
hist_ratio.GetYaxis().SetLabelSize(0.1)
hist_ratio.GetYaxis().SetTitleSize(0.12)

# Draw the ratio histogram
hist_ratio.Draw("ep")

# Add labels and title for the ratio plot
hist_ratio.GetXaxis().SetTitle("M_{bb} [GeV]")
hist_ratio.GetYaxis().SetTitle("Data / MC")

# Set y-axis range and divisions
hist_ratio.SetMinimum(-2)
hist_ratio.SetMaximum(2)  # Adjust maximum as needed
hist_ratio.GetYaxis().SetNdivisions(505)  # Increase divisions for better visibility

# Save the canvas as a PDF file
canvas.Print('/afs/cern.ch/user/s/sraj/sraj/www/CUA/HH-bbgg',"invariant_mass_plot.pdf")

# Show the canvas
canvas.Draw()

