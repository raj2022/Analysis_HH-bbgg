# Data and Background plot (without Higgs)
# Integrated luminosity to be implemented from Golden Json, https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#2022_Analysis_Summary_Table 
# signal missing
# Data shouldn't be scaled/normalized. We need to normalize the Signal and the Monte Carlo samples. No need to normalize the data.
# Check Comments on the slide 
# Cross-section implemetation

import ROOT

def create_lorentz_vector(pt, eta, phi, m):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, m)
    return lv

def process_file(file_path, tree_name):
    # Open the ROOT file in read mode
    file_1 = ROOT.TFile(file_path, "READ")
    tree = file_1.Get(tree_name)

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


data_file_paths = ["../../output_root/Data_EraE.root", "../../output_root/Data_EraF.root", "../../output_root/Data_EraG.root"]

background_files = [
    ("../../output_root/GGJets.root", "Gluon-Gluon Jets"),
    ("../../output_root/GJetPt20To40.root", "GJet Pt20To40"),
    ("../../output_root/GJetPt40.root", "GJet Pt40"),
    ("../../output_root/GluGluHToGG.root", "H->gamma gamma"),
    ("../../output_root/ttHToGG.root", "H->gamma gamma"),
    ("../../output_root/VBFHToGG.root", "H->gamma gamma"),
    ("../../output_root/VHToGG.root", "H->gamma gamma")
]




# Tree and variable names
tree_name = "DiphotonTree/data_125_13TeV_NOTAG"

# Define integrated luminosities for each data sample (in pb)[include the values from JSON]
integrated_luminosities = {
    "Data_EraE": 5.8070,
    "Data_EraF":  17.7819,
    "Data_EraG": 3.0828
}

# Cross-section
cross_sections = {
    "GGJets": 108.3,
    "GJetPt20To40": 242.5,
    "GJetPt40": 919.1,
    "GluGluHToGG": 39.91,
    "ttHToGG": 0.5687,
    "VBFHToGG": 4.359,
    "VHToGG": 2.943
}



# Process data files
data_invariant_masses = []
for data_file_path in data_file_paths:
    data_sample_name = data_file_path.split("/")[-1].split(".")[0]
    luminosity = integrated_luminosities.get(data_sample_name, 1.0)  # Default to 1 if luminosity is not found
    data_invariant_masses.extend(process_file(data_file_path, tree_name))

# Create a histogram for data invariant masses
hist_data = ROOT.TH1F("hist_data", "", 20, 80, 180)
for mass in data_invariant_masses:
    hist_data.Fill(mass)

#  Process background files
background_hists = {}

# Colors for different backgrounds
background_colors = [ROOT.kBlue-9, ROOT.kOrange-2, ROOT.kYellow-7, ROOT.kGreen+5, ROOT.kMagenta-10, ROOT.kCyan+1, ROOT.kRed-7]

#for background_file, bg_name in background_files:
   # bg_invariant_masses = process_file(background_file, tree_name)
   # if bg_name not in background_hists:
      #  bg_hist = ROOT.TH1F(f"hist_{bg_name}", f"{bg_name} Invariant Mass", 20, 80, 180)
     #   background_hists[bg_name] = bg_hist
    #else:
    #    bg_hist = background_hists[bg_name]
   # for mass in bg_invariant_masses:
  #      bg_hist.Fill(mass)
 #   bg_hist.SetFillColor(background_colors[len(background_hists) % len(background_colors)])

# Check it!!
for idx, (background_file, bg_name) in enumerate(background_files):
    bg_invariant_masses = process_file(background_file, tree_name)
    bg_hist = ROOT.TH1F(f"hist_{bg_name}", f"{bg_name} Invariant Mass", 20, 80, 180)
    
    # Calculate the weight
    file = ROOT.TFile.Open(background_file)
    tree = file.Get(tree_name)
    n_events = tree.GetEntries()
    file.Close()
    
    cross_section = cross_sections.get(bg_name, 1.0)
    total_luminosity = sum(integrated_luminosities.values())
    weight = cross_section * total_luminosity / n_events
    
    for mass in bg_invariant_masses:
        bg_hist.Fill(mass, weight)
    
    bg_hist.SetFillColor(background_colors[idx % len(background_colors)])
    background_hists[bg_name] = bg_hist



# Create a canvas
canvas = ROOT.TCanvas("canvas", "Invariant Mass", 800, 800)

# Adjust canvas to include ratio plot
pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0.02)  # join pad1 and pad2
pad1.SetTicks(1, 1)
pad1.Draw()
pad1.cd()

# Draw the background histograms
stack = ROOT.THStack("stack", "")
for bg_name, bg_hist in background_hists.items():
    stack.Add(bg_hist)

# Set y-axis minimum to 0 and draw the histograms
stack.SetMinimum(0)
max_y = max(stack.GetMaximum(), hist_data.GetMaximum())
stack.SetMaximum(max_y * 1.2)

# Set y-axis title for the main plot
# stack.GetYaxis().SetTitle("Events")

# Draw the stack and data histogram
stack.Draw("HIST")
hist_data.SetMarkerStyle(20)
hist_data.SetMarkerSize(1.2)
hist_data.SetMarkerColor(ROOT.kBlack)
hist_data.Draw("SAME E1")

# Add legend
legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
legend.AddEntry(hist_data, "Data", "lep")
for bg_name, bg_hist in background_hists.items():
    legend.AddEntry(bg_hist, bg_name, "f")
legend.Draw()

# Draw CMS text
cms_label = ROOT.TLatex()
cms_label.SetNDC()
cms_label.SetTextFont(61)
cms_label.SetTextSize(0.04)
cms_label.DrawLatex(0.1, 0.91, "CMS")

# Draw "Work in Progress"
work_label = ROOT.TLatex()
work_label.SetNDC()
work_label.SetTextFont(52)
work_label.SetTextSize(0.03)
work_label.DrawLatex(0.16, 0.91, "Work in Progress")

# Draw energy information
energy_label = ROOT.TLatex()
energy_label.SetNDC()
energy_label.SetTextFont(42)
energy_label.SetTextSize(0.03)
energy_label.DrawLatex(0.80, 0.91, "(13.6 TeV)")

# Set ticks on all sides with smaller size
stack.GetXaxis().SetTickSize(0.02)
stack.GetYaxis().SetTickSize(0.02)

# Draw ratio plot
canvas.cd()
pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
pad2.SetTopMargin(0.05)
pad2.SetBottomMargin(0.3)
pad2.SetTicks(1, 1)
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

# Set y-axis title for the ratio plot
hist_ratio.GetYaxis().SetTitle("Data / MC")

# Add labels and title for the ratio plot
hist_ratio.GetXaxis().SetTitle("M_{bb} [GeV]")

# Set y-axis range and divisions
hist_ratio.SetMinimum(-2)
hist_ratio.SetMaximum(2)  # Adjust maximum as needed
hist_ratio.GetYaxis().SetNdivisions(505)  # Increase divisions for better visibility

# Draw horizontal lines at y=1 and y=2
line1 = ROOT.TLine(80, -1, 180, -1)
line1.SetLineStyle(2)  # Dashed line
line1.SetLineColor(ROOT.kRed)
line1.Draw()

line2 = ROOT.TLine(80, 0, 180, 0)
line2.SetLineStyle(2)  # Dashed line
line2.SetLineColor(ROOT.kRed)
line2.Draw()

# Draw the ratio histogram
hist_ratio.Draw("ep")


# Save the canvas as a PDF file
canvas.Print("/afs/cern.ch/user/s/sraj/sraj/www/CUA/HH-bbgg/invariant_mass_plot.pdf")

# Show the canvas
canvas.Draw()





